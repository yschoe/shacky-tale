# Session Log

Date: 2026-03-24
Workspace: `/home/yschoe/git/shacky-tales`

## Timeline

1. Compared `shacky/` and `shacky_t/` and confirmed they were identical except for filename/path capitalization.
2. Verified `shacky/` removal after user deleted it externally.
3. Ported the Turbo Pascal game to Python in `shacky_python/` using `pygame`.
4. Implemented `.fon` asset loading (black/white rendering) and map loading with fallback behavior.
5. Added input buffering and truncation for repeated key events, with movement/action cooldowns.
6. Added run documentation in `shacky_python/README.md`.
7. Generated `shacky_python/map2.map` and updated loader priority to use local map first.
8. Fixed rapid HP drain by throttling world ticks and capping per-tick HP loss.
9. Added splash/intro screens before gameplay.
10. Tuned gameplay further:
   - Slower HP loss and less sticky monster movement with randomized movement candidates.
   - Reduced spawn frequency and added off-screen monster culling.
11. Reworked map and world design:
   - Smaller map dimensions (`72x36`) with larger terrain clumps.
   - Large water region with island.
   - Goddess (`A`) placed on island; shoemaker (`v`) placed on opposite side.
   - Region-based monster spawning by biome.
12. Adjusted map to ensure landmark reachability:
   - Reduced forest density.
   - Carved explicit trail corridors so land landmarks are reachable on foot.
   - Kept island landmarks reachable only with shoes (water traversal).
13. User restored original assets (`map2.map` and missing `.fon` files).
14. Updated Python port to support dynamic map dimensions from loaded map file.
15. Added proper message-box word wrapping and map-view sizing fixes.
16. Added primitive `.sd` music playback based on Pascal `sounds.pas`.
17. Restored shoemaker gate logic to original behavior (requires gem).
18. Updated splash and characters screens to white background / black text.
19. Added message-box portraits for dialog events.
20. Reduced message font and placed wrapped text below portrait.
21. Produced a parity checklist versus `shacky_t/shacky.pas`.
22. Created `fonted/` and ported `foned90.pas` to Python as `fonted/fonted.py` with README.
23. Created static web port in `shacky_web/`:
   - `index.html`, `game.js`, auto-generated hard-coded `assets.js`, `README.md`
   - Ported gameplay loop from Python version for browser canvas.
24. Added held-key movement repeat to both ports:
   - Web: key hold repeat with initial delay and interval
   - Python: KEYUP-aware hold repeat with same timing.
25. Added movement/attack SFX to both ports.
26. Reduced movement SFX volume by half in both ports.

## Files Created/Updated During Session

- `shacky_python/main.py`
- `shacky_python/README.md`
- `shacky_python/map2.map`
- `fonted/fonted.py`
- `fonted/README.md`
- `shacky_web/index.html`
- `shacky_web/assets.js`
- `shacky_web/game.js`
- `shacky_web/README.md`
- `log.md`
- `transcript.md`

## Latest Request

- User asked: `Yes, please go ahead.` (update logs)
- `log.md` and `transcript.md` updated.
