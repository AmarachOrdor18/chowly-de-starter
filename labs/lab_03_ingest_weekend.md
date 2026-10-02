# Lab 3 (Weekend 1): Ingest all four source types into Bronze

**Time:** about 3 hours, at your own pace. Demo it on Monday (5 minutes).

## Business context
Chowly's data is now in four different places: a Postgres database, a MongoDB cluster, spreadsheets and files from suppliers and HR, and two public APIs. Nothing can be cleaned or modelled until it is all in one place, unchanged, so that there is always an honest copy of what each source said.

## Objective
Land every source untouched in the Bronze layer with bookkeeping columns, and show that a rerun or a failure does not corrupt it.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Data Factory Copy activity: source, destination, mapping (current Microsoft Learn page)
- Reading CSV, JSON and Excel in a notebook
- What Delta tables are, in one paragraph
- ETL versus ELT, and when a Dataflow Gen2 is the right tool

## Steps
### The rule
Land the data **untouched**. No cleaning in Bronze. Only bookkeeping columns.

### Part A: SQL source with a Data Factory pipeline
1. In your workspace: New item > Data pipeline `pl_ingest_sql`.
2. Add a **Copy data** activity. Source: your Postgres connection, table `chowly.orders`. Destination: `lh_chowly`, table `bronze_orders` (overwrite for now).
3. Repeat for `order_items`, `payments`, `menu_items`, `menu_price_history`, `staff`. (Tip: one ForEach over a list of table names is cleaner. Try it if you feel brave.)

### Part B: NoSQL source
Copy the MongoDB collections `complaints` and `order_events` into `Files/landing/nosql/` as JSON.
If the MongoDB connector is not available to you, upload `sample_data/complaints.jsonl` and `order_events.jsonl` by hand and write down what you did and why in `docs/ingest_notes.md`.

### Part C: Files
Take the files your own app's upload feature stored (A3), and also `sample_data/files/*` for the full history. Upload them into `Files/landing/files/`. Notice how your filename contract from A3 lets the notebook find every weekly file with one pattern. Run notebook `01_bronze_files.py` (paste its cells into a Fabric notebook, or import the `.ipynb` version). Finish the TODO for the Excel roster.

### Part D: API
Run notebook `02_bronze_api.py`. Finish the holidays TODO. Compare: your app's `daily_context` table (A4) holds one row per day from the day you built it. The notebook fetches the whole four months of history at once. Write two lines on when you would use each.

### Part E: ETL the other way (one source only)
Land the Excel staff roster again, this time with a **Dataflow Gen2**, cleaning names on the way in. Write 5 lines in `docs/ingest_notes.md`: which way was easier, and what would break at 100x the data?


### Then: Assignment 1
See `assignments/assignment_1.md`. Due Monday morning.

## Test cases
Run every test. Copy this table into `submissions/lab_03/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L3-T1 | Bronze row counts match the sources | Count rows in every Bronze table and compare with its source. | orders 3,839; order_items 12,004; payments 3,804; menu_items 24; menu_price_history 27; staff 9; complaints 276; order_events 15,216; supplier_prices 152; stock_counts 4; staff_roster 10; weather_daily 123 (fallback file). | | |
| L3-T2 | Bronze is untouched | Count `bronze_orders` rows and distinct order ids. | The row count includes the duplicate rows. You did not clean anything. | | |
| L3-T3 | Rerun does not double | Run your ingest a second time. | Counts are the same as after the first run. | | |
| L3-T4 | API outage | Break the API URL on purpose and run the notebook. | The fallback file is used, `bronze_weather_daily` still has 123 rows, and `_source` says `fallback-file`. | | |
| L3-T5 | Malformed file | Add a supplier file where a price says `N/A` and run the ingest. | The pipeline does not fail. The bad value is visible in Bronze as text. | | |
| L3-T6 | New weekly file is picked up | Add `supplier_prices_2026-09-07.csv` with 8 rows. | Supplier Bronze count becomes 160 without changing any code. | | |
| L3-T7 | Bookkeeping columns exist | Inspect the schema of any Bronze table. | `_ingested_at`, `_source` and (for files) `_source_file` exist. | | |
| L3-T8 | Nested JSON is preserved | Print the schema of `bronze_complaints`. | The `meta` field is still a nested struct. | | |
| L3-T9 | ETL one, ELT the rest | Compare your Dataflow Gen2 roster load with your notebook load. | Both produce the same 10 roster rows; you wrote five lines on which was easier. | | |


## Deliverables
All four go in `submissions/lab_03/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** Exported pipeline(s) and notebooks (Git-synced or JSON/ipynb); `docs/ingest_notes.md` with row counts and your ETL-vs-ELT notes; Screenshot of each Bronze table with its count. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: A map of the four sources: how each is pulled, how often, how each can fail, and what the pipeline does when it does.

## Reflection questions
1. Why do we keep duplicates and bad dates in Bronze?
2. Which source was the most annoying to ingest, and why?
3. What would break first if the orders table had 5 million rows?
4. Where did your AI assistant help, and where did it invent something?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

