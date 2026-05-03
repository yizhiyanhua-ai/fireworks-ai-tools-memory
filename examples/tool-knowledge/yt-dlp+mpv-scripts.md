# yt-dlp+mpv — reusable script seeds

- `build_playlist.sh` — source: `/Volumes/ExtaData/newcode/fireworks-radio/scripts/build_playlist.sh`
  用搜索词批量生成临时 `.m3u` 播放清单。

- `play_mix.sh` — source: `/Volumes/ExtaData/newcode/fireworks-radio/scripts/play_mix.sh`
  负责生成预设混播、清理旧 PID、启动 `mpv`。

- `stop_mix.sh` — source: `/Volumes/ExtaData/newcode/fireworks-radio/scripts/stop_mix.sh`
  负责根据 PID 文件收掉当前混播，避免残留进程。

Recommended import commands:

```bash
python3 cli/tools_memory.py register-script \
  --tool yt-dlp+mpv \
  --source /Volumes/ExtaData/newcode/fireworks-radio/scripts/build_playlist.sh \
  --name build-playlist \
  --description "Build a short YouTube playlist from explicit queries."

python3 cli/tools_memory.py register-script \
  --tool yt-dlp+mpv \
  --source /Volumes/ExtaData/newcode/fireworks-radio/scripts/play_mix.sh \
  --name play-mix \
  --description "Start a short coding mix through mpv."

python3 cli/tools_memory.py register-script \
  --tool yt-dlp+mpv \
  --source /Volumes/ExtaData/newcode/fireworks-radio/scripts/stop_mix.sh \
  --name stop-mix \
  --description "Stop the current mpv mix via stored PID."
```
