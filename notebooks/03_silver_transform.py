# Notebook 03: Bronze -> Silver. Clean, type, dedupe, validate. Bad rows go to quarantine, not the bin.

# %%
from pyspark.sql import functions as F, Window

# %% [markdown]
# ### Pattern for every table
# 1. read bronze  2. cast types  3. dedupe (keep the latest by updated_at)  4. split good / bad  5. write silver + quarantine

# %%
def split_valid(df, rules):
    """rules: list of (rule_name, condition_that_means_the_row_is_GOOD).
    Returns (good_rows, bad_rows). Bad rows carry the list of rules they broke."""
    # a rule that evaluates to NULL (for example quantity is NULL) counts as FAILED
    failed = F.array(*[F.when(~F.coalesce(cond, F.lit(False)), F.lit(name)) for name, cond in rules])
    df = df.withColumn("_failed_rules", F.filter(failed, lambda x: x.isNotNull()))
    good = df.filter(F.size("_failed_rules") == 0).drop("_failed_rules")
    bad = df.filter(F.size("_failed_rules") > 0)
    return good, bad

# %% [markdown]
# ### Worked example: orders

# %%
o = spark.table("bronze_orders")          # loaded from Postgres by your pipeline in Lab 3
o = (o.withColumn("order_id", F.col("order_id").cast("int"))
      .withColumn("placed_at", F.to_timestamp("placed_at"))
      .withColumn("served_at", F.to_timestamp("served_at"))
      .withColumn("paid_at", F.to_timestamp("paid_at"))
      .withColumn("updated_at", F.to_timestamp("updated_at")))

w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
o = o.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")     # dedupe

rules = [
    ("served_before_placed", F.col("served_at").isNull() | (F.col("served_at") >= F.col("placed_at"))),
    ("paid_without_timestamp", (F.col("status") != "PAID") | F.col("paid_at").isNotNull()),
]
good, bad = split_valid(o, rules)
good.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_orders")
bad.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("quarantine_orders")
print("silver:", good.count(), "quarantined:", bad.count())

# %% [markdown]
# ### Your turn (Lab 4)
# Do the same for order_items, payments and complaints. Rules to implement:
# - order_items: quantity > 0, unit_price > 0, order_id exists in silver_orders
# - payments: order_id exists in silver_orders, amount > 0
# - complaints: rating between 1 and 5, order_id exists
# - orders: a food order must have a chef (you need order_items to know if it has food)

# %%
# TODO order_items

# %%
# TODO payments

# %%
# TODO complaints (flatten the nested meta field: meta.table_no, meta.channel)
