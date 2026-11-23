# Doodligo production status

Workflow per episode: Muse (muse.ai, in the Claude desktop app's browser) makes 12 × 10 s 3D clips
(two batches of 6) + voice MP3s (same "v2" voices as Ep01) → `engine/compose.py` adds captions,
cards, music, title/end cards → push to `videos/` → Sonap import (github_path) → schedule 16:30 UTC.

Prompts for Muse: `PYTHONPATH=episodes python3 engine/prep.py episodes/<ep>.py clips1|clips2|voices`

| Ep | Code | Clips | Voices | Video | Scheduled (UTC) |
|----|------|-------|--------|-------|-----------------|
| 01 | dl001_colors | ✅ | ✅ | ✅ | 2026-11-23 16:30 |
| 02 | dl002_counting | ✅ | ✅ | ✅ | 2026-11-24 16:30 |
| 03 | dl003_abc | ✅ | ✅ | ✅ | 2026-11-25 16:30 |
| 04 | dl004_farm | 6/12 | – | – | – |
| 05 | dl005_shapes | – | – | – | – |
| 06 | dl006_fruit | – | – | – | – |
| 07 | dl007_wild | – | – | – | – |
| 08 | dl008_teeth | – | – | – | – |
| 09 | dl009_weather | – | – | – | – |
| 10 | dl010_ocean | – | – | – | – |

Muse weekly usage limit reached on 2026-11-23; resets Monday 2026-11-30 11:03 (Asia/Colombo).
