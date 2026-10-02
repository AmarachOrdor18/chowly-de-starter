# Chowly Data Engineering on Microsoft Fabric

You built Chowly, a restaurant app that takes orders. Now you will build the data platform behind it, in Microsoft Fabric, and serve the results back into your app as a manager dashboard. No Power BI.

```
 SOURCES                          MICROSOFT FABRIC                                  YOUR APP
 Postgres  (orders, menu, staff)  Data Factory pipelines                            Manager role
 MongoDB   (complaints, events)     -> Lakehouse  BRONZE (raw)  -> SILVER (clean)         ^
 Files     (prices, roster, stock)  -> Warehouse  GOLD (star schema)  -------------->  Analytics API
 APIs      (weather, holidays)      Eventstream -> Eventhouse (live)                  -> Dashboard
                                    Lineage, security, governance
```

## Start here
0. `docs/03_day0_primer.md`: can you do these ten things?
1. `docs/00_prerequisites.md`: accounts and tools (do this before Day 1)
2. `docs/04_deliverables_guide.md`: what you hand in for every lab
3. `docs/01_fabric_setup.md`: create your workspace, lakehouse and warehouse
4. `docs/02_source_systems_setup.md`: source databases and sample history

## What is in this repo
| Folder | What |
|---|---|
| `docs/` | Setup guides |
| `app_changes/` | `source_features.md` (build the four source types into your app), `upgrade_your_app.md` (five changes so it remembers), and the reference schema |
| `data_generator/` | Creates months of realistic, deliberately messy data, and loads it into your sources |
| `sample_data/` | The shared dataset everyone uses (seed 2026) |
| `notebooks/` | Fabric notebooks (`.py` files with `# %%` cells, and `.ipynb` copies to import) |
| `warehouse/` | Gold schema starter SQL |
| `labs/` | One guide per lab: business context, steps, test cases and four deliverables |
| `submissions/`, `templates/` | Where your lab deliverables go, and the templates for them |
| `assignments/` | Two assignments |
| `capstone/` | The capstone brief |
| `analytics_api/` | A reference API that reads Gold and serves your dashboard |
| `scale/` | Experiments that show what changes when data gets big. Measured numbers only |
| `reset/` | Put any layer back to a known state and rerun |

## Rules of the course
- Fork this repo. Commit after every lab. History is graded.
- Never commit secrets. `.env` is git-ignored. Keep it that way.
- Use an AI assistant and keep a log: `ai_log.md` with prompt, result, what you accepted, what you rejected, what you fixed yourself.
- Bronze is raw. Silver is clean. Gold is for people.

## Importing notebooks into Fabric
Workspace > Import > Notebook > select the `.ipynb` from `notebooks/`. Attach `lh_chowly` as the default lakehouse.
