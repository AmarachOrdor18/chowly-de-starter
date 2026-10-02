# Lab 7 (Day 7): What happens when Chowly gets big?

**Time:** 75 minutes in class. Day 6 started this with an instructor demo of Experiment 1.

## Business context
Chowly is opening more branches. The nightly job that took a short time last month takes longer every week, and the manager asks whether it will still finish before breakfast when there are ten times as many orders.

## Objective
Measure how the same work behaves at different sizes, compare full and incremental processing, SQL and Spark, and flat and partitioned tables, and explain what you saw.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Parallelism and distributed processing in plain words (one waiter vs ten)
- Partitioning by date
- What a Spark job does when you press run

## Steps
### The rule
You record only numbers you measured. Every timing is written to `scale_benchmark_log` by the `timed()` helper. If you could not run something, write `NOT VERIFIED`.

### Part A: Build the datasets (15 min)
Run `scale/10_scale_setup.py`. Start with `s100k` and `s1m`. Only add `s10m` if your session is comfortable. Write the row counts in `docs/scale_notes.md`.

### Part B: Predict before you measure (5 min)
In `docs/scale_notes.md`, before running anything, write one line for each:
1. 10x the rows: will the time be about 10x, less, or more? Why?
2. Incremental run on 1 percent of rows: how much faster?
3. Partitioning by date and asking for one week: what should improve?

### Part C: Run the experiments (40 min)
Run `scale/11_scale_experiments.py` section by section:
1. Full reload vs incremental
2. Same transformation at 100K and 1M (and 10M if built)
3. Spark vs SQL (run the T-SQL by hand in the SQL analytics endpoint and record its time)
4. Partitioning: flat vs by date

### Part D: Explain (15 min)
Answer in `docs/scale_notes.md`:
1. Which of your predictions were wrong? Why?
2. Where did the time grow with the data, and where did it not?
3. Did incremental help? What did you have to be true for it to help?
4. In one paragraph: what would change in Chowly at 100 million orders? (You do not have to run it.)

## Test cases
Run every test. Copy this table into `submissions/lab_07/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L7-T1 | Datasets exist | List the `scale_*` tables and their counts. | At least `s100k` and `s1m`, with counts close to the targets. | | |
| L7-T2 | Prediction first | Check the Git history of `docs/scale_notes.md`. | Predictions were committed before results. | | |
| L7-T3 | Every run is logged | Query `scale_benchmark_log`. | Rows for experiments 1 to 4, each with dataset, row count, seconds and your capacity note filled in. | | |
| L7-T4 | Only measured numbers | Compare each number in your notes with the log. | Every number in the notes is in the log. Anything untested says NOT VERIFIED. | | |
| L7-T5 | Incremental touched fewer rows | Read the printed row counts from Experiment 1. | The incremental run touched a small fraction of the rows, and you can say how small. | | |
| L7-T6 | SQL vs Spark recorded | Check for your by-hand T-SQL timing. | Either a logged T-SQL time or an honest NOT VERIFIED. | | |
| L7-T7 | Partitioning observed | Compare `DESCRIBE DETAIL` for the flat and partitioned tables. | File counts recorded for both; you described what they show. | | |
| L7-T8 | Rebuild is safe | Run the setup notebook again. | Tables are replaced, not doubled. | | |


## Deliverables
All four go in `submissions/lab_07/` in your repo. Details and templates: `docs/04_deliverables_guide.md`.

1. **Export (the blueprint).** The notebooks as you ran them (`10_scale_setup`, `11_scale_experiments`); An export of `scale_benchmark_log` as CSV; `docs/scale_notes.md`. Commit the real files. A screenshot alone does not count.
2. **Video (Loom, three minutes at most).** Answer four things out loud: *Why did we build this? What went wrong? How did you fix it?* Then run it and show the output.
3. **Reflection sheet.** `reflection.md`, answering the questions below in your own words.
4. **One-pager.** `one_pager.md` from `templates/one_pager_template.md`. Focus: For the operations lead: what we measured, at which sizes, on which capacity, and what we would do before the next branch opens.

## Reflection questions
1. Which prediction was most wrong and why?
2. When did doing less work (incremental, partitioned) not help?
3. When is SQL enough and when do you want Spark?
4. What changes at 100 million orders? Mark what you did not test as NOT VERIFIED.

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

