# OpenPark System Architecture

OpenPark is an autonomous urban mobility and parking intelligence platform.
It combines vector tile mapping, real-time IIoT telemetry, satellite vision verification,
and predictive AI occupancy modeling.

## Core Subsystems
1. **Spatial Vector Engine**: MapLibre GL JS client with Google Hybrid / Retina raster-tile fallback.
2. **IIoT Telemetry Gateway**: High-frequency bay occupancy events from physical ground sensors.
3. **AI Copilot & Vision Agent**: Natural language query resolver and satellite aerial verification.
4. **Cloud Database & PostGIS**: Supabase PostgreSQL with spatial geometry indices and Realtime pub/sub.
5. **Offline PWA Core**: Service Worker v2.0 enabling autonomous offline navigation.
