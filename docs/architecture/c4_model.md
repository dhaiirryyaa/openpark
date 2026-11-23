# OpenPark C4 Architecture Model

## Level 1: System Context
- **Users**: Urban drivers seeking parking.
- **External Systems**: Google Maps Platform, Supabase Cloud, Traccar GPS.

## Level 2: Container Diagram
- **PWA Web App**: Single Page Application (MapLibre + Apple Glass UI).
- **Backend API**: Python FastAPI ASGI server.
- **Database**: PostgreSQL with PostGIS extension.
