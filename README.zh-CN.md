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

## 自然语言安装方式

如果你平时主要在 Codex 里工作，最自然的安装方式不是先背命令，而是直接说人话：

- `帮我安装 fireworks-ai-tools-memory`
- `把 fireworks-ai-tools-memory 加到我当前 Codex 环境`
- `把这个 skill 设成共享的，后面几个账号都能用`

命令行安装只是兜底：

```bash
npx skills add yizhiyanhua-ai/fireworks-ai-tools-memory
```

如果你已经把仓库拉到本地，也可以直接用仓库里的初始化脚本：

```bash
./install-codex.sh
```

## 常见自然语言用法

这个 skill 最适合你不想再重复踩工具坑的时候直接开口：

- `先注入 yt-dlp+mpv 的经验再干活`
- `把这次 ncm-cli 的问题沉淀下来`
- `把这个脚本记进工具经验库`
- `以后遇到 Spotify CLI 认证先提醒我`
- `把这次 session 里的工具教训 flush 进去`

对应到底层命令，最常见的是：

```bash
python3 cli/tools_memory.py inject --tool yt-dlp+mpv
python3 cli/tools_memory.py checkpoint --tool ncm-cli --note "搜索能成功，不代表能播出来"
python3 cli/tools_memory.py flush --tool spotify-cli --summary-file ./session-summary.md
python3 cli/tools_memory.py register-script --tool yt-dlp+mpv --source ./scripts/play_mix.sh --name play-mix
python3 cli/tools_memory.py list-scripts --tool yt-dlp+mpv
python3 cli/tools_memory.py export-script --tool yt-dlp+mpv --name play-mix --dest /tmp/play_mix.sh
```

## 为什么要做这个

`fireworks-skill-memory` 解决的是一类问题：skill 级经验记忆。

但很多代价更高的重复犯错，其实并不发生在 skill 层，而是发生在 tool 层：

- 某个 CLI 参数顺序很挑
- 搜索能成功，播放却因为音源问题直接失败
- OAuth 看起来走通了，最后卡在回调或权限
- 同一个脚本明明已经解决过问题，但下一次没人记得它在哪

这些不是“prompt 没写好”，而是工具使用经验没有被沉淀。

`fireworks-ai-tools-memory` 就是专门记这类东西的。

更直接一点说：  
很多失败不是“模型不够聪明”，而是工具的现实世界行为太脏。认证、代理、路径、播放权限、后台进程、CLI 参数顺序，这些东西如果不被显式记住，就会在下一次以几乎一样的方式再来一遍。

## 它记录什么

- 工具专属避坑经验
- 最佳调用顺序
- 常用降级链路
- 代理、环境变量、认证要求
- 值得复用的脚本
- 跨会话可继承的工具使用手册

## 技术原理

这个项目其实做了三件很朴素但很必要的事：

1. 把“经验”的粒度从 skill 改成 tool key  
   不是记“这次写了什么 prompt”，而是记 `ncm-cli`、`spotify-cli`、`yt-dlp+mpv` 这些真实会翻车的运行对象。
2. 把会话中的临时教训变成结构化文件  
   用 `CHECKPOINTS.md` 兜住现场笔记，用 `KNOWLEDGE.md` 留住后续可复用的 lessons，用 `SCRIPTS.md` 和 `scripts/` 收住真正有用的脚本。
3. 把“下一次少走弯路”变成一个明确闭环  
   任务前 `inject`，任务中 `checkpoint`，任务后 `flush`，跑通一次的脚本再 `register-script`。

### 1. 整体架构

![Architecture Overview](docs/diagrams/architecture-overview.png)

这张图讲的是最核心的结构：

- 调用层只负责表达意图，不负责记忆
- CLI 和 runtime 负责把意图路由成操作
- store 层负责把 lessons、checkpoints、scripts 落盘
- 真正的记忆对象是 `tool-key`，不是仓库名，也不是某次 prompt

### 2. 一次任务是怎么沉淀成“下次更稳”的

![Session Memory Loop](docs/diagrams/session-memory-loop.png)

这件事的关键不在安装时，而在任务进行中：

- `inject` 在任务开始前把已有经验先塞回来
- 工具真正翻车时，用 `checkpoint` 先保住原始细节
- 会话结束后再用 `flush` 从 summary / session 里提炼出可复用的 lesson
- 如果中途出现真正值钱的脚本，再单独注册成资产

这就是它必要的原因。很多工具链问题只有在真实使用时才暴露，等会话结束再回忆，细节往往已经丢了。

### 3. 为什么它必须和 fireworks-skill-memory 分开

![Skill Boundary](docs/diagrams/skill-boundary.png)

这层边界如果不划清，后面一定会越记越乱。

- `fireworks-skill-memory` 更适合记某个 skill 自己的策略、偏好和输出方式
- `fireworks-ai-tools-memory` 更适合记跨 skill 复用的工具行为、坑点和脚本

把工具经验硬塞进 skill memory，问题不是“不能用”，而是经验会变得太局部，复用价值急剧下降。

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
├── docs/
│   └── diagrams/
│       ├── architecture-overview.svg
│       ├── architecture-overview.png
│       ├── session-memory-loop.svg
│       ├── session-memory-loop.png
│       ├── skill-boundary.svg
│       └── skill-boundary.png
```
