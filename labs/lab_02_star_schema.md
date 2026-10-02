# Lab 2 (Day 4): Design and build the star schema

**Time:** 2 hours in class.

## Business context
The manager wants four numbers every morning: revenue by day and category, average wait per chef by hour, complaint rate for delayed versus on-time orders, and complaints per waiter. The live tables cannot answer these quickly or safely. The analytics team must design a model where these questions become simple queries and where last year's price is still last year's price.

## Objective
Turn the manager's questions into fact and dimension tables, state the grain of each fact, and prove that history survives a price change.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Facts, dimensions, measures and grain (Day 3 notes)
- Slowly changing dimension Type 2 in plain words
- Basic DDL: CREATE TABLE and primary keys (note: Fabric Warehouse primary keys are NOT ENFORCED)

## Steps
### Part A: Design on paper first (40 min)
On your whiteboard or paper, for each of these manager questions, mark the **measure** (the number) and the **dimensions** (the "by" words):
1. Revenue by day and by category
2. Average actual wait per chef, by hour
3. Complaint rate for delayed vs on-time orders
4. Which waiter has the most complaints per 100 orders?

Then, for each fact table (`fact_order_item`, `fact_order`, `fact_payment`, `fact_complaint`) write ONE sentence: "One row = ______". This is the grain.

### Part B: Build it (50 min)
Open `warehouse/01_create_gold_schema.sql`. One dimension is done. Build the other tables from the TODO list. Use the design you wrote in Part A.

### Part C: Prove the SCD (30 min)
1. Insert a menu item row into `dim_menu_item` by hand with `valid_from` in May, `valid_to` in June, price 3500.
2. Insert the new current row at 4000.
3. Write a query that returns which row applies on 2026-06-01 and on 2026-07-01.

## Test cases
Run every test. Copy this table into `submissions/lab_02/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L2-T1 | Grain is written down | Open your SQL file. | A comment above every fact table saying 'One row = ...'. | | |
| L2-T2 | History query works | Insert two Jollof Rice price rows (May 3,500; June onward 4,000). Query the price valid on 2026-06-01 and on 2026-07-01. | The two dates return different prices. | | |
| L2-T3 | Only one current row | Query for items with more than one `is_current = 1` row. | Zero rows returned. | | |
| L2-T4 | No overlapping validity | Query for two rows of the same item whose date ranges overlap. | Zero rows returned. | | |
| L2-T5 | Grain mistake is understood | Using three orders and five lines, compute average wait per order and per line. | Two different numbers, and a sentence saying which is correct and why. | | |
| L2-T6 | Role-playing dimension | Show how one staff dimension serves waiter, chef and bartender. | `fact_order` has three staff keys pointing to `dim_staff`. | | |
| L2-T7 | Every question has a join path | For each of the four manager questions, write the tables and joins you would use. | All four are answerable from your schema with joins only (no subqueries on raw tables). | | |


## Deliverables
All four go in `submissions/lab_02/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** `warehouse/01_create_gold_schema.sql` completed; A diagram image of your star schema; The SCD history query and its output. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: The manager's four questions, the star schema that answers them, and the grain of each fact, in one page someone else could use to write a query.

## Reflection questions
1. Which table grows fastest, and which barely grows?
2. Why did we choose Type 2 for menu prices? Would you choose it for a table number?
3. What goes wrong if `actual_wait_min` sits on the order-line fact?
4. What did your AI assistant get wrong about Fabric Warehouse SQL, if anything?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

