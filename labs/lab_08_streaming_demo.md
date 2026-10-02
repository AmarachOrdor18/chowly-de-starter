# Lab 8 (Day 7 (last hour)): Streaming order events (guided demo)

## Business context
The kitchen manager wants to see how many orders are waiting right now and how long the last ten took, without waiting for tomorrow's report. A nightly batch cannot answer that.

## Objective
Follow a live demo that sends order events through an Eventstream into an Eventhouse and read two prepared queries.

## Learn first
Before you start, make sure you can explain each of these. Your instructor adds the current links after testing them.
- Batch versus streaming, the bus and the taxi
- What an event is

## Steps
Follow along with your instructor. Not graded, but you need it for the capstone options.

1. Create an **Eventstream** `es_orders` with a custom endpoint source.
2. Run `python stream_demo.py` (instructor supplies it) which sends order events every few seconds.
3. Send the stream to an **Eventhouse** (KQL database) `eh_chowly`.
4. In the KQL query editor, write a query that counts orders placed but not yet served, and the average wait of the last 10 served orders.
5. Discuss: which dashboard tiles need streaming, and which are fine with a nightly batch?

## Test cases
Run every test. Copy this table into `submissions/lab_08/tests.md` and fill in **Result** (PASS, FAIL, BLOCKED) and **Evidence** (a screenshot, query output or commit link). A test that fails is acceptable if you explain why and what you would do about it. A test you did not run must say NOT RUN.

| ID | Scenario | How to test | Expected result | Result | Evidence |
|---|---|---|---|---|---|
| L8-T1 | Events arrive | Start the sender and run the count query twice, ten seconds apart. | The count goes up. | | |
| L8-T2 | Stopping the sender stops the growth | Pause the sender and run the query twice. | The count does not change. | | |
| L8-T3 | Waiting count is right | Compare orders PLACED minus SERVED with your query. | They agree. | | |


## Deliverables (light, because this is a guided demo)
Put these in `submissions/lab_08/`:

1. **Export.** Screenshot of the Eventstream and Eventhouse; The two KQL queries you ran.
2. **Reflection sheet.** `reflection.md`, answering the questions below.

A video and a one-pager are not required for this lab.

## Reflection questions
1. Which Chowly dashboard tile really needs streaming and which does not?
2. What does streaming cost that batch does not?
3. What would happen to the live tile if the sender crashed?

## AI log
Add at least one entry to `ai_log.md` for this lab (template: `ai_log_template.md`), including one thing the AI got wrong or that you rejected.

## Done when
All test cases have a Result with evidence, the deliverables are committed, and nothing in your notes is a number you did not measure.

