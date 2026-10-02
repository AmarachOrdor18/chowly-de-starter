-- Lab 2: build the Gold star schema in your Fabric WAREHOUSE (wh_chowly).
-- Fabric Warehouse notes: use VARCHAR (not NVARCHAR), DATETIME2(6), and primary keys must be declared
--   PRIMARY KEY NONCLUSTERED ... NOT ENFORCED  (they document the design, the engine does not check them).
-- Run in the Warehouse query editor, one block at a time.

CREATE SCHEMA gold;
GO

-- ONE example dimension, done for you -------------------------------------------------
CREATE TABLE gold.dim_date (
    date_key      INT          NOT NULL,   -- 20260714, a smart key that reads well
    full_date     DATE         NOT NULL,
    day_name      VARCHAR(10)  NOT NULL,
    day_of_week   INT          NOT NULL,
    is_weekend    BIT          NOT NULL,
    month_no      INT          NOT NULL,
    month_name    VARCHAR(10)  NOT NULL,
    year_no       INT          NOT NULL,
    is_holiday    BIT          NOT NULL,
    holiday_name  VARCHAR(80)  NULL
);
ALTER TABLE gold.dim_date ADD CONSTRAINT pk_dim_date PRIMARY KEY NONCLUSTERED (date_key) NOT ENFORCED;
GO

-- TODO 1: dim_menu_item   (SCD Type 2)
--   surrogate key item_key, business key item_id, item_name, category, list_price, prep_minutes,
--   valid_from, valid_to, is_current
-- TODO 2: dim_staff       (SCD Type 2)   surrogate key staff_key, staff_id, full_name, role, valid_from, valid_to, is_current
-- TODO 3: dim_table       table_key, table_no

-- TODO 4: fact_order_item   GRAIN: one row per item line on an order
--   keys: date_key, item_key, waiter_key, chef_key, bartender_key, table_key, degenerate: order_id
--   measures: quantity, unit_price, line_amount, est_prep_minutes
-- TODO 5: fact_order        GRAIN: one row per order
--   measures: item_count, order_total, est_wait_min, actual_wait_min, is_delayed
-- TODO 6: fact_payment      GRAIN: one row per payment
--   measures: amount        attributes: method, is_simulated
-- TODO 7: fact_complaint    GRAIN: one row per complaint
--   measures: rating        attributes: complaint_text, channel

-- Write the grain of each fact in a comment above its CREATE TABLE. Your marks depend on it.
