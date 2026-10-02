# Scale experiments

Chowly works with 3,800 orders. What happens with 10 million, or 100 million? In this folder you find out, **by measuring**.

## The rule of this folder
**Never write a performance number you did not measure.** Every timing goes into the `scale_benchmark_log` table through the `timed()` helper, together with the row count, the operation and notes about your Fabric capacity. If something could not be tested, write `NOT VERIFIED`.

## Files
| File | Used in |
|---|---|
| `postgres_scale_seed.sql` | Day 1 demo: make the operational database big, watch it struggle |
| `10_scale_setup.py` | Build scale tables of chosen sizes in the lakehouse |
| `11_scale_experiments.py` | Experiments 1 to 4 (full vs incremental, size, SQL vs Spark, partitioning) |

## Suggested sizes
Start small and go up only if the run finishes comfortably. Record what your capacity could and could not do.

| Label | Approx. orders | Notes |
|---|---|---|
| `s100k` | 100 thousand | Always run this first |
| `s1m` | 1 million | Normal for a class capacity |
| `s10m` | 10 million | Try it; watch the session |
| `s100m` | 100 million | NOT VERIFIED. Only the instructor tries this, on a large capacity |

## What you are looking for
- Which operations grew roughly with the data, and which did not
- What changed when you only touched new rows
- What changed when files were organised by date
- What SQL did well, and what Spark did well
