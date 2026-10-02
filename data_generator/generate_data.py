"""
Chowly synthetic data generator.

Produces four months of realistic restaurant data across four source types:
  SQL-shaped CSVs : menu_items, menu_price_history, staff, orders, order_items, payments
  NoSQL JSONL     : complaints (nested documents), order_events
  Files           : supplier_prices_<week>.csv, staff_roster.xlsx (messy), stock_counts.json
  API fallback    : weather_daily.json, holidays.json (same shape as the live APIs)

A small share of rows is deliberately dirty. Each defect is written to an answer key
(instructors only). Same seed gives the same data for everyone.

Usage:
  python generate_data.py --out ../sample_data --seed 2026
  python generate_data.py --out ./out --start 2026-05-01 --end 2026-08-31 --dirty 0.03
"""
import argparse
import csv
import json
import math
import random
from datetime import date, datetime, timedelta
from pathlib import Path

FOOD = [
    ("Jollof Rice and Chicken", 3500, 20), ("Fried Rice and Turkey", 3800, 22),
    ("Egusi Soup and Pounded Yam", 4500, 30), ("Pepper Soup (Goat)", 3000, 18),
    ("Suya Platter", 4000, 25), ("Grilled Tilapia", 5500, 35),
    ("Ofada Rice and Stew", 4200, 28), ("Moi Moi", 1200, 15),
    ("Plantain and Eggs", 2000, 12), ("Beef Burger and Fries", 4800, 18),
    ("Chicken Shawarma", 3200, 12), ("Small Chops Platter", 3600, 15),
]
DRINKS = [
    ("Chapman", 1800, 5), ("Zobo", 1200, 3), ("Bottled Water", 500, 1),
    ("Soft Drink", 700, 1), ("Fresh Orange Juice", 1800, 6), ("Smoothie", 2500, 8),
    ("Palm Wine", 2000, 3), ("Draught Beer", 1500, 2), ("Red Wine Glass", 3500, 2),
    ("Mojito", 3800, 9), ("Iced Tea", 1500, 4), ("Coffee", 1600, 6),
]
HOT_DRINKS = {"Chapman", "Zobo", "Bottled Water", "Fresh Orange Juice", "Smoothie", "Iced Tea", "Mojito"}
STAFF = [
    (1, "Ngozi Eze", "waiter"), (2, "Tunde Bakare", "waiter"), (3, "Amina Sule", "waiter"),
    (4, "Chidi Okafor", "waiter"), (5, "Emeka Nwosu", "chef"), (6, "Bisi Adeyemi", "chef"),
    (7, "Yusuf Bello", "chef"), (8, "Kelechi Obi", "bartender"), (9, "Funke Alade", "bartender"),
]
# Price changes: (item name, effective date, new price)
PRICE_CHANGES = [
    ("Jollof Rice and Chicken", "2026-06-15", 4000),
    ("Chapman", "2026-07-01", 2000),
    ("Grilled Tilapia", "2026-07-20", 6000),
]
HOLIDAYS = {"2026-06-12": "Democracy Day", "2026-05-01": "Workers' Day", "2026-05-27": "Eid al-Adha (observed)"}


def iso(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./out")
    ap.add_argument("--answer-key", default=None, help="folder for the dirty-data answer key")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--start", default="2026-05-01")
    ap.add_argument("--end", default="2026-08-31")
    ap.add_argument("--dirty", type=float, default=0.03)
    a = ap.parse_args()

    rnd = random.Random(a.seed)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    key_dir = Path(a.answer_key) if a.answer_key else out / "_answer_key"
    key_dir.mkdir(parents=True, exist_ok=True)
    start, end = date.fromisoformat(a.start), date.fromisoformat(a.end)

    # ---------- menu ----------
    menu = []
    item_id = 1
    for cat, items in (("food", FOOD), ("drink", DRINKS)):
        for name, price, prep in items:
            menu.append({"item_id": item_id, "name": name, "category": cat, "price": price, "prep": prep})
            item_id += 1
    by_name = {m["name"]: m for m in menu}
    changes = sorted((by_name[n]["item_id"], date.fromisoformat(d), p) for n, d, p in PRICE_CHANGES)

    def price_on(iid, d):
        p = next(m["price"] for m in menu if m["item_id"] == iid)
        for cid, cdate, cprice in changes:
            if cid == iid and d >= cdate:
                p = cprice
        return p

    # menu_items holds the CURRENT price (this is what a naive app stores)
    cur = {m["item_id"]: m["price"] for m in menu}
    for cid, _, cprice in changes:
        cur[cid] = cprice
    write_csv(out / "menu_items.csv", ["item_id", "name", "category", "price", "prep_minutes", "is_active", "updated_at"],
              [[m["item_id"], m["name"], m["category"], cur[m["item_id"]], m["prep"], 1, "2026-08-31 23:00:00"] for m in menu])
    hist = []
    for m in menu:
        first_from = a.start + " 00:00:00"
        my = [c for c in changes if c[0] == m["item_id"]]
        cur_price, cur_from = m["price"], first_from
        for _, cdate, cprice in my:
            hist.append([m["item_id"], cur_price, cur_from, cdate.isoformat() + " 00:00:00"])
            cur_price, cur_from = cprice, cdate.isoformat() + " 00:00:00"
        hist.append([m["item_id"], cur_price, cur_from, ""])
    write_csv(out / "menu_price_history.csv", ["item_id", "price", "valid_from", "valid_to"], hist)

    write_csv(out / "staff.csv", ["staff_id", "full_name", "role", "is_active", "updated_at"],
              [[s[0], s[1], s[2], 1, "2026-08-31 23:00:00"] for s in STAFF])

    # ---------- simulated weather and holidays (fallback for the API lab) ----------
    weather = {}
    d = start
    while d <= end:
        doy = d.timetuple().tm_yday
        base = 29 + 3 * math.sin((doy - 100) / 365 * 2 * math.pi)
        temp = round(base + rnd.uniform(-3, 3), 1)
        rain = round(max(0.0, rnd.gauss(4, 8)) if rnd.random() < 0.5 else 0.0, 1)
        weather[d.isoformat()] = {"temp_max_c": temp, "rain_mm": rain}
        d += timedelta(days=1)
    (out / "weather_daily.json").write_text(json.dumps(weather, indent=1))
    (out / "holidays.json").write_text(json.dumps(
        [{"date": k, "name": v, "countryCode": "NG"} for k, v in HOLIDAYS.items()], indent=1))

    # ---------- orders ----------
    waiters = [s for s in STAFF if s[2] == "waiter"]
    chefs = [s for s in STAFF if s[2] == "chef"]
    bars = [s for s in STAFF if s[2] == "bartender"]
    food_items = [m for m in menu if m["category"] == "food"]
    drink_items = [m for m in menu if m["category"] == "drink"]

    orders, lines, payments, complaints, events = [], [], [], [], []
    oid = lid = pid = cid = eid = 0
    d = start
    while d <= end:
        wk = d.weekday()
        base = 26 if wk < 4 else (42 if wk in (4, 5) else 34)
        if d.isoformat() in HOLIDAYS:
            base = int(base * 0.6)
        w = weather[d.isoformat()]
        n = max(5, int(rnd.gauss(base, 5)))
        for _ in range(n):
            oid += 1
            hour = rnd.choices(range(11, 23), weights=[2, 5, 9, 8, 3, 2, 3, 6, 9, 8, 4, 2])[0]
            placed = datetime(d.year, d.month, d.day, hour, rnd.randint(0, 59), rnd.randint(0, 59))
            waiter = rnd.choice(waiters)
            n_food = rnd.choices([0, 1, 2, 3], weights=[10, 45, 30, 15])[0]
            n_drink = rnd.choices([0, 1, 2, 3], weights=[8, 40, 32, 20])[0]
            if n_food + n_drink == 0:
                n_drink = 1
            picks = []
            for _ in range(n_food):
                picks.append(rnd.choice(food_items))
            for _ in range(n_drink):
                hot_bias = w["temp_max_c"] > 31
                pool = [m for m in drink_items if (m["name"] in HOT_DRINKS) == hot_bias] if rnd.random() < 0.35 else drink_items
                picks.append(rnd.choice(pool or drink_items))
            has_food = any(p["category"] == "food" for p in picks)
            has_drink = any(p["category"] == "drink" for p in picks)
            chef = rnd.choice(chefs) if has_food else None
            bar = rnd.choice(bars) if has_drink else None
            est_food = max([p["prep"] for p in picks if p["category"] == "food"], default=0)
            est_drink = max([p["prep"] for p in picks if p["category"] == "drink"], default=0)
            est = max(est_food, est_drink) + 3 * max(0, len(picks) - 2)
            noise = max(0.6, rnd.gauss(1.05, 0.2))
            if chef and chef[1] == "Emeka Nwosu" and wk >= 4:
                noise *= 1.5            # hidden insight: Emeka is slow on Fri-Sun
            if hour in (13, 19, 20):
                noise *= 1.15           # rush hour
            if rnd.random() < 0.06:
                noise *= 2.6            # serious delay
            actual = max(3, round(est * noise))
            served = placed + timedelta(minutes=actual)
            paid_at = served + timedelta(minutes=rnd.randint(10, 60))
            total = 0
            for p in picks:
                lid += 1
                q = rnd.choices([1, 2, 3], weights=[75, 20, 5])[0]
                up = price_on(p["item_id"], d)
                total += q * up
                lines.append([lid, oid, p["item_id"], q, up, p["prep"], iso(placed)])
            orders.append({
                "order_id": oid, "table_no": rnd.randint(1, 15), "waiter_id": waiter[0],
                "chef_id": chef[0] if chef else "", "bartender_id": bar[0] if bar else "",
                "status": "PAID", "placed_at": iso(placed), "served_at": iso(served), "paid_at": iso(paid_at),
                "estimated_wait_min": est, "actual": actual, "updated_at": iso(paid_at), "total": total,
            })
            pid += 1
            payments.append([pid, oid, total, rnd.choices(["card", "cash", "transfer"], weights=[45, 30, 25])[0], 1, iso(paid_at), iso(paid_at)])
            # events (NoSQL): placed, assigned, served, paid
            for et, at, actor in (("PLACED", placed, "customer"), ("ASSIGNED", placed + timedelta(minutes=1), f"waiter:{waiter[0]}"),
                                  ("SERVED", served, f"waiter:{waiter[0]}"), ("PAID", paid_at, "customer")):
                eid += 1
                events.append({"event_id": eid, "order_id": oid, "event_type": et, "at": iso(at), "actor": actor})
            # complaints (NoSQL)
            ratio = actual / max(est, 1)
            p_c = 0.45 if ratio > 1.8 else (0.05 if ratio > 1.3 else 0.01)
            if rnd.random() < p_c:
                cid += 1
                rating = rnd.choice([1, 1, 2, 2, 3]) if ratio > 1.5 else rnd.choice([2, 3, 4])
                text = rnd.choice(["Waited far too long", "Food came cold", "Drinks were late", "Nobody told us about the delay",
                                   "Wrong order", "Great food but slow"]) if ratio > 1.3 else rnd.choice(["Portion was small", "Music too loud", "Table was sticky"])
                complaints.append({"complaint_id": cid, "order_id": oid, "rating": rating, "text": text,
                                   "created_at": iso(served + timedelta(minutes=rnd.randint(2, 20))),
                                   "meta": {"channel": "app", "table_no": orders[-1]["table_no"]}})
        d += timedelta(days=1)

    # ---------- inject dirt ----------
    key = []
    def mark(table, k, issue):
        key.append([table, k, issue])

    for o in rnd.sample(orders, int(len(orders) * a.dirty)):
        kind = rnd.choice(["served_before_placed", "paid_no_timestamp", "missing_chef", "dup"])
        if kind == "served_before_placed":
            dt = datetime.strptime(o["placed_at"], "%Y-%m-%d %H:%M:%S") - timedelta(minutes=rnd.randint(5, 30))
            o["served_at"] = iso(dt); mark("orders", o["order_id"], "served_at earlier than placed_at")
        elif kind == "paid_no_timestamp":
            o["paid_at"] = ""; mark("orders", o["order_id"], "status PAID but paid_at is empty")
        elif kind == "missing_chef" and o["chef_id"] != "":
            has_food = any(l[1] == o["order_id"] and l[2] <= len(FOOD) for l in lines)
            if has_food:
                o["chef_id"] = ""; mark("orders", o["order_id"], "food order with no chef")
        elif kind == "dup":
            orders.append(dict(o)); mark("orders", o["order_id"], "duplicate order row")
    for l in rnd.sample(lines, int(len(lines) * a.dirty)):
        if rnd.random() < 0.5:
            l[3] = rnd.choice([0, -1, -2]); mark("order_items", l[0], "quantity is zero or negative")
        else:
            l[4] = rnd.choice([0, ""]); mark("order_items", l[0], "unit_price is zero or missing")
    for p in rnd.sample(payments, int(len(payments) * a.dirty / 2)):
        p[1] = 900000 + p[0]; mark("payments", p[0], "payment points to an order that does not exist")
    for c in rnd.sample(complaints, max(1, int(len(complaints) * 0.08))):
        c["rating"] = rnd.choice([0, 7, 11, -1]); mark("complaints", c["complaint_id"], "rating outside 1 to 5")

    write_csv(out / "orders.csv",
              ["order_id", "table_no", "waiter_id", "chef_id", "bartender_id", "status", "placed_at", "served_at", "paid_at", "estimated_wait_min", "updated_at"],
              [[o["order_id"], o["table_no"], o["waiter_id"], o["chef_id"], o["bartender_id"], o["status"], o["placed_at"], o["served_at"], o["paid_at"], o["estimated_wait_min"], o["updated_at"]] for o in orders])
    write_csv(out / "order_items.csv", ["order_item_id", "order_id", "item_id", "quantity", "unit_price", "est_prep_minutes", "updated_at"], lines)
    write_csv(out / "payments.csv", ["payment_id", "order_id", "amount", "method", "is_simulated", "paid_at", "updated_at"], payments)
    for name, rows in (("complaints.jsonl", complaints), ("order_events.jsonl", events)):
        with open(out / name, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")

    # ---------- files: supplier prices (weekly), messy roster, stock counts ----------
    files_dir = out / "files"
    files_dir.mkdir(exist_ok=True)
    ingredients = [("Chicken (kg)", 3800), ("Rice (50kg bag)", 78000), ("Tilapia (kg)", 4200), ("Goat meat (kg)", 6500),
                   ("Palm oil (5L)", 9500), ("Tomatoes (basket)", 14000), ("Beef (kg)", 7200), ("Oranges (100)", 8000)]
    wk_start = start - timedelta(days=start.weekday())
    while wk_start <= end:
        rows = []
        for name, base in ingredients:
            drift = 1 + 0.0035 * ((wk_start - start).days // 7) + rnd.uniform(-0.03, 0.03)
            price = round(base * drift, -1)
            if rnd.random() < 0.03:
                price = "N/A"
            rows.append([name.upper() if rnd.random() < 0.15 else name, price, "NGN", "Mile12 Market"])
        write_csv(files_dir / f"supplier_prices_{wk_start.isoformat()}.csv", ["ingredient", "unit_price", "currency", "supplier"], rows)
        wk_start += timedelta(days=7)

    # messy roster: same people, different spellings, one role change, one stranger
    roster_rows = [
        ["Ngozi Eze", "Waiter", "2025-11-03", "08033000001"], ["Tunde  Bakare", "waiter", "2025-11-03", "08033000002"],
        ["AMINA SULE", "Waiter", "2026-01-12", "0803 300 0003"], ["Chidi Okafor", "Waiter", "2026-01-12", "08033000004"],
        ["Emeka Nwosu", "Chef", "2025-09-01", "08033000005"], ["Bisi Adeyemi", "Sous Chef", "2025-09-01", "08033000006"],
        ["Yusuf Bello", "chef", "2026-02-02", "08033000007"], ["Kelechi Obi", "Bartender", "2025-12-01", "08033000008"],
        ["F. Alade", "Bartender", "2025-12-01", "08033000009"], ["Seun Coker", "Cleaner", "2026-03-01", "08033000010"],
    ]
    try:
        from openpyxl import Workbook
        wb = Workbook(); ws = wb.active; ws.title = "Roster"
        ws.append(["Name", "Position", "Start date", "Phone"])
        for r in roster_rows:
            ws.append(r)
        wb.save(files_dir / "staff_roster.xlsx")
    except ImportError:
        write_csv(files_dir / "staff_roster.csv", ["Name", "Position", "Start date", "Phone"], roster_rows)
    stock = [{"counted_on": (end - timedelta(days=i * 7)).isoformat(),
              "items": [{"sku": n.split(" (")[0].lower().replace(" ", "_"), "on_hand": rnd.randint(2, 60), "unit": n.split("(")[-1].rstrip(")") if "(" in n else "unit"} for n, _ in ingredients]}
             for i in range(4)]
    (files_dir / "stock_counts.json").write_text(json.dumps(stock, indent=1))

    write_csv(key_dir / "dirty_answer_key.csv", ["table", "record_id", "issue"], key)
    print(f"orders={len(orders)} lines={len(lines)} payments={len(payments)} complaints={len(complaints)} events={len(events)} dirty={len(key)}")


if __name__ == "__main__":
    main()
