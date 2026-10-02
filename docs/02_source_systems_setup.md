# Source systems setup (Lab 1)

Your Chowly app is young and has almost no history. To practice data engineering you need months of data.
So you will create a **reference source database** and load generated history into it.

## Postgres
1. Create a database in your Postgres provider.
2. Run `app_changes/reference_schema.postgres.sql` against it.
3. Put the connection string in `.env` as `POSTGRES_DSN`.

## MongoDB Atlas
1. Create a free M0 cluster and a database user.
2. Put the connection string in `.env` as `MONGO_URI`.

## Load the history
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd data_generator
python load_sources.py --data ../sample_data
```
Expected counts: about 3,800 orders, 12,000 order lines, 3,800 payments, 270 complaints, 15,000 events.
These numbers are a little higher than the clean totals on purpose. Some rows are dirty. That is the point.

Then run the trigger block at the bottom of `reference_schema.postgres.sql`.

## Want your own data? Generate a fresh set
```bash
python generate_data.py --out ./my_data --seed 7 --dirty 0.05
```
Different seed, different history. Do not commit `my_data/` if it is large.

## Free API sources used later
- Weather: Open-Meteo (no key)
- Public holidays: Nager.Date (no key)
Both can change. If either fails, the notebooks fall back to files in `sample_data/`.
