# Microservice Topology & Service Boundaries

OpenPark employs modular service isolation within a consolidated ASGI runtime:
- **`ai_copilot.py`**: Heuristic intent classification and local entity recognition.
- **`ai_parking_scanner.py`**: Spatial radius search and temporal bay occupancy estimation.
- **`iiot_service.py`**: Hardware telemetry simulation and sensor state caching.
- **`supabase_service.py`**: Cloud database sync, PostGIS spatial queries, and auth token validation.
- **`traccar_service.py`**: GPS protocol gateway for mobile vehicle tracking.
