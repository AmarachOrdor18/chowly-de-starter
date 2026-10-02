# Fabric setup (Day 1 lab)

Names matter. Use exactly these so the notebooks and SQL in this repo work without edits.

## Step 1: Create the workspace
1. Sign in at https://app.fabric.microsoft.com
2. Workspaces > New workspace. Name it `chowly-<yourname>`.
3. Under Advanced, make sure it is assigned to the capacity your instructor gave you.

## Step 2: Create the items
| Item | Name | What it is for |
|---|---|---|
| Lakehouse | `lh_chowly` | Raw and cleaned data: Bronze and Silver |
| Warehouse | `wh_chowly` | The analytical star schema: Gold |

Create them from the workspace: New item > Lakehouse, then New item > Warehouse.

## Step 3: Look around (do this before touching anything)
In `lh_chowly`, find **Tables** and **Files**. Tables hold structured Delta tables. Files hold anything (CSV, JSON, Excel).
Every Lakehouse also gets a **SQL analytics endpoint**: a read-only T-SQL door to your tables. Find it in the item list.
In `wh_chowly`, open a new SQL query and run `SELECT 1 AS it_works;`

## Step 4: Create the landing folders
In `lh_chowly` > Files, create these folders:
```
landing/
  files/      <- supplier prices, roster, stock counts
  nosql/      <- complaints and order events from MongoDB
```
Upload `sample_data/weather_daily.json` and `sample_data/holidays.json` into `landing/` (they are fallbacks for the API lab).

## Step 5: Connect the workspace to Git
Workspace settings > Git integration > connect to your GitHub fork. Commit after each lab. Fabric stores notebooks and pipelines as files, so your history will show the work as it happened.
If the Git option is unavailable for your account, export notebooks and pipeline JSON by hand into the `fabric_export/` folder of your repo and commit them.

## Step 6: Run the smoke test
Create a notebook, attach `lh_chowly` as the default lakehouse, and run:
```python
df = spark.createDataFrame([(1, "Jollof Rice")], ["item_id", "name"])
df.write.format("delta").mode("overwrite").saveAsTable("smoke_test")
print(spark.table("smoke_test").count())
```
Then open the SQL analytics endpoint and run `SELECT * FROM smoke_test`. If the table does not show up right away, wait a minute and refresh. The endpoint can lag behind fresh writes.

## Done when
- Workspace, `lh_chowly`, `wh_chowly` exist
- Smoke test passes
- Git connected (or the fallback folder exists) and your first commit is pushed
- A screenshot of your workspace item list is in `docs/screenshots/day1.png`

## Common problems
| Symptom | Likely cause |
|---|---|
| Cannot create a Lakehouse | Workspace is not on a Fabric capacity |
| Notebook is slow to start | First session start takes a minute or two; reuse the session |
| Table missing in the SQL endpoint | Metadata sync delay; wait and refresh |
| Everyone's notebooks crawl | Shared capacity is saturated; stop idle sessions |
