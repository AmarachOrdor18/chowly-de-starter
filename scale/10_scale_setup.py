# Notebook 10: build scale tables in the lakehouse by multiplying the clean Silver data.
# Needs silver_orders and silver_order_items from Lab 4. Change SIZES to try other sizes.
# Nothing here is a benchmark. Benchmarks are in notebook 11 and are always measured.

# %%
from pyspark.sql import functions as F
import time, datetime

SIZES = {"s100k": 100_000, "s1m": 1_000_000}      # add "s10m": 10_000_000 when ready
ORDER_ID_OFFSET = 10_000_000                        # keeps copies from colliding; raise it if you go above 10m
BASE_ORDERS = spark.table("silver_orders").select("order_id", "table_no", "waiter_id", "chef_id", "placed_at", "estimated_wait_min", "actual_wait_min", "updated_at")
BASE_ITEMS  = spark.table("silver_order_items").select("order_item_id", "order_id", "item_id", "quantity", "unit_price")
n_base = BASE_ORDERS.count()
print("base orders:", n_base)

# %%
def build(label, target_orders):
    copies = max(1, target_orders // n_base)
    k = spark.range(copies).withColumnRenamed("id", "copy")
    orders = (BASE_ORDERS.crossJoin(k)
        .withColumn("order_id", F.col("order_id") + F.col("copy") * ORDER_ID_OFFSET)
        .withColumn("placed_at", F.expr("placed_at + make_interval(0, 0, 0, cast(copy % 640 as int), 0, 0, 0)"))
        .withColumn("updated_at", F.expr("updated_at + make_interval(0, 0, 0, cast(copy % 640 as int), 0, 0, 0)"))
        .withColumn("order_date", F.to_date("placed_at"))
        .drop("copy"))
    items = (BASE_ITEMS.crossJoin(k)
        .withColumn("order_id", F.col("order_id") + F.col("copy") * ORDER_ID_OFFSET)
        .withColumn("order_item_id", F.col("order_item_id") + F.col("copy") * ORDER_ID_OFFSET * 10)
        .drop("copy"))
    t0 = time.time()
    orders.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"scale_orders_{label}")
    items.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"scale_items_{label}")
    dt = time.time() - t0
    print(label, "orders:", spark.table(f"scale_orders_{label}").count(), "items:", spark.table(f"scale_items_{label}").count(), "build seconds:", round(dt, 1))

for label, n in SIZES.items():
    build(label, n)

# %% [markdown]
# The logging table. Created once. Every experiment writes here.

# %%
spark.sql("""
CREATE TABLE IF NOT EXISTS scale_benchmark_log (
  run_at TIMESTAMP, experiment STRING, operation STRING, dataset STRING, row_count BIGINT,
  seconds DOUBLE, capacity_note STRING, config_note STRING, notes STRING)
USING DELTA
""")
