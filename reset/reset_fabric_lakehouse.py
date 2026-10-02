# Notebook: reset the lakehouse layers. Attach lh_chowly as the default lakehouse.
# This DROPS tables. Read the list it prints before you run the second cell.

# %%
PREFIXES = ("bronze_", "silver_", "quarantine_", "scale_")
KEEP = ("scale_benchmark_log",)        # keep your measurements unless you clear them on purpose
to_drop = [t.name for t in spark.catalog.listTables() if t.name.startswith(PREFIXES) and t.name not in KEEP]
print(len(to_drop), "tables will be dropped:")
for t in to_drop:
    print("  ", t)

# %%
CONFIRM = False          # change to True, then run this cell
if CONFIRM:
    for t in to_drop:
        spark.sql(f"DROP TABLE IF EXISTS {t}")
    print("done")
else:
    print("nothing dropped (CONFIRM is False)")
