# Database Schema Migrations

OpenPark uses declarative schema files stored in `backend/schema.sql` and Supabase SQL Editor.
To apply changes to Postgres:
```sql
ALTER TABLE parking_lots ADD COLUMN IF NOT EXISTS is_covered BOOLEAN DEFAULT FALSE;
```
