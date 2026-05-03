# yt-dlp+mpv — example memory

- [2026-05] If `ncm-cli` fails because tracks have no playable source, stop retrying and switch to `yt-dlp + mpv`.  [HIT:1]
- [2026-05] Validate playback with one foreground `mpv --no-video <youtube-url>` track first, then expand to a playlist.  [HIT:1]
- [2026-05] After testing a single track, kill it before starting the real mix or you will get overlapping audio.  [HIT:1]
- [2026-05] Prefer short explicit query-built playlists over large opaque autoplay chains during coding sessions.  [HIT:1]
- [2026-05] `yt-dlp --print webpage_url "ytsearch1:<query>"` is a good default for building a stable temporary playlist file.  [HIT:1]
- [2026-05] If background `mpv` exits silently, test one track in the foreground first and only then move back to playlist mode.  [HIT:1]
