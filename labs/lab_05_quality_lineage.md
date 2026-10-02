# Lab 5 (Day 8): Data quality, master data and lineage

**Time:** 2 hours in class.

## Business context
The manager says the dashboard shows 210,000 for 14 July and her till shows 195,000. Nobody can say which is right. The team must be able to show what was rejected, why, how staff records from different systems were matched, and exactly where every number came from.

## Objective
Profile the data, enforce and report validation rules, build one master staff record, and trace a dashboard number back to its source.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Profiling: nulls, distincts, min and max, duplicates
- Reject, fix or flag: choosing an action per rule
- Master data and golden records
- Lineage in Fabric: where to find the view

## Steps
### Part A: Profile (30 min)
For each of orders, order_items, payments, complaints, write a profile in `docs/data_quality_report.md`:
row count, null counts per column, distinct counts of key columns, min and max of dates and amounts, duplicate keys.

### Part B: Rules and quarantine (40 min)
List every validation rule you enforce and which table it applies to. Then build `gold.dq_log (run_at, table_name, rows_in, rows_good, rows_rejected)` and write one row per table on each run.

### Part C: Master data (30 min)
Open `silver_staff` (from SQL) and the roster (from Excel). They describe the same people with different spellings.
Build one master record per person. Document your matching rule and what it cannot handle.

### Part D: Lineage (20 min)
In the workspace, open the Lineage view. Screenshot it. Then trace by hand: "Total revenue on the dashboard" back to source columns. Write the chain in `docs/lineage.md`.

### Part E: Quality at scale (15 min)
Run your Part A profile on `scale_orders_s1m` (from Lab 7). Then answer in the report:
1. Which profile checks got slower? Which did not?
2. If 1 percent of 100 million rows are bad, how many is that? Can a person read them all?
3. So what must a quarantine table also contain, to be useful at that size? (Hint: a count per rule and per day.)

## Test cases
Run every test. Copy this table into `submissions/lab_05/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L5-T1 | Profile covers four tables | Open `docs/data_quality_report.md`. | Row count, null counts, distinct keys, min/max and duplicate keys for orders, order_items, payments and complaints. | | |
| L5-T2 | Rules catch what they should | List each rule with the number of rows it caught. | At least eight rules, each with a count and an action. | | |
| L5-T3 | Cascade separated from real defects | Split rejected children into true defects and cascaded ones. | Your report states both counts for items, payments and complaints. | | |
| L5-T4 | Quality log grows | Run the pipeline twice and query `gold.dq_log`. | Rows for each table for each run, with different `run_at` values. | | |
| L5-T5 | Master staff | Query the master staff table. | One row per real person. 'F. Alade' and 'Funke Alade' are one person. A roster person with no system id is flagged. | | |
| L5-T6 | Matching rule has a limit | Add a fictional 'Femi Alade' to the roster and run the match. | You can show the wrong match and write how you would catch it. | | |
| L5-T7 | Lineage trace | Open the Lineage view and write the chain for 'total revenue'. | Chain from dashboard number to Gold table to Silver table to Bronze table to source column. Screenshot included. | | |
| L5-T8 | Quality at scale | Profile `scale_orders_s1m` and answer Part E. | You wrote which checks got slower and what a quarantine table must also hold at large size (counts per rule per day). | | |


## Deliverables
All four go in `submissions/lab_05/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** Notebook or SQL for the rules, `dq_log` creation SQL, master staff code; `docs/data_quality_report.md`, `docs/lineage.md`; Lineage screenshot. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: For the manager: what the data health numbers mean, what was rejected yesterday, and who to tell when a number looks wrong.

## Reflection questions
1. Which rejected row surprised you most, and what caused it?
2. Reject, fix or flag: which did you choose for each rule and why?
3. When would your staff matching rule give a wrong answer?
4. If 1 percent of 100 million rows are bad, what do you need other than a list of them?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

