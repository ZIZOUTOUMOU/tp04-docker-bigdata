import os
import time
import pandas as pd

DATA_DIR = os.getenv("DATA_DIR", "/app/data")
DATA_FILE = os.getenv("DATA_FILE", "sample.csv")
CHUNK = int(os.getenv("CHUNK_SIZE", "1000000"))
path = os.path.join(DATA_DIR, DATA_FILE)
if not os.path.exists(path):
    raise SystemExit(f"File not found: {path}. Did you mount the data folder?")
print(f"Reading in chunks of {CHUNK:,} rows: {path}")

cols = ["event_time", "event_type", "category_code", "brand", "price", "user_id"]
types = {"event_type": "category", "category_code": "string", "brand": "string",
         "price": "float64", "user_id": "int64"}

total_events = 0
raw_rows = 0
purchases_count = 0
revenue = 0.0
users = set()
by_type = pd.Series(dtype="int64")
brand_rev = pd.Series(dtype="float64")
cat_rev = pd.Series(dtype="float64")
hour_purch = pd.Series(dtype="int64")

start = time.time()
for i, chunk in enumerate(pd.read_csv(path, usecols=cols, dtype=types,
                                      chunksize=CHUNK, encoding="utf-8-sig"), 1):
    raw_rows += len(chunk)
    # Cleaning (same logic as TP03 in Power Query)
    chunk["event_type"] = chunk["event_type"].astype("string")
    chunk["brand"] = chunk["brand"].fillna("unknown")
    chunk["category_code"] = chunk["category_code"].fillna("unknown")
    chunk["main_category"] = chunk["category_code"].str.split(".").str[0]
    chunk = chunk[chunk["price"] > 0].drop_duplicates()

    # Running totals
    total_events += len(chunk)
    users.update(chunk["user_id"].unique())
    by_type = by_type.add(chunk["event_type"].value_counts(), fill_value=0)

    p = chunk[chunk["event_type"] == "purchase"]
    purchases_count += len(p)
    revenue += p["price"].sum()
    brand_rev = brand_rev.add(p.groupby("brand")["price"].sum(), fill_value=0)
    cat_rev = cat_rev.add(p.groupby("main_category")["price"].sum(), fill_value=0)
    hours = pd.to_datetime(p["event_time"].str.replace(" UTC", "", regex=False)).dt.hour
    hour_purch = hour_purch.add(hours.value_counts(), fill_value=0)

    print(f"  chunk {i}: {raw_rows:,} rows read ({time.time() - start:.0f}s)", flush=True)

print(f"\nRaw rows: {raw_rows:,} | Clean rows: {total_events:,}")
print("\n=== KPIs ===")
print("Total events :", total_events)
print("Unique users :", len(users))
print("Purchases    :", purchases_count)
print("Revenue      :", round(revenue, 2))
print("Conversion % :", round(100 * purchases_count / total_events, 2))

print("\n=== Events by type ===")
print(by_type.astype(int).sort_values(ascending=False))

print("\n=== Top 10 brands by revenue ===")
print(brand_rev.sort_values(ascending=False).head(10).round(2))

print("\n=== Revenue by main category ===")
print(cat_rev.sort_values(ascending=False).round(2))

print("\n=== Purchases per hour ===")
print(hour_purch.astype(int).sort_index())

print(f"\nDone in {time.time() - start:.0f}s")
