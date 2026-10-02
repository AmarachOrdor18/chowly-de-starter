# Capstone: engineer three new features

## Business context
Chowly is growing. The owner has just approved two more branches and asks the analytics team for three new capabilities before the second branch opens. Each one needs data from somewhere new, a pipeline that does not break, numbers the owner can trust, and a screen in the Chowly app. The owner has seen too many dashboards that were wrong and nobody knew. She will only accept features that can show where their numbers come from, what happens when data goes bad, and what happens at ten times the volume.

The four source features you built on Day 2 (SQL, NoSQL, files, API) are prerequisites, not capstone features. They created the data. The platform you built on Days 3 to 10 is what you use now.

## Objective
Take three new business features all the way through the platform:

```
SOURCE > INGEST > BRONZE > SILVER > GOLD > QUALITY > GOVERNANCE > API > CHOWLY MANAGER DASHBOARD
```

Work alone or in pairs. Pairs build three features from different menu letters and add one more of their own choice.

## What "engineer a feature" means
Every feature must show all nine of these. A feature missing any of them counts as unfinished.

| # | Requirement |
|---|---|
| 1 | The business question in one sentence, and who asks it |
| 2 | Source(s). Across your three features, at least one uses a file source and at least one uses the API source |
| 3 | What changes in the model: new column, table or dimension. Grain stated |
| 4 | The pipeline or notebook change, and whether it is incremental |
| 5 | At least two quality rules for the new data, with quarantine |
| 6 | Governance: owner, sensitivity, who may read it |
| 7 | The API endpoint and the app screen |
| 8 | A test: a query that proves the number is right |
| 9 | Scale: answer in writing "What would change if this feature had 100 million records?" (volume, partitioning, incremental, serving). Add one measured number from `scale_benchmark_log` if your capacity allowed a test. If you could not test it, write NOT VERIFIED. Never write a number you did not measure |

## Feature menu
Pick from the menu or propose your own (your instructor must approve it).

**A. Smarter waiting time.** Replace the fixed estimated wait with the median actual wait for similar orders, by hour of week. Feed it back into the order screen. (This closes the loop from analytics back to the operational app.)

**B. Chef and bartender scorecard.** Estimated against actual prep time, delayed share and complaint rate for each staff member and shift, with a fair ranking.

**C. Supplier cost and margin watch.** Load the weekly supplier price files. Estimate ingredient cost per dish with a simple recipe table you create. Alert when margin on a dish falls under a threshold.

**D. Weather and holiday demand.** Show how drinks against food demand moves with temperature, rain and holidays. Add a next-day staffing suggestion.

**E. Complaint insights.** Classify complaint text into themes (slow service, wrong order, food quality, other) with simple rules. Show top themes by week and link each to delay or no delay.

**F. Stock alert.** Combine stock counts (JSON file) with sales to estimate days of stock left for each ingredient.

**G. Live kitchen board.** Use streaming events to show orders in progress and the current average wait, updating without a page refresh.

**H. Data health panel.** Last refresh time, rows rejected per table, and a plain-language lineage summary, for a non-technical manager.

**Stretch options (harder, and some Fabric details are version-sensitive, so check your instructor first):**

**I. Refresh button.** A "Refresh data" button on the Manager page that starts the pipeline and shows when it finished. It must handle two people pressing it at once.

**J. Quarantine review.** A screen where the manager sees rejected rows, approves or corrects them, and the corrected rows re-enter the pipeline. This is a human approval step inside a data pipeline.

**K. Supplier invoice reader.** Supplier invoices arrive as PDFs. Use an AI model to extract vendor, invoice number, dates and total into Bronze, and then quality-check and load them like any other source. You must handle a PDF the AI cannot read.

## Rules
- At least one feature must use streaming OR incremental loads with a watermark.
- Everything the dashboard shows comes from the Gold layer. No direct queries to the app database.
- Commit as you go. We will read the history.
- Never commit secrets.

## Test cases
These are required for **every** feature, in addition to your own number-proving test (requirement 8). Put results in `submissions/capstone/<feature letter>/tests.md`, with Result and Evidence.

| ID | Scenario | How to test | Expected result |
|---|---|---|---|
| C-T1 | Metric is right | Compute the headline number by hand from the source or Silver. | Dashboard, Gold and your hand calculation agree. |
| C-T2 | Rerun is safe | Run the pipeline twice in a row. | No duplicate rows, same counts. |
| C-T3 | Duplicate input | Feed the same source record twice. | One row in Gold. |
| C-T4 | Missing or empty data | Remove a field or send an empty file or response. | The bad row goes to quarantine with a reason, the rest loads. |
| C-T5 | Source failure | Make the source or API unavailable. | The pipeline reports it and the app shows a clear message. Nothing else breaks. |
| C-T6 | Late or changed data | Change an old source record. | The next run picks it up, and history in the dimension is preserved where it should be. |
| C-T7 | Wrong grain trap | Join your fact to a dimension that could multiply rows. | Row counts and totals do not inflate. |
| C-T8 | Access | Read the feature's table with the app's identity, then try a table it must not read. | Allowed on the Gold table, denied on Bronze. |
| C-T9 | Refresh or trigger | Start the update the way the owner would (schedule, button or event). Do it several times. | It behaves the same each time. |
| C-T10 | Scale reasoning | Read your answer to requirement 9. | It names what changes at 100 million records and marks untested claims NOT VERIFIED. |

## Deliverables
All four are required, per feature, in `submissions/capstone/<feature letter>/`, plus one set for the whole project.

1. **Export (the blueprint).** Pipelines, notebooks, SQL, API and app code, committed. Also `design.md`: the nine requirements for each feature, the architecture diagram, the star schema with grains, the data quality report, the lineage screenshot and the governance register.
2. **Video (Loom, ten minutes for the whole project).** Why did we build these? What went wrong? How did you fix it? Then run it: show each feature, the lineage, and one quality rule catching a bad row.
3. **Reflection sheet.** Answer these:
   1. What was the hardest decision, and what did you choose and why?
   2. Which test failed first, and what did it teach you?
   3. What would break first at 100 million records?
   4. Where was your AI assistant wrong, and how did you catch it? (Add the entries to `ai_log.md`.)
   5. What would you do differently if you started again?
4. **One-pager for the owner.** What each feature tells her, how to read the dashboard, what the data health panel means, and what to do when a tile looks wrong. Written for a non-technical reader.

## Demo day (Day 12)
Ten minutes each. Use the four prompts: **Why? What issues occurred? How did you fix it? Run it and see the output.** Then answer one question from the class: "What would break first at 100 million records, and what would you change?"

## Marking
| Area | Marks |
|---|---|
| Features work end to end | 25 |
| Test cases run, honest results, evidence | 15 |
| Modelling quality (grain, SCD, no double counting) | 10 |
| Pipeline quality (incremental, safe reruns, ETL vs ELT choices, scale reasoning) | 15 |
| Data quality and governance evidence | 10 |
| App design and clarity of the dashboard | 5 |
| Video, reflection and one-pager | 10 |
| AI log honesty and depth | 5 |
| Demo and explanation | 5 |
| **Total** | **100** |
