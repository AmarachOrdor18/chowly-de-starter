# Reset procedures

You should be able to put the whole environment back to a known state and rerun any lab. Do resets **top to bottom** for a full reset. Each layer can also be reset on its own.

| Layer | Script | What it removes | Then rerun |
|---|---|---|---|
| Generated data | `python data_generator/generate_data.py --out sample_data --seed 2026 --answer-key ../instructor/answer_key` | Nothing. It rewrites the sample files (same seed, same data) | Everything downstream |
| Postgres source | `reset_postgres.sql`, then `app_changes/reference_schema.postgres.sql` | The `chowly` and `chowly_scale` schemas | `python data_generator/load_sources.py --only postgres` |
| MongoDB source | `python reset/reset_mongo.py` | `complaints` and `order_events` collections | `python data_generator/load_sources.py --only mongo` |
| Fabric Bronze, Silver, quarantine, scale tables | `reset_fabric_lakehouse.py` (notebook) | Every table with a prefix: bronze_, silver_, quarantine_, scale_ | Lab 3 and Lab 4 |
| Fabric Gold | `reset_warehouse.sql` | The `gold` schema and all its tables | Lab 2 (schema) then Lab 4 (loads) |
| Landing files | Delete folders under `Files/landing/` in the lakehouse UI | Uploaded files | Lab 3 |
| Pipelines and notebooks | Delete in the workspace, or restore from Git (`git checkout <commit>`) | Items | Import again |

## Rerun test
A healthy pipeline gives the same row counts after a reset and rerun. If it does not, something is not repeatable. Write down why.

## Order for a full reset and rerun
1. Reset Gold, then Silver/Bronze, then landing files
2. Reset Postgres and MongoDB, reload them
3. Lab 3 (Bronze), Lab 4 (Silver, then Gold)
4. Compare row counts with `instructor/EXPECTED_RESULTS.md`

Never reset on a shared workspace without telling the class first.
