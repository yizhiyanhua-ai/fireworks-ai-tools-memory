"""Codex-specific adapters for explicit tool-memory workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from memory_core.store import (
    append_checkpoint,
    clear_checkpoints,
    extract_lessons_from_text,
    load_checkpoints,
    merge_lessons,
)


@dataclass(frozen=True)
class FlushResult:
    knowledge_path: Path
    lessons: list[str]
    checkpoints_cleared: bool


def add_checkpoint(tool_name: str, note: str) -> Path:
    return append_checkpoint(tool_name, note)


def _extract_text_from_json(value: object) -> list[str]:
    chunks: list[str] = []
    if isinstance(value, str):
        chunks.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            chunks.extend(_extract_text_from_json(item))
    elif isinstance(value, list):
        for item in value:
            chunks.extend(_extract_text_from_json(item))
    return chunks


def load_codex_source_text(
    *,
    summary_path: Path | None = None,
    session_path: Path | None = None,
    stdin_text: str | None = None,
) -> str:
    if summary_path is not None:
        if not summary_path.exists():
            raise FileNotFoundError(summary_path)
        return summary_path.read_text(encoding="utf-8")

    if session_path is not None:
        if not session_path.exists():
            raise FileNotFoundError(session_path)
        raw = session_path.read_text(encoding="utf-8")
        suffix = session_path.suffix.lower()
        if suffix in {".md", ".txt"}:
            return raw
        if suffix == ".json":
            try:
                return "\n".join(_extract_text_from_json(json.loads(raw)))
            except Exception:
                return raw
        if suffix == ".jsonl":
            chunks: list[str] = []
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    chunks.extend(_extract_text_from_json(json.loads(line)))
                except Exception:
                    chunks.append(line)
            return "\n".join(chunks)
        return raw

    if stdin_text is not None:
        text = stdin_text.strip()
        if not text:
            raise ValueError("stdin summary text is empty")
        return text

    raise ValueError("no summary source provided")


def flush_summary_to_knowledge(
    tool_name: str,
    *,
    summary_path: Path | None = None,
    session_path: Path | None = None,
    stdin_text: str | None = None,
    include_checkpoints: bool = False,
    keep_checkpoints: bool = False,
    max_lessons: int = 5,
) -> FlushResult:
    summary_text = load_codex_source_text(
        summary_path=summary_path,
        session_path=session_path,
        stdin_text=stdin_text,
    )
    lessons = extract_lessons_from_text(summary_text)

    if include_checkpoints:
        checkpoint_text = "\n".join(load_checkpoints(tool_name))
        lessons.extend(extract_lessons_from_text(checkpoint_text))

    deduped: list[str] = []
    seen: set[str] = set()
    for lesson in lessons:
        normalized = lesson.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(lesson.strip())

    if not deduped:
        raise ValueError("no lesson candidates found in the provided source")

    selected = deduped[: max(max_lessons, 1)]
    knowledge_path = merge_lessons(tool_name, selected)

    if keep_checkpoints:
        cleared = False
    else:
        clear_checkpoints(tool_name)
        cleared = True

    return FlushResult(
        knowledge_path=knowledge_path,
        lessons=selected,
        checkpoints_cleared=cleared,
    )
