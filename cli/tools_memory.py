#!/usr/bin/env python3
"""Minimal CLI for persistent tool memory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory_core.store import (
    build_injection_text,
    export_script,
    list_scripts,
    load_knowledge_text,
    register_script,
)
from runtimes.codex_runtime import add_checkpoint, flush_summary_to_knowledge


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools-memory",
        description="Shared tool-memory CLI for Codex and Claude-style workflows.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inject = sub.add_parser("inject", help="Print tool lessons and script index.")
    inject.add_argument("--tool", required=True)
    inject.add_argument("--top", type=int, default=20)

    checkpoint = sub.add_parser("checkpoint", help="Append a raw checkpoint note.")
    checkpoint.add_argument("--tool", required=True)
    checkpoint.add_argument("--note", required=True)

    show = sub.add_parser("show", help="Print a tool knowledge file.")
    show.add_argument("--tool", required=True)

    flush = sub.add_parser("flush", help="Distill lessons from summary/session inputs.")
    flush.add_argument("--tool", required=True)
    source_group = flush.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--summary-file")
    source_group.add_argument("--session-file")
    source_group.add_argument("--stdin", action="store_true")
    flush.add_argument("--include-checkpoints", action="store_true")
    flush.add_argument("--keep-checkpoints", action="store_true")
    flush.add_argument("--max-lessons", type=int, default=5)

    reg = sub.add_parser("register-script", help="Copy a reusable script into tool memory.")
    reg.add_argument("--tool", required=True)
    reg.add_argument("--source", required=True)
    reg.add_argument("--name")
    reg.add_argument("--description", default="")

    ls = sub.add_parser("list-scripts", help="List saved scripts for a tool.")
    ls.add_argument("--tool", required=True)

    exp = sub.add_parser("export-script", help="Export a saved script to a destination path.")
    exp.add_argument("--tool", required=True)
    exp.add_argument("--name", required=True)
    exp.add_argument("--dest", required=True)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "inject":
        text = build_injection_text(args.tool, top_n=args.top)
        if not text:
            print(f"[fireworks-ai-tools-memory] No memory found for tool: {args.tool}", file=sys.stderr)
            return 1
        print(text)
        return 0

    if args.command == "checkpoint":
        path = add_checkpoint(args.tool, args.note)
        print(path)
        return 0

    if args.command == "show":
        text = load_knowledge_text(args.tool)
        if not text:
            print(f"[fireworks-ai-tools-memory] No knowledge found for tool: {args.tool}", file=sys.stderr)
            return 1
        print(text)
        return 0

    if args.command == "flush":
        summary_path = Path(args.summary_file).expanduser().resolve() if args.summary_file else None
        session_path = Path(args.session_file).expanduser().resolve() if args.session_file else None
        stdin_text = sys.stdin.read() if args.stdin else None
        result = flush_summary_to_knowledge(
            args.tool,
            summary_path=summary_path,
            session_path=session_path,
            stdin_text=stdin_text,
            include_checkpoints=args.include_checkpoints,
            keep_checkpoints=args.keep_checkpoints,
            max_lessons=args.max_lessons,
        )
        print(result.knowledge_path)
        return 0

    if args.command == "register-script":
        dest = register_script(
            args.tool,
            Path(args.source).expanduser().resolve(),
            name=args.name,
            description=args.description,
        )
        print(dest)
        return 0

    if args.command == "list-scripts":
        for entry in list_scripts(args.tool):
            print(entry)
        return 0

    if args.command == "export-script":
        dest = export_script(args.tool, args.name, Path(args.dest).expanduser().resolve())
        print(dest)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
