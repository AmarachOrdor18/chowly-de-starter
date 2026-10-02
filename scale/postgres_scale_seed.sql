-- Day 1 demo and scale source: make the OPERATIONAL database big, inside Postgres, with no external files.
-- Runs in a separate schema so your real data is untouched.
-- Change :n (rows) to try different sizes. Start with 1,000,000.
-- Record how long each step takes in scale/dry_run notes. Do not guess.

CREATE SCHEMA IF NOT EXISTS chowly_scale;

DROP TABLE IF EXISTS chowly_scale.orders_big;
CREATE TABLE chowly_scale.orders_big AS
SELECT
  g                                                     AS order_id,
  1 + (g % 15)                                          AS table_no,
  1 + (g % 4)                                           AS waiter_id,
  5 + (g % 3)                                           AS chef_id,
  (timestamp '2025-01-01 10:00:00'
     + ((g % 640) * interval '1 day')
     + ((g * 7919) % 43200) * interval '1 second')      AS placed_at,
  (1000 + ((g * 37) % 9000))::numeric(10,2)             AS order_total,
  10 + (g % 60)                                         AS estimated_wait_min
FROM generate_series(1, 1000000) AS g;      -- change 1000000 to try other sizes

ALTER TABLE chowly_scale.orders_big ADD COLUMN updated_at timestamp;
UPDATE chowly_scale.orders_big SET updated_at = placed_at + interval '30 minutes';
ALTER TABLE chowly_scale.orders_big ADD PRIMARY KEY (order_id);

-- THE DEMO QUERY. Run it with \timing on. While it runs, in a second session try inserting one order
-- and notice whether it is slowed down.
SELECT date_trunc('hour', placed_at) AS hour, COUNT(*) AS orders, SUM(order_total) AS revenue
FROM chowly_scale.orders_big
GROUP BY 1 ORDER BY 1;

-- Cleanup
-- DROP SCHEMA chowly_scale CASCADE;
