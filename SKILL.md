---
name: fireworks-ai-tools-memory
description: Persistent cross-session memory for AI tool usage. TRIGGER when the user wants to remember tool pitfalls, CLI best practices, fallback chains, proxy/auth requirements, reusable scripts, or wants to build a durable tool playbook across Codex/Claude sessions.
---

# fireworks-ai-tools-memory

Persistent memory for tool usage, not just skill usage.

Use this when the important unit is a toolchain such as `ncm-cli`, `yt-dlp + mpv`, `lark-cli`, `spotify-cli`, `paseo`, `browser-use`, or any repeatable command workflow.

## What It Stores

1. Tool-specific lessons
2. Reusable fallback chains
3. Proxy and auth requirements
4. Common failure modes and recovery steps
5. Reusable scripts worth carrying across sessions

## Why It Exists

Skill memory is useful, but many expensive mistakes are not really about a skill.

They are about tools:

- wrong CLI argument order
- unstable auth callbacks
- Premium or rights restrictions
- local path quirks
- process cleanup issues
- background daemon behavior
- scripts that already solved the problem once

This skill turns those lessons into durable tool-scoped memory.

## Codex Commands

```bash
python3 cli/tools_memory.py inject --tool yt-dlp+mpv
python3 cli/tools_memory.py checkpoint --tool ncm-cli --note "Search works but playback often fails on source availability."
python3 cli/tools_memory.py flush --tool spotify-cli --summary-file ./session-summary.md
python3 cli/tools_memory.py register-script --tool yt-dlp+mpv --source ./scripts/play_mix.sh --name play-mix
python3 cli/tools_memory.py list-scripts --tool yt-dlp+mpv
python3 cli/tools_memory.py export-script --tool yt-dlp+mpv --name play-mix --dest /tmp/play_mix.sh
```

## Common User Requests

- `记住这个 tool 的坑`
- `把这次 ncm-cli 的问题沉淀下来`
- `以后遇到 Spotify CLI 认证问题先提醒我`
- `把这个脚本记到工具经验库`
- `先注入 yt-dlp + mpv 的经验再做`

## Recommended Tool Keys

- `ncm-cli`
- `spotify-cli`
- `yt-dlp+mpv`
- `lark-cli`
- `paseo`
- `browser-use`
- `feishu-docx`
- `terminal-audio`

## Practical Rule

If the user is not asking about a named skill, but the real lesson is tool behavior, store it here instead of forcing it into a skill bucket.
