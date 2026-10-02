# Lab 1 (Days 2 and 3): Build the four sources, make the app remember, audit the OLTP

**Time:** about 3 hours of work. Start on Day 2 in class. The first 45 minutes of Day 3 is a clinic to finish and pass the checkpoint.

## Business context
The manager at Chowly asks two questions she cannot get answered today: did slow service cause the bad reviews, and does the weather change what we sell? The app keeps complaints as table rows, takes no supplier files, knows nothing about weather, and forgets old prices. Before any analytics is possible, the app itself has to produce the right kinds of data and stop forgetting.

## Objective
Add SQL, NoSQL, file and API data sources to Chowly, make the app keep history, and show that a heavy question cannot be answered well from the live database.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- What MongoDB documents and collections are, compared with tables
- How file uploads work in your web framework, and why you must not trust an uploaded file
- How to call a REST API with a timeout, and how to cache the answer
- What a database trigger is (for `updated_at`)

## Steps
Tip: if you can, start Part A2 (MongoDB) on the evening of Day 1. Atlas signup is the slowest part.

### Part A: Build the source features (`app_changes/source_features.md`)
| Step | Feature | Suggested time |
|---|---|---|
| A1 | Manager role and staff table | 15 min |
| A2 | Complaints and events to MongoDB | 45 min |
| A3 | Supplier price and staff roster uploads | 45 min |
| A4 | "Today at Chowly" API banner | 40 min |

### Part B: Make the app analytics ready (`app_changes/upgrade_your_app.md`)
Five changes: timestamps, price snapshot on the order line, `updated_at`, events (already done in A2, just verify), price history.

### Part C: Stand up the reference source systems
Your app is new and has almost no history. Follow `docs/02_source_systems_setup.md` to create the reference Postgres schema and load four months of history into Postgres and MongoDB. Your Fabric pipelines in Lab 3 will read from these.
(Your own app's live data becomes an extra source you can plug in during the capstone.)

### Part D: Audit the OLTP system
Run this against the reference Postgres, with timing on:
```sql
SELECT date_trunc('hour', placed_at) AS hour, COUNT(*) AS orders
FROM chowly.orders GROUP BY 1 ORDER BY 1;
```
In `docs/oltp_audit.md` answer:
1. How long did it take? What would happen if 50 waiters were saving orders at the same moment?
2. List three questions a manager would ask that this database cannot answer well. Say why.
3. Which of your four sources was hardest to build? What broke?
4. For each of your four sources, write one way it can fail (SQL, NoSQL, file, API). You will need this on Day 5.

### Checkpoint (start of Day 3)
Show your instructor:
- A complaint document in Atlas, and four events for one order
- `supplier_prices_2026-05-04.csv` and `staff_roster.xlsx` uploaded, with two `file_uploads` rows
- The "Today at Chowly" banner with real weather, and the app still working with the internet off
- A query returning the actual wait of one order

## Test cases
Run every test. Copy this table into `submissions/lab_01/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L1-T1 | Complaint reaches MongoDB | Submit a complaint with a rating in the app. | One document in `complaints` with the fields in the contract, including the nested `meta` object. | | |
| L1-T2 | Order event trail | Take one order from placed to paid. | Four documents in `order_events` (PLACED, ASSIGNED, SERVED, PAID) in time order, and each time agrees with the timestamp on the order in SQL. | | |
| L1-T3 | Uploaded file stays untouched | Upload `supplier_prices_2026-05-04.csv`. Compare its checksum with the original. | Checksums are identical. The file is stored under the filename contract. | | |
| L1-T4 | Bad uploads are refused | Try a `.pdf` as the roster, an empty CSV, and a file over your size limit. | All three are refused with a clear message and create no `file_uploads` row. | | |
| L1-T5 | Upload is logged | Upload the roster Excel file. | A row in `file_uploads` with file name, type, role, time, size and path. | | |
| L1-T6 | API failure does not break ordering | Turn off your internet, reload the Manager page, and place an order. | The banner says weather is unavailable, `source_status` is not `ok`, and the order still works. | | |
| L1-T7 | API answer is cached | Load the Manager page five times in a minute and check your logs. | One outbound call to each API, not five. | | |
| L1-T8 | Orphan complaint | Submit a complaint for order id 999999. | Your app refuses it, or stores it flagged. Write down which you chose and why. (You will meet this again on Day 8.) | | |
| L1-T9 | Price history survives | Change a menu price after an order exists. | The old order line still shows the old `unit_price`, and `menu_price_history` has two rows for that item. | | |
| L1-T10 | Wait time is computable | Run a query for one order: `served_at - placed_at`. | A sensible number of minutes, no NULLs for a served order. | | |
| L1-T11 | Reference sources loaded | Follow `docs/02_source_systems_setup.md`, then count rows. | Postgres: staff 9, menu_items 24, menu_price_history 27, orders 3,839, order_items 12,004, payments 3,804. MongoDB: complaints 276, order_events 15,216. | | |
| L1-T12 | OLTP audit | Run the hourly orders query from Part D with timing on. | You recorded a time and answered the four audit questions in `docs/oltp_audit.md`. | | |


## Deliverables
All four go in `submissions/lab_01/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** Commit links for: migration SQL, the code for A1 to A4, the `file_uploads` and `daily_context` table definitions; `.env.example` (never the real `.env`); Screenshots: a Mongo complaint, four events, two uploads, the banner. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: What data Chowly now produces, where each kind lives, how a manager uploads a file, and what the banner means when it says 'unavailable'.

## Reflection questions
1. Which of the four sources was hardest to build, and what broke?
2. In SQL, a foreign key stopped a complaint for a missing order. What stops it now, and what did you choose?
3. Why must the app store the uploaded file untouched instead of cleaning it?
4. What would the manager still be unable to answer after today, and why?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

