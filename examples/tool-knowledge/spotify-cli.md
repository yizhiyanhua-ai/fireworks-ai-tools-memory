# spotify-cli — example memory

- [2026-05] Spotify CLI 的问题通常不是“再点一次登录就好了”，而是 OAuth 回调、本地监听、缓存状态和 Premium 限制叠在一起。  [HIT:1]
- [2026-05] `spotify_player` 在当前环境里可能生成授权链接，但本地 `127.0.0.1` 回调并不稳定，不能把“浏览器已跳转”误判成“CLI 已可用”。  [HIT:1]
- [2026-05] `spotify-tui` 旧版本可能还在用 `localhost` 回调，而 Spotify Developer Dashboard 不再接受它；这时必须改成 `127.0.0.1` 或直接补丁二进制。  [HIT:1]
- [2026-05] 即使 token 已拿到，也不等于 API 可用；若官方 API 返回 `403 Active premium subscription required for the owner of the app`，就别再折腾 CLI 了。  [HIT:1]
- [2026-05] 当 Spotify 路线死在 Premium 限制时，最务实的策略是直接切到别的播放源，而不是继续修播放器。  [HIT:1]

