# v5 -> v6 -> DPO (point 26)

- `pooled.md`: `scripts/pooled.py`, the three seeds' fixed/broken counts summed, exact McNemar per seed.
- `all-sets.txt`: `scripts/compare.py` per seed on every set (calls and abstentions only).

Two runs were evaluated twice. On the first pass `mtg-ft-1.5b-v5-s2-free` (77 of 722
replies) and `mtg-ft-1.5b-v6-free` (26) came back as a run of `!` characters, the
llama.cpp ROCm garbage seen before; the same models were clean on every other set.
Both were re-run on 2026-11-23 with the same GGUF and are clean (0 such replies);
every committed run was scanned for replies that start with 16 repeated characters.
