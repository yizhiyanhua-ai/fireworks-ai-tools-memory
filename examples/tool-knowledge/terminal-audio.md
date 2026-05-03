# terminal-audio — example memory

- [2026-05] When the user says “没声音”, first separate four classes of failure: source availability, auth/permissions, player process state, and double playback.  [HIT:1]
- [2026-05] Do not assume a stopped state means no audio bug; there may already be a foreground test process still playing outside the main queue.  [HIT:1]
- [2026-05] Before starting a new mix, inspect existing player processes and kill test leftovers so the user does not hear overlapping tracks.  [HIT:1]
- [2026-05] For coding-session music, a short explicit mix is operationally better than a huge queue because it is easier to verify, restart, and debug.  [HIT:1]
- [2026-05] In real usage, the fastest path is usually not the most elegant stack; it is the one that produces audible output with the fewest moving parts.  [HIT:1]
