#!/usr/bin/env python3
"""Storage primitives for tool-scoped memory."""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class MemoryPaths:
    memory_home: Path
    tools_dir: Path
    global_file: Path


def _expand_path(value: str) -> Path:
    return Path(os.path.expanduser(value)).resolve()


def get_paths() -> MemoryPaths:
    configured_home = os.environ.get("AI_TOOLS_MEMORY_HOME")
    if configured_home:
        memory_home = _expand_path(configured_home)
    else:
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            memory_home = _expand_path(str(Path(codex_home) / "memories" / "fireworks-ai-tools-memory"))
        else:
            memory_home = _expand_path("~/.ai-tools-memory")
    tools_dir = _expand_path(os.environ.get("AI_TOOLS_MEMORY_TOOLS_DIR", str(memory_home / "tools")))
    global_file = _expand_path(os.environ.get("AI_TOOLS_MEMORY_GLOBAL_FILE", str(memory_home / "global" / "KNOWLEDGE.md")))
    return MemoryPaths(memory_home=memory_home, tools_dir=tools_dir, global_file=global_file)


def _normalize_tool_name(tool_name: str) -> str:
    name = tool_name.strip()
    if not name:
        raise ValueError("tool name must not be empty")
    return name.replace("/", "__")


def _tool_dir(tool_name: str, create: bool = False) -> Path:
    path = get_paths().tools_dir / _normalize_tool_name(tool_name)
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def _knowledge_path(tool_name: str) -> Path:
    return _tool_dir(tool_name, create=True) / "KNOWLEDGE.md"


def _knowledge_path_readonly(tool_name: str) -> Path:
    return _tool_dir(tool_name, create=False) / "KNOWLEDGE.md"


def _checkpoints_path(tool_name: str) -> Path:
    return _tool_dir(tool_name, create=True) / "CHECKPOINTS.md"


def _scripts_dir(tool_name: str) -> Path:
    path = _tool_dir(tool_name, create=True) / "scripts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _scripts_index_path(tool_name: str) -> Path:
    return _tool_dir(tool_name, create=True) / "SCRIPTS.md"


def _scripts_index_path_readonly(tool_name: str) -> Path:
    return _tool_dir(tool_name, create=False) / "SCRIPTS.md"


def read_entries(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip().startswith("- ")]


def load_knowledge_text(tool_name: str) -> str:
    path = _knowledge_path_readonly(tool_name)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _get_hit_count(entry: str) -> int:
    match = re.search(r"\[HIT:(\d+)\]", entry)
    return int(match.group(1)) if match else 0


def _set_hit_count(entry: str, count: int) -> str:
    tag = f"[HIT:{count}]"
    if re.search(r"\[HIT:\d+\]", entry):
        return re.sub(r"\[HIT:\d+\]", tag, entry)
    return f"{entry}  {tag}"


def _ensure_timestamp(entry: str) -> str:
    if re.search(r"\[\d{4}-\d{2}\]", entry):
        return entry
    return f"[{datetime.now().strftime('%Y-%m')}] {entry}"


def _render_knowledge(tool_name: str, entries: list[str]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    body = "\n".join(entries) if entries else "- [placeholder] No tool lessons recorded yet."
    return (
        f"# {tool_name} — tool memory\n\n"
        f"> Shared cross-session lessons for `{tool_name}`.\n"
        f"> Auto-maintained by fireworks-ai-tools-memory. Last updated: {today}\n\n"
        f"## Entries\n\n"
        f"{body}\n"
    )


def _render_scripts_index(tool_name: str, entries: list[str]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    body = "\n".join(entries) if entries else "- No scripts registered yet."
    return (
        f"# {tool_name} — reusable scripts\n\n"
        f"> Saved scripts for `{tool_name}`.\n"
        f"> Last updated: {today}\n\n"
        f"## Scripts\n\n"
        f"{body}\n"
    )


def _merge_entry_lines(existing: list[str], lines: list[str]) -> list[str]:
    for lesson in lines:
        line = lesson.strip()
        if not line:
            continue
        if not line.startswith("- "):
            line = f"- {line}"
        key = line[2:].lower()
        matched = False
        for index, current in enumerate(existing):
            if key[:32] and key[:32] in current.lower():
                existing[index] = _set_hit_count(current, _get_hit_count(current) + 1)
                matched = True
                break
        if not matched:
            body = _ensure_timestamp(line[2:])
            existing.append(f"- {body}  [HIT:1]")
    return existing


def merge_lessons(tool_name: str, lessons: list[str]) -> Path:
    path = _knowledge_path(tool_name)
    entries = read_entries(path)
    entries = _merge_entry_lines(entries, lessons)
    path.write_text(_render_knowledge(tool_name, entries), encoding="utf-8")
    return path


def append_checkpoint(tool_name: str, note: str) -> Path:
    path = _checkpoints_path(tool_name)
    if not path.exists():
        path.write_text(
            f"# {tool_name} — checkpoints\n\n> Raw notes captured during tool work.\n\n",
            encoding="utf-8",
        )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note.strip()}\n")
    return path


def load_checkpoints(tool_name: str) -> list[str]:
    return read_entries(_checkpoints_path(tool_name))


def clear_checkpoints(tool_name: str) -> Path:
    path = _checkpoints_path(tool_name)
    path.write_text(
        f"# {tool_name} — checkpoints\n\n> Raw notes captured during tool work.\n\n",
        encoding="utf-8",
    )
    return path


def extract_lessons_from_text(text: str) -> list[str]:
    lines = text.splitlines()
    collected: list[str] = []
    capture = False
    headers = (
        "## lessons",
        "## takeaways",
        "## best practices",
        "## pitfalls",
        "## 经验",
        "## 经验沉淀",
        "## 避坑",
        "## 最佳实践",
    )
    for raw in lines:
        line = raw.strip()
        lower = line.lower()
        if lower in headers:
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and re.match(r"^[-*]\s+.+", line):
            collected.append(re.sub(r"^[-*]\s+", "", line))
        elif capture and re.match(r"^\d+\.\s+.+", line):
            collected.append(re.sub(r"^\d+\.\s+", "", line))
    return collected


def list_scripts(tool_name: str) -> list[str]:
    index_path = _scripts_index_path_readonly(tool_name)
    return read_entries(index_path)


def register_script(tool_name: str, source: Path, *, name: str | None = None, description: str = "") -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    script_name = name or source.name
    dest = _scripts_dir(tool_name) / script_name
    shutil.copy2(source, dest)
    try:
        mode = dest.stat().st_mode
        dest.chmod(mode | 0o111)
    except Exception:
        pass

    index = _scripts_index_path(tool_name)
    entries = read_entries(index)
    rel_path = f"scripts/{script_name}"
    line = f"- `{script_name}` — {description.strip() or 'No description.'} (`{rel_path}`)"
    replaced = False
    for idx, current in enumerate(entries):
        if f"`{script_name}`" in current:
            entries[idx] = line
            replaced = True
            break
    if not replaced:
        entries.append(line)
    index.write_text(_render_scripts_index(tool_name, entries), encoding="utf-8")
    return dest


def export_script(tool_name: str, name: str, dest: Path) -> Path:
    source = _scripts_dir(tool_name) / name
    if not source.exists():
        raise FileNotFoundError(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    return dest


def build_injection_text(tool_name: str, top_n: int = 20) -> str:
    entries = read_entries(_knowledge_path_readonly(tool_name))
    ranked = sorted(entries, key=_get_hit_count, reverse=True)[: max(top_n, 1)]
    scripts = list_scripts(tool_name)[:5]
    if not ranked and not scripts:
        return ""
    body = "\n".join(ranked) if ranked else "- No lessons yet."
    scripts_body = "\n".join(scripts) if scripts else "- No reusable scripts registered."
    return (
        f"[fireworks-ai-tools-memory: {tool_name}]\n\n"
        f"Tool lessons:\n{body}\n\n"
        f"Reusable scripts:\n{scripts_body}\n"
    )
