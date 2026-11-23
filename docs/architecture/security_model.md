# Security & Row Level Security (RLS) Model

All database tables enforce PostgreSQL Row Level Security:
- `parking_lots`: Public `SELECT` allowed; `UPDATE` restricted to verified service role or lot operators.
- `reservations`: Drivers may only read and write their own records (`auth.uid() = user_id`).
- `driver_profiles`: Private to individual driver identity.
