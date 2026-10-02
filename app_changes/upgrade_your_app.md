# Class 2, Part B: make your Chowly app analytics ready

**Do Part A first: `source_features.md`.** It adds the NoSQL, file and API features and the Manager role.

Your app was built to run a restaurant. Analytics needs it to also **remember**. You will make five changes to YOUR OWN app.
The reference SQL in `reference_schema.postgres.sql` shows the target. Your table and column names will differ. Adapt, do not copy blindly.
Use your AI assistant, and log the prompts and what you accepted or rejected.

## The five changes

### 1. A timestamp at every status change
Add `placed_at`, `served_at`, `paid_at` to orders. Set each one in the code path that changes the status, using the server clock.
Why: waiting time is `served_at - placed_at`. Without these, the question "how long did the customer wait?" cannot be answered.
```sql
ALTER TABLE orders ADD COLUMN placed_at TIMESTAMP, ADD COLUMN served_at TIMESTAMP, ADD COLUMN paid_at TIMESTAMP;
UPDATE orders SET placed_at = created_at WHERE placed_at IS NULL;   -- backfill what you can
```

### 2. Snapshot price and prep time on the order line
Add `unit_price` and `est_prep_minutes` to order items and fill them at the moment the order is placed.
Why: if the menu price changes next week, last week's revenue must not change.

### 3. `updated_at` on every table, kept fresh automatically
```sql
ALTER TABLE orders ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT now();
-- then a trigger, as in reference_schema.postgres.sql (or set it in your ORM's save hook)
```
Why: pipelines load only what changed since last time, using `updated_at` as the bookmark (the watermark).

### 4. Emit an event on every status change
You built this in Part A (A2). Check it now against the timestamps from change 1: the `at` in each event must match the timestamp written on the order.
Why: events keep the full story of an order. The orders table only keeps the latest state.

### 5. Never overwrite a menu price
When a price changes, close the old row in `menu_price_history` (set `valid_to`) and insert a new one. Update the current price on `menu_items`.
Why: this is exactly what a Slowly Changing Dimension solves in the warehouse. If the app already loses history, the warehouse has nothing to preserve.

## Prove it works (Lab 1)
Place three orders in your app and take one all the way to paid. Then show:
1. A query that returns the actual wait time of your order
2. The event documents for that order in MongoDB, with times that agree with the SQL timestamps
3. What happens to an old order line when you change a menu price
