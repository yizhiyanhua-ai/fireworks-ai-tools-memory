<div align="center">

<img src="assets/images/fireworks-ai-tools-memory-icon.png" alt="fireworks-ai-tools-memory icon" width="120" />

<br />

# fireworks-ai-tools-memory

**给 AI 工具、CLI 工作流和可复用脚本做持久化经验记忆。**

这个项目不是记“某个 skill 怎么用”，而是记更容易反复踩坑的那一层：工具、工具链、认证、代理、降级链路，以及那些已经救过你一次的脚本。

[English](README.md) · [MIT License](LICENSE)

</div>

![fireworks-ai-tools-memory landing image](assets/images/fireworks-ai-tools-memory-landing.png)

---

## 为什么要做这个

`fireworks-skill-memory` 解决的是一类问题：skill 级经验记忆。

但很多代价更高的重复犯错，其实并不发生在 skill 层，而是发生在 tool 层：

- 某个 CLI 参数顺序很挑
- 搜索能成功，播放却因为音源问题直接失败
- OAuth 看起来走通了，最后卡在回调或权限
- 同一个脚本明明已经解决过问题，但下一次没人记得它在哪

这些不是“prompt 没写好”，而是工具使用经验没有被沉淀。

`fireworks-ai-tools-memory` 就是专门记这类东西的。

## 它记录什么

- 工具专属避坑经验
- 最佳调用顺序
- 常用降级链路
- 代理、环境变量、认证要求
- 值得复用的脚本
- 跨会话可继承的工具使用手册

## 存储结构

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

## 推荐的 tool key

- `ncm-cli`
- `spotify-cli`
- `yt-dlp+mpv`
- `lark-cli`
- `paseo`
- `browser-use`

## Codex 里的典型用法

### 任务前注入工具经验

```bash
python3 cli/tools_memory.py inject --tool yt-dlp+mpv
```

### 工作中记录 checkpoint

```bash
python3 cli/tools_memory.py checkpoint \
  --tool ncm-cli \
  --note "搜索能成功，不代表能播出来；很多歌会死在音源可用性。"
```

### 任务后提炼 lessons

```bash
python3 cli/tools_memory.py flush \
  --tool spotify-cli \
  --summary-file ./session-summary.md
```

### 记住一个值得复用的脚本

```bash
python3 cli/tools_memory.py register-script \
  --tool yt-dlp+mpv \
  --source ./scripts/play_mix.sh \
  --name play-mix \
  --description "用 mpv 启动一条短编码混播。"
```

### 查看和导出脚本

```bash
python3 cli/tools_memory.py list-scripts --tool yt-dlp+mpv
python3 cli/tools_memory.py export-script \
  --tool yt-dlp+mpv \
  --name play-mix \
  --dest /tmp/play_mix.sh
```

## 它和 fireworks-skill-memory 的关系

- `fireworks-skill-memory`：记住某个 skill 该怎么用得更稳
- `fireworks-ai-tools-memory`：记住某个工具、某条工具链该怎么操作才不翻车

这两个不是替代关系，而是互补关系。

## 仓库资源

```text
fireworks-ai-tools-memory/
├── assets/
│   └── images/
│       ├── fireworks-ai-tools-memory-icon.png
│       └── fireworks-ai-tools-memory-landing.png
```
