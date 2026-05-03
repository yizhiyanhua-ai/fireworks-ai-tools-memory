<div align="center">

<img src="assets/images/fireworks-ai-tools-memory-icon.png" alt="fireworks-ai-tools-memory icon" width="120" />

<br />

# fireworks-ai-tools-memory

**Persistent experience memory for AI tools, CLI workflows, and reusable scripts.**

This project extends the memory idea beyond skills and focuses on the messier operational layer: tools, toolchains, auth quirks, proxy rules, fallback paths, and scripts that already paid their tuition once.

[中文文档](README.zh-CN.md) · [MIT License](LICENSE)

</div>

![fireworks-ai-tools-memory landing image](assets/images/fireworks-ai-tools-memory-landing.png)

---

## Why Build This

`fireworks-skill-memory` solves one problem well: skill-scoped experience.

But a lot of expensive repetition does not happen at the skill layer.
It happens at the tool layer:

- one CLI searches correctly but cannot actually play
- another tool authenticates halfway then dies on callback behavior
- a daemon only works with home-directory symlinks, not external volume paths
- a script already solved the issue once, but nobody remembers where it is

Those are not “prompting mistakes.”
They are operational lessons.

`fireworks-ai-tools-memory` exists to store them explicitly.

## What It Covers

- Tool-specific pitfalls
- Best-practice invocation sequences
- Fallback chains
- Proxy and environment requirements
- Reusable scripts worth saving
- Cross-session tool playbooks for Codex or Claude Code

## Storage Model

```text
<memory-home>/
├── global/KNOWLEDGE.md
└── tools/
    └── <tool-key>/
        ├── KNOWLEDGE.md
        ├── CHECKPOINTS.md
        ├── SCRIPTS.md
        └── scripts/
            └── <saved-script>
```

## Tool Keys

Use stable keys such as:

- `ncm-cli`
- `spotify-cli`
- `yt-dlp+mpv`
- `lark-cli`
- `paseo`
- `browser-use`

## Codex Workflow

### Inject memory before a task

```bash
python3 cli/tools_memory.py inject --tool yt-dlp+mpv
```

### Save a checkpoint during work

```bash
python3 cli/tools_memory.py checkpoint \
  --tool ncm-cli \
  --note "Search may work while playback still fails because the song has no playable source."
```

### Distill lessons after a session

```bash
python3 cli/tools_memory.py flush \
  --tool spotify-cli \
  --summary-file ./session-summary.md
```

### Save a reusable script

```bash
python3 cli/tools_memory.py register-script \
  --tool yt-dlp+mpv \
  --source ./scripts/play_mix.sh \
  --name play-mix \
  --description "Start a short coding mix through mpv."
```

### List and export saved scripts

```bash
python3 cli/tools_memory.py list-scripts --tool yt-dlp+mpv
python3 cli/tools_memory.py export-script \
  --tool yt-dlp+mpv \
  --name play-mix \
  --dest /tmp/play_mix.sh
```

## What Makes It Different

This is not a generic notes bucket.

It is opinionated:

- Tool memory should be keyed by the actual runtime object that fails
- Lessons should be short, operational, and reusable
- Fallbacks are first-class knowledge
- Scripts are assets, not side notes

## Relationship to fireworks-skill-memory

- `fireworks-skill-memory`: remember how to use a skill better
- `fireworks-ai-tools-memory`: remember how to operate tools better

They are complementary, not redundant.

## Repository Assets

```text
fireworks-ai-tools-memory/
├── assets/
│   └── images/
│       ├── fireworks-ai-tools-memory-icon.png
│       └── fireworks-ai-tools-memory-landing.png
```
