# Real-Time Synchronization Protocols

OpenPark uses Supabase Realtime (Postgres WAL CDC) to stream row updates:
- Table: `parking_lots`
- Event: `UPDATE` (column: `free_spots`, `status`)
- Client: Native EventSource / WebSocket connection with auto-reconnection and exponential backoff.
