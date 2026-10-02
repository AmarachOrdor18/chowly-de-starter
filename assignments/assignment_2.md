# Assignment 2: Trust it and protect it (due the day after Weekend 2, before Day 11)

Covers: data profiling, validation, lineage, master data, ownership, security, metadata, governance.

## Part 1: Quality (40 marks)
You are given `sample_data/orders.csv` and `sample_data/order_items.csv` (do not clean them by hand).
1. (10) Profile both files with a notebook. Report duplicates, nulls, impossible values.
2. (15) Write eight validation rules as a table: rule name, table, condition, what happens to a failing row (reject, fix, or flag), and why.
3. (10) Implement them. Report how many rows each rule caught. Compare with your classmates. Why might two correct answers differ slightly?
4. (5) Explain in three sentences why rejected rows go to a quarantine table and not the bin.

## Part 2: Master data and lineage (25 marks)
5. (10) The roster contains "F. Alade" and the SQL table contains "Funke Alade". Describe your matching rule, then give one case where it would match the wrong people.
6. (15) A manager says: "The dashboard says revenue on 14 July was 210,000. My till says 195,000." Write the exact steps, table by table, that you would follow using lineage to find the cause.

## Part 3: Governance (35 marks)
7. (10) Produce a data owner register for the Gold tables.
8. (10) A new waiter should see only their own orders and complaints. Describe two ways to enforce this, and say which you built.
9. (10) List every secret in your project and where each one is stored. Any in git history? Show the check.
10. (5) AI log: one place the AI was wrong on this assignment and how you found out.
