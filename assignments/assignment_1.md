# Assignment 1: Model it and land it (due Monday morning after Weekend 1)

Covers: entities and relationships, dimensional modelling, star schema, fact and dimension tables, SCDs, extraction, ETL vs ELT.

## Part 1: Modelling (40 marks)
Chowly's manager asks for a new report: **"For every waiter and every hour of the day, how many orders were late, and how much revenue did those late orders carry?"**

1. (5) Underline the measures and circle the dimensions in the question.
2. (10) Draw the star schema that answers it. Show every table with its keys.
3. (5) State the grain of your fact table in one sentence.
4. (10) The restaurant promotes waiter Tunde Bakare to "head waiter" in July. Explain what happens to June's report under SCD Type 1 and under SCD Type 2. Which would you choose and why?
5. (10) Someone proposes adding `actual_wait_min` to `fact_order_item` instead of `fact_order`. Show with a small example (3 orders, 5 lines) how this gives a wrong average wait.

## Part 2: Extraction (30 marks)
6. (10) Fill this table for the Chowly sources: source, type (SQL, NoSQL, file, API), how often it changes, ETL or ELT, and one reason.
7. (10) The weather API is down when your nightly job runs. Describe what your pipeline does, in three steps.
8. (10) Your pipeline reads the whole orders table every night. There are now 5 million orders. Describe the problem and the fix in your own words. (Day 5 gave you the idea of a bookmark. The professional name for it, the watermark, is used in Day 6. Using either word is fine.)

## Part 3: Build (30 marks)
9. (20) Show your Bronze tables (screenshot with row counts) and explain one thing you noticed about the raw data that would break a report if left as it is.
10. (10) AI log: paste one prompt you gave your AI tool for this assignment, what it returned, and what you changed.

## Submit
A folder `assignments/assignment_1/` in your repo with `answers.md`, a diagram image, and screenshots.
