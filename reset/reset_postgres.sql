-- Wipes the reference source database. Afterwards re-run app_changes/reference_schema.postgres.sql
-- and then: python data_generator/load_sources.py --only postgres
-- Run the trigger block at the bottom of the reference schema again after loading.
DROP SCHEMA IF EXISTS chowly CASCADE;
DROP SCHEMA IF EXISTS chowly_scale CASCADE;
