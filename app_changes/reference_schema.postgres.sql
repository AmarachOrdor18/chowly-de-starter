-- Chowly reference source database (Postgres).
-- This is the "analytics ready" version of the Chowly model.
-- Class 2 has students upgrade THEIR OWN app to match these ideas.
-- Lab 1 loads history into THIS schema so everyone has the same source system to ingest from.

CREATE SCHEMA IF NOT EXISTS chowly;
SET search_path TO chowly;

-- Change 3: every table has updated_at, kept fresh by a trigger (powers incremental loads)
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS staff (
  staff_id    INT PRIMARY KEY,
  full_name   VARCHAR(100) NOT NULL,
  role        VARCHAR(20)  NOT NULL CHECK (role IN ('waiter','chef','bartender')),
  is_active   INT NOT NULL DEFAULT 1,
  updated_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS menu_items (
  item_id       INT PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  category      VARCHAR(10)  NOT NULL CHECK (category IN ('food','drink')),
  price         NUMERIC(10,2) NOT NULL,          -- CURRENT price only
  prep_minutes  INT NOT NULL,
  is_active     INT NOT NULL DEFAULT 1,
  updated_at    TIMESTAMP NOT NULL DEFAULT now()
);

-- Change 5: never lose old prices. The app (or a trigger) writes here whenever price changes.
CREATE TABLE IF NOT EXISTS menu_price_history (
  item_id     INT NOT NULL REFERENCES menu_items(item_id),
  price       NUMERIC(10,2) NOT NULL,
  valid_from  TIMESTAMP NOT NULL,
  valid_to    TIMESTAMP NULL,
  PRIMARY KEY (item_id, valid_from)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id            INT NOT NULL,   -- no primary key on purpose: the sample history contains duplicate rows the pipeline must catch
  table_no            INT NOT NULL,
  waiter_id           INT REFERENCES staff(staff_id),
  chef_id             INT REFERENCES staff(staff_id),
  bartender_id        INT REFERENCES staff(staff_id),
  status              VARCHAR(20) NOT NULL,       -- PLACED, ASSIGNED, SERVED, PAID
  -- Change 1: a timestamp for every status change
  placed_at           TIMESTAMP NOT NULL,
  served_at           TIMESTAMP NULL,
  paid_at             TIMESTAMP NULL,
  estimated_wait_min  INT NOT NULL,
  updated_at          TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id     INT PRIMARY KEY,
  order_id          INT NOT NULL,   -- loose on purpose in the raw layer; the warehouse must catch orphans
  item_id           INT NOT NULL,
  quantity          INT NOT NULL,
  -- Change 2: snapshot price and prep time on the line, so menu edits never rewrite history
  unit_price        NUMERIC(10,2),
  est_prep_minutes  INT,
  updated_at        TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payments (
  payment_id    INT PRIMARY KEY,
  order_id      INT NOT NULL,
  amount        NUMERIC(10,2) NOT NULL,
  method        VARCHAR(20) NOT NULL,
  is_simulated  INT NOT NULL DEFAULT 1,   -- payments are pretend, and labelled as such
  paid_at       TIMESTAMP NOT NULL,
  updated_at    TIMESTAMP NOT NULL DEFAULT now()
);

-- Triggers (created last so the bulk load in Lab 1 keeps the original updated_at values;
-- the loader script disables them by loading before they exist, then you run this block)
-- Run the block below AFTER load_sources.py has finished.
--
-- DO $$
-- DECLARE t text;
-- BEGIN
--   FOREACH t IN ARRAY ARRAY['staff','menu_items','orders','order_items','payments'] LOOP
--     EXECUTE format('CREATE TRIGGER trg_%s_updated BEFORE UPDATE ON chowly.%s
--                     FOR EACH ROW EXECUTE FUNCTION chowly.set_updated_at()', t, t);
--   END LOOP;
-- END $$;
