-- Reset the Gold layer in wh_chowly. Drops the tables, then the schema.
-- Re-create with warehouse/01_create_gold_schema.sql (your version) or the instructor solution.
DROP TABLE IF EXISTS gold.fact_weather_daily;
DROP TABLE IF EXISTS gold.fact_complaint;
DROP TABLE IF EXISTS gold.fact_payment;
DROP TABLE IF EXISTS gold.fact_order_item;
DROP TABLE IF EXISTS gold.fact_order;
DROP TABLE IF EXISTS gold.dim_table;
DROP TABLE IF EXISTS gold.dim_staff;
DROP TABLE IF EXISTS gold.dim_menu_item;
DROP TABLE IF EXISTS gold.dim_date;
DROP TABLE IF EXISTS gold.etl_watermark;
DROP TABLE IF EXISTS gold.dq_log;
DROP SCHEMA IF EXISTS gold;
