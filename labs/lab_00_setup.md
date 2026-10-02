# Lab 0 (Day 1): Set up your Fabric workspace

**Time:** 60 minutes in class

## Business context
Chowly's new analytics team has been given a blank Microsoft Fabric tenant. Before anyone can move a single order into it, the team needs a workspace that works, a place for raw and cleaned data, a place for the final analytical tables, and a record of who did what.

## Objective
Create a working workspace with a lakehouse and a warehouse, prove they run code, and connect the workspace to Git.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- What a Fabric workspace, lakehouse and warehouse are (read the current Microsoft Learn overview of each)
- What a SQL analytics endpoint is, in one paragraph
- Basic Git: clone, commit, push

## Steps
Follow `docs/01_fabric_setup.md`, steps 1 to 6, exactly. Use the names `lh_chowly` and `wh_chowly`.

## Test cases
Run every test. Copy this table into `submissions/lab_00/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L0-T1 | Notebook runs | Run the smoke test notebook from the setup guide. | It prints 1 and creates a table named `smoke_test`. | | |
| L0-T2 | SQL endpoint sees the lakehouse table | Open the SQL analytics endpoint and run `SELECT * FROM smoke_test`. If it is missing, wait a minute and refresh. | One row: item_id 1, name Jollof Rice. | | |
| L0-T3 | Warehouse runs SQL | In `wh_chowly` run `SELECT 1 AS it_works;` | Returns one row. | | |
| L0-T4 | Git is connected | Commit a change from Fabric or push your exported notebook. | The commit appears in your GitHub fork. | | |
| L0-T5 | Names are exact | List the items in your workspace. | `lh_chowly` and `wh_chowly` exist with those exact names. | | |


## Deliverables
All four go in `submissions/lab_00/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** Screenshot of the workspace item list; The smoke-test notebook (Git-synced or exported `.ipynb`); Link to your first commit. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: How a new teammate can create the same workspace in 10 minutes: items, names, the smoke test, and the three mistakes to avoid.

## Reflection questions
1. What problem does a lakehouse solve that a normal database does not?
2. What was the first thing that went wrong in your setup, and how did you find out why?
3. Why do we name the items exactly the same way as everyone else?
4. Which step would you explain differently to a beginner?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

