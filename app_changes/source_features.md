# Part A of Class 2: build the features that create the four source types

A data platform needs things to ingest. Right now your Chowly app produces only one kind of data: rows in a SQL database.
Before you make the app analytics ready, you will add four small features so that Chowly produces **SQL, NoSQL, file and API data**, the way a real restaurant system does.

These are **not** your capstone features. These four are the foundation. The capstone comes at the end and builds on top of them.

| # | Source type | The feature | Where the data lives |
|---|---|---|---|
| A1 | SQL | Orders, items, menu, staff, payments (you already have this) plus a Manager role | Your SQL database |
| A2 | NoSQL | Complaints, ratings and the order event log move to MongoDB | MongoDB Atlas |
| A3 | Files | The manager uploads the weekly supplier price list (CSV) and the staff roster (Excel) | An `uploads/` folder or storage bucket, plus a `file_uploads` table |
| A4 | API | "Today at Chowly": weather and public holiday, fetched from outside APIs | A daily snapshot table, plus a banner on the screen |

Use your AI assistant, and log it. Your stack is your choice.

---

## A1: SQL, plus the Manager role
You already store orders in SQL. Two things to add:
1. **A third role in your role switch: Manager.** (Customer, Waiter, Manager. No login needed, same simple switch as before.) The Manager screen will hold the upload page (A3), the "Today" banner (A4), and later the dashboard.
2. **A `staff` table with a `role` column** (waiter, chef, bartender) if you did not already have one.

**Done when:** you can switch to Manager and see an empty Manager page.

---

## A2: NoSQL, complaints and the event log
Complaints and ratings are free text with a flexible shape, and events are an append-only log. Both fit a document database better than a table.

**Build:**
1. Create a free MongoDB Atlas cluster (see `docs/00_prerequisites.md`). Put the connection string in `.env`.
2. When a customer submits a complaint and rating, the app writes **one document** to the `complaints` collection:
```json
{
  "complaint_id": 17,
  "order_id": 42,
  "rating": 2,
  "text": "Waited far too long",
  "created_at": "2026-09-30 13:20:05",
  "meta": { "channel": "app", "table_no": 7 }
}
```
3. Every time an order changes status (PLACED, ASSIGNED, SERVED, PAID) the app writes one document to the `order_events` collection:
```json
{ "event_id": 311, "order_id": 42, "event_type": "SERVED", "at": "2026-09-30 13:05:11", "actor": "waiter:3" }
```
4. The order details page now reads the complaint for that order **from MongoDB**.
5. Stop writing complaints to your SQL table. (Keep the old table if you like, but the app must use Mongo.)

**Think about it (you will meet this again on Day 8):** in SQL a foreign key stopped someone submitting a complaint for an order that does not exist. In MongoDB nothing stops that. Where in your code do you check that `order_id` is real?

**Done when:**
- Submit a complaint in the app and see the document in Atlas
- Take one order from placed to paid and see four event documents for it
- The order details page shows the complaint and rating from Mongo

---

## A3: Files, supplier prices and staff roster
Real restaurants run on spreadsheets. Somebody emails the supplier's price list. HR keeps the roster in Excel. These arrive as files, not as rows, and they are messy.

**Build (Manager role only):**
1. An upload page with two upload buttons:
   - **Supplier price list** (CSV)
   - **Staff roster** (Excel .xlsx)
2. The app saves the file **exactly as uploaded**. Do not clean it. Do not fix the column names. That is the data engineer's job later.
3. Filenames follow this **contract**, so a pipeline can find them:
   - `supplier_prices_YYYY-MM-DD.csv` where the date is the Monday of that week
   - `staff_roster.xlsx` (a new upload replaces the file, but keep the old ones in a `staff_roster_archive/` folder with the upload date in the name)
4. Every upload writes one row to a SQL table:
```
file_uploads (upload_id, file_name, file_type, uploaded_by_role, uploaded_at, size_bytes, storage_path)
```
5. The page lists past uploads from that table.
6. Basic guard rails only: wrong file type is refused, empty file is refused, files over a size limit are refused. Nothing else.
7. Bonus: also accept a `stock_counts.json` upload.

Use the sample files in `sample_data/files/` to test. They are deliberately messy.

**Done when:**
- You upload `supplier_prices_2026-05-04.csv` and `staff_roster.xlsx` and both appear in the storage folder unchanged
- Two rows appear in `file_uploads`
- A `.pdf` upload is refused

**Where do the files go next?** In Lab 3 you will move them into Fabric OneLake. In a real system you would store them in cloud storage (Azure Blob, ADLS or S3) and point a Fabric **shortcut** at that location so the files appear in the lakehouse without copying. Check the current Fabric docs for supported shortcut sources. For now a local folder is fine.

---

## A4: API, "Today at Chowly"
Sales depend on things outside the restaurant: heat, rain, public holidays. Your app will fetch these from two free public APIs.

**Build:**
1. A backend endpoint `GET /api/context/today` that calls:
   - **Weather:** Open-Meteo forecast API for Lagos (latitude 6.5244, longitude 3.3792), asking for today's maximum temperature and rainfall
   - **Holidays:** Nager.Date public holidays for Nigeria (`NG`) for the current year
   Check each provider's current docs for the exact URL and response shape.
2. The endpoint returns:
```json
{ "date": "2026-09-30", "temp_max_c": 31.2, "rain_mm": 0.0, "is_holiday": false, "holiday_name": null, "source_status": "ok" }
```
3. **Failure rules (this is the real lesson):**
   - Use a timeout of 5 seconds
   - Cache the answer for the day, so you do not call the API on every page load
   - If either API fails, return what you have with `source_status: "partial"` or `"unavailable"`. Never crash. Never block a customer from ordering
4. Save one row per day in a SQL table:
```
daily_context (context_date, temp_max_c, rain_mm, holiday_name, fetched_at, source_status)
```
5. Show a small banner on the Manager and Waiter screens: "Today: 31C, no rain, not a public holiday" or "Weather unavailable".

**Done when:**
- The banner shows real values
- Turn off your internet, reload, and the app still works and shows "unavailable"
- `daily_context` has a row for today

---

## Checkpoint (end of Day 3, first thing)
Show your instructor all four: a complaint in Atlas, four events for one order, two files uploaded with two `file_uploads` rows, and the banner with real weather. Commit everything.

Only then start Part B: `upgrade_your_app.md` (the five changes that make the app remember).

## Why this comes first
In the next ten days you will pull data from every one of these places: SQL, NoSQL, files, and APIs. If the app does not produce them, there is nothing real to ingest. And you will feel, from the app side, why each source type behaves differently.
