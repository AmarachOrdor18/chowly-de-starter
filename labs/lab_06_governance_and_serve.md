# Lab 6 (Days 9 and 10): Govern the data and serve it to the app

**Time:** Parts A and B on Day 9 (practice block, 60 min). Part C on Day 10 (90 min). Splitting it keeps Day 10 for building.

## Business context
Chowly's waiters must only see their own orders, the dashboard app must not hold an admin password, and the manager needs a screen she can read in 30 seconds. Right now everything is open, and nothing is shown to the manager.

## Objective
Document ownership, give the app a read-only identity, restrict rows per waiter, and show three tiles in the Manager role, fed only by Gold.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Least privilege and service principals in plain words
- Row-level security (check the current Fabric Warehouse documentation for the exact syntax)
- Environment variables and keeping secrets out of Git
- Caching API results

## Steps
### Part A: Governance register (30 min)
Fill in `docs/governance_register.md` with one row per Gold table: owner (a role, not a person's name), sensitivity (public, internal, confidential), who may read it, refresh frequency, and description of each column in one line. This doubles as your data dictionary.

### Part B: Security (30 min)
1. Create a **read-only** identity for the app (a service principal, guided by your instructor).
2. Give it access to the Gold warehouse only. Not to Bronze. Not to the workspace admin role.
3. Store its secret in an environment variable. Never commit it.
4. Row-level security: create a rule so that a login mapped to a waiter can only see rows for their own orders. Prove it with two test queries.

### Part C: Serve the app (60 min)
Using `analytics_api/main.py` as a guide, add a Manager role to your app and build three tiles:
1. Revenue by day
2. Average actual vs estimated wait per chef
3. Complaints and average rating for delayed vs on-time orders


### Part D: Serve aggregates, not raw data (Day 10 demo, 10 min)
Your instructor times the same dashboard query against (a) the raw scale fact table and (b) a small pre-aggregated Gold table, and records both in `scale_benchmark_log`. Write two sentences: why does the app only query Gold?

## Test cases
Run every test. Copy this table into `submissions/lab_06/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L6-T1 | Register is complete | Open `docs/governance_register.md`. | Every Gold table has an owner role, sensitivity, readers, refresh and column descriptions. | | |
| L6-T2 | Least privilege | With the app's identity, try to read a Gold table and then a Bronze table. | Gold works. Bronze is denied. | | |
| L6-T3 | Row-level security | Run the same query as waiter A and waiter B. | Each sees only their own rows, and the two counts add up to the total. | | |
| L6-T4 | No secrets in Git | Search your history: `git log -p | grep -iE "password|secret|mongodb\+srv|postgresql://"`. | No hits. `.env` is ignored. | | |
| L6-T5 | API fails gracefully | Use a wrong credential or stop access. | The API returns a 503 message and the app shows 'data unavailable', not a crash. | | |
| L6-T6 | Tiles match the truth | Compare the three tiles with a direct query on Gold. | Numbers are identical. | | |
| L6-T7 | Cache works | Request the same tile twice within a minute. | The warehouse is queried once. | | |
| L6-T8 | Serve aggregates | Time a query on the raw scale fact and on a small aggregate table. | Two rows in `scale_benchmark_log`, and two sentences on why the app queries only Gold. | | |


## Deliverables
All four go in `submissions/lab_06/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** `docs/governance_register.md`; RLS SQL, the API code and the code for the three tiles; Output of the git secret search. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: How the manager dashboard is fed, who can see what, and what to do if a tile looks wrong or stops updating.

## Reflection questions
1. Who owns each Gold table and what does that person have to decide?
2. Why enforce row access in the database and not only in the app?
3. What secret could still leak in your project?
4. Why does the dashboard read aggregates and not raw rows?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

