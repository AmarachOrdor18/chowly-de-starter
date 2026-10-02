# Notebook 01: land FILE sources into the Bronze layer of the lakehouse (ELT: load first, clean later)
# Attach your lakehouse (lh_chowly) as the default lakehouse before running.
# Upload the contents of sample_data/files to  Files/landing/files/  first.

# %% [markdown]
# ## Rule of Bronze: keep the data exactly as it arrived. Add only bookkeeping columns.

# %%
from pyspark.sql import functions as F

def add_meta(df, source_name):
    """Bookkeeping columns every Bronze table carries."""
    return (df.withColumn("_ingested_at", F.current_timestamp())
              .withColumn("_source", F.lit(source_name))
              .withColumn("_source_file", F.input_file_name()))

# %% [markdown]
# ### 1. Supplier prices (many weekly CSVs, one table)

# %%
supplier = (spark.read.option("header", True).option("inferSchema", False)
            .csv("Files/landing/files/supplier_prices_*.csv"))
supplier = add_meta(supplier, "files/supplier_prices")
supplier.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("bronze_supplier_prices")
print(spark.table("bronze_supplier_prices").count(), "rows")

# %% [markdown]
# ### 2. Stock counts (nested JSON). Keep it nested in Bronze. Flatten it in Silver.

# %%
stock = spark.read.option("multiLine", True).json("Files/landing/files/stock_counts.json")
stock = add_meta(stock, "files/stock_counts")
stock.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("bronze_stock_counts")
stock.printSchema()

# %% [markdown]
# ### 3. Staff roster (Excel): your turn
# Spark cannot read .xlsx directly. Two ways: (a) a Dataflow Gen2 (the ETL way), or (b) pandas.
# Pick one, land it as bronze_staff_roster, and write two lines in your notes on why you chose it.

# %%
# TODO: read Files/landing/files/staff_roster.xlsx into a Spark dataframe with pandas
#       (hint: pandas.read_excel with the local path /lakehouse/default/Files/landing/files/staff_roster.xlsx)
# TODO: add bookkeeping columns and save as bronze_staff_roster

# %% [markdown]
# ### 4. NoSQL exports landed as JSON lines (complaints, order_events)
# Your Data Factory pipeline (Lab 3) copies MongoDB collections into Files/landing/nosql/ as JSON.
# If the connector gives you trouble, upload sample_data/complaints.jsonl and order_events.jsonl there by hand.
# Bronze keeps the nested structure (meta.channel, meta.table_no) untouched.

# %%
for name in ["complaints", "order_events"]:
    df = spark.read.json(f"Files/landing/nosql/{name}*.json*")
    df = add_meta(df, f"mongo/{name}")
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"bronze_{name}")
    print(name, df.count(), "documents")
