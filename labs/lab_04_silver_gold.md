# Lab 4 (Day 6): Bronze to Silver to Gold, with an incremental load

**Time:** 2 hours in class.

## Business context
The raw copy has duplicates, dates stored as text, negative quantities and payments for orders that do not exist. If the dashboard read it, the manager's revenue would be wrong and nobody would know why. And the nightly copy rereads everything, which will not survive growth.

## Objective
Clean Bronze into Silver with bad rows quarantined, load the Gold star schema, and make the load incremental and safe to rerun.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Cleaning patterns in PySpark: casting, deduplication with a window, splitting good and bad rows
- How the warehouse reads a lakehouse table (cross-item query)
- Watermark, incremental load, idempotent load
- Why NULL handling in rules matters

## Steps
### Part A: Silver (60 min)
Open `notebooks/03_silver_transform.py`. The orders table is done as a worked example. Finish order_items, payments and complaints with the rules listed in the notebook.
After each table, print how many rows went to Silver and how many to quarantine.

### Part B: Load Gold (40 min)
In `wh_chowly`, load your dimensions and `fact_order` from Silver using T-SQL `INSERT ... SELECT` across the lakehouse and warehouse.
Hint: lakehouse tables are reachable as `[lh_chowly].[dbo].[table_name]` from the warehouse.

### Part C: Make it incremental (20 min)
1. Create `gold.etl_watermark (table_name, last_loaded_at)`.
2. Change your `fact_order` load to only take rows where `updated_at` is greater than the watermark.
3. Move the watermark forward at the end.
4. Prove it: update one order in Postgres, re-run the pipeline, and show that only one row moved.

### Instructor demo (not a student task)
Your instructor runs Experiment 1 (full vs incremental) once on the 1M-order table and records the result in `scale_benchmark_log`. You repeat it yourself in Lab 7.

## Test cases
Run every test. Copy this table into `submissions/lab_04/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L4-T1 | Nothing is lost | For orders, add Silver and quarantine row counts. | Silver plus quarantine equals the number of distinct orders in Bronze. | | |
| L4-T2 | Silver reruns cleanly | Run the Silver notebook twice. | The same counts both times. | | |
| L4-T3 | NULL is not silently passed | Put a row with a NULL quantity through your rule. | It goes to quarantine, with the rule name recorded. | | |
| L4-T4 | Cascade is visible | Count quarantined order items whose parent order is also quarantined. | You can state how many quarantined children are not bad themselves. | | |
| L4-T5 | Gold reconciles | Compare the sum of line amounts with the sum of order totals. | The two sums are equal. | | |
| L4-T6 | History in the join | Check Jollof Rice lines placed before and after 15 June. | Lines before use the 3,500 price period, lines after use 4,000. | | |
| L4-T7 | Incremental works | Update one order in Postgres, rerun the pipeline. | Exactly one `fact_order` row changes and the watermark moves forward. | | |
| L4-T8 | Double run does not double | Run the Gold load twice in a row. | `fact_order` has the same row count after the second run. | | |
| L4-T9 | Late update is caught | Change an old order in Postgres so its `updated_at` is newer than the watermark. | The next run picks it up. | | |


## Deliverables
All four go in `submissions/lab_04/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** Silver notebook, Gold SQL, and the pipeline (Git-synced or exported); `docs/incremental_proof.md` with before/after row counts; Screenshots of Silver and quarantine counts. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: How the nightly pipeline works, what it does on a rerun, where rejected rows go, and how someone checks that Gold matches Silver.

## Reflection questions
1. Why do we quarantine instead of delete?
2. What does 'idempotent' mean for your Gold load? How did you test it?
3. Which rule produced the most rejects and is that a data problem or a rule problem?
4. What would you change if this table had 100 million rows?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

