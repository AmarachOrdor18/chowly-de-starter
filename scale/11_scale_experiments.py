# Notebook 11: scale experiments. Every number comes from timed(); nothing is typed in by hand.
# Fill in CAPACITY_NOTE once (what capacity and size your workspace uses). Run each experiment, then read the log.

# %%
import time, datetime
from pyspark.sql import functions as F

CAPACITY_NOTE = "TODO: e.g. trial capacity / F-SKU name, Spark pool size"     # fill this in honestly
CONFIG_NOTE   = "default Spark pool, no tuning"

def timed(experiment, operation, dataset, row_count, fn, notes=""):
    """Runs fn(), forces execution, logs wall-clock seconds to scale_benchmark_log."""
    t0 = time.time()
    fn()
    secs = round(time.time() - t0, 2)
    spark.createDataFrame([(datetime.datetime.now(), experiment, operation, dataset, int(row_count), float(secs),
                            CAPACITY_NOTE, CONFIG_NOTE, notes)],
        "run_at timestamp, experiment string, operation string, dataset string, row_count long, seconds double, capacity_note string, config_note string, notes string"
    ).write.format("delta").mode("append").saveAsTable("scale_benchmark_log")
    print(f"{experiment} | {operation} | {dataset} | {row_count:,} rows | {secs} s")
    return secs

def daily_revenue(orders, items):
    return (orders.join(items, "order_id")
                  .withColumn("amt", F.col("quantity") * F.col("unit_price"))
                  .groupBy("order_date").agg(F.sum("amt").alias("revenue"), F.countDistinct("order_id").alias("orders")))

# %% [markdown]
# ## Experiment 1: full reload vs incremental
# Full = aggregate every row. Incremental = aggregate only rows changed after the watermark.
# Question to answer before you run: how many rows do you expect the incremental run to touch?

# %%
DATASET = "s1m"     # change to s100k / s10m
o = spark.table(f"scale_orders_{DATASET}"); i = spark.table(f"scale_items_{DATASET}")
n = o.count()

timed("exp1_full_vs_incremental", "full aggregate", DATASET, n, lambda: daily_revenue(o, i).write.format("noop").mode("overwrite").save())

# watermark = keep roughly the newest 1 percent of rows
wm_row = o.select(F.expr("percentile_approx(unix_timestamp(updated_at), 0.99)").alias("wm")).collect()[0]["wm"]
o_new = o.filter(F.unix_timestamp("updated_at") > wm_row)
n_new = o_new.count()
print("rows above watermark:", n_new, "of", n)
timed("exp1_full_vs_incremental", "incremental aggregate (new rows only)", DATASET, n_new, lambda: daily_revenue(o_new, i).write.format("noop").mode("overwrite").save(),
      notes="filter on a non-partitioned column; see experiment 4")

# %% [markdown]
# ## Experiment 2: same transformation, growing data

# %%
for label in ["s100k", "s1m"]:               # add "s10m" if you built it
    o2 = spark.table(f"scale_orders_{label}"); i2 = spark.table(f"scale_items_{label}")
    timed("exp2_size", "daily revenue aggregate", label, o2.count(), lambda: daily_revenue(o2, i2).write.format("noop").mode("overwrite").save())

# %% [markdown]
# ## Experiment 3: SQL vs Spark
# Spark part runs here. The T-SQL part you run by hand in the lakehouse SQL analytics endpoint (or the warehouse),
# then record it with the cell below. Same question, both ways.
#
# T-SQL to run by hand (copy exactly):
#   SELECT order_date, SUM(i.quantity * i.unit_price) AS revenue
#   FROM scale_orders_s1m o JOIN scale_items_s1m i ON i.order_id = o.order_id GROUP BY order_date;

# %%
label = "s1m"
o3 = spark.table(f"scale_orders_{label}"); i3 = spark.table(f"scale_items_{label}")
timed("exp3_sql_vs_spark", "Spark DataFrame aggregate", label, o3.count(), lambda: daily_revenue(o3, i3).write.format("noop").mode("overwrite").save())
o3.createOrReplaceTempView("o3v"); i3.createOrReplaceTempView("i3v")
timed("exp3_sql_vs_spark", "Spark SQL aggregate", label, o3.count(),
      lambda: spark.sql("SELECT order_date, SUM(i.quantity*i.unit_price) r FROM o3v o JOIN i3v i ON i.order_id=o.order_id GROUP BY order_date").write.format("noop").mode("overwrite").save(),
      notes="same engine as DataFrame version: expect a similar time")

# %%
# Record your by-hand T-SQL timing (seconds shown in the SQL editor). Leave seconds as None if you did not run it.
TSQL_SECONDS = None       # e.g. 4.2  <- only a number YOU observed
if TSQL_SECONDS is not None:
    spark.createDataFrame([(datetime.datetime.now(), "exp3_sql_vs_spark", "T-SQL aggregate in SQL endpoint", label, int(o3.count()), float(TSQL_SECONDS),
                            CAPACITY_NOTE, "SQL analytics endpoint", "measured by hand")],
        "run_at timestamp, experiment string, operation string, dataset string, row_count long, seconds double, capacity_note string, config_note string, notes string"
    ).write.format("delta").mode("append").saveAsTable("scale_benchmark_log")

# %% [markdown]
# ## Experiment 4: partitioning by date
# Same data, written two ways. Then ask the same question: one week of orders.

# %%
src = spark.table("scale_orders_s1m")
src.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("scale_orders_s1m_flat")
src.write.format("delta").mode("overwrite").option("overwriteSchema", "true").partitionBy("order_date").saveAsTable("scale_orders_s1m_by_date")
for t in ["scale_orders_s1m_flat", "scale_orders_s1m_by_date"]:
    d = spark.sql(f"DESCRIBE DETAIL {t}").select("numFiles", "sizeInBytes").collect()[0]
    print(t, "files:", d["numFiles"], "bytes:", d["sizeInBytes"])

# pick a week that exists in the data
start = src.agg(F.min("order_date")).collect()[0][0]
wk_from, wk_to = start + datetime.timedelta(days=100), start + datetime.timedelta(days=107)

for t in ["scale_orders_s1m_flat", "scale_orders_s1m_by_date"]:
    df = spark.table(t).filter((F.col("order_date") >= F.lit(wk_from)) & (F.col("order_date") < F.lit(wk_to)))
    timed("exp4_partitioning", "count one week", t, df.count(), lambda: df.groupBy("order_date").count().write.format("noop").mode("overwrite").save())

# %%
display(spark.table("scale_benchmark_log").orderBy("run_at"))
