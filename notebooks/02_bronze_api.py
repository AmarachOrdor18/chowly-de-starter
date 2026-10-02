# Notebook 02: land API data into Bronze.
# APIs change and fail. Land the raw response, keep the request details, and have a fallback.

# %%
import json, requests
from datetime import datetime
from pyspark.sql import functions as F

LAT, LON = 6.5244, 3.3792     # Lagos
START, END = "2026-05-01", "2026-08-31"

# %% [markdown]
# ### Weather (Open-Meteo, no API key). Check the current docs before class: https://open-meteo.com/en/docs/historical-weather-api

# %%
url = ("https://archive-api.open-meteo.com/v1/archive"
       f"?latitude={LAT}&longitude={LON}&start_date={START}&end_date={END}"
       "&daily=temperature_2m_max,precipitation_sum&timezone=Africa%2FLagos")
try:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    source = "open-meteo-live"
except Exception as e:
    print("API failed, using the fallback file:", e)
    payload = None
    source = "fallback-file"

# %%
if payload:
    d = payload["daily"]
    rows = [(t, float(tmax) if tmax is not None else None, float(p) if p is not None else None)
            for t, tmax, p in zip(d["time"], d["temperature_2m_max"], d["precipitation_sum"])]
else:
    raw = json.load(open("/lakehouse/default/Files/landing/weather_daily.json"))
    rows = [(k, v["temp_max_c"], v["rain_mm"]) for k, v in raw.items()]

weather = spark.createDataFrame(rows, "date string, temp_max_c double, rain_mm double")
weather = (weather.withColumn("_ingested_at", F.current_timestamp())
                  .withColumn("_source", F.lit(source)))
weather.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("bronze_weather_daily")
print(source, weather.count(), "rows")

# %% [markdown]
# ### Public holidays (Nager.Date, no key): https://date.nager.at/api/v3/PublicHolidays/2026/NG

# %%
# TODO: call the holidays endpoint, land the raw list as bronze_holidays with the same metadata columns.
#       If the call fails, fall back to Files/landing/holidays.json.
