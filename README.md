# OpenPark 🅿️

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![MapLibre GL](https://img.shields.io/badge/MapLibre%20GL%20JS-4.7-396afc.svg)](https://maplibre.org/maplibre-gl-js/docs/API/)
[![SQLite FTS5](https://img.shields.io/badge/SQLite-FTS5%20Overture%20India-003B57.svg)](https://www.sqlite.org/fts5.html)
[![Tests](https://img.shields.io/badge/Tests-85%2F85%20Passing-success.svg)](backend/tests/)
[![Release](https://img.shields.io/badge/Release-v2.8.0-blueviolet.svg)](docs/RELEASE_NOTES_v2.7.0.md)
[![Commits](https://img.shields.io/badge/Commits-665%2B-informational.svg)](https://github.com/dhaiirryyaa/openpark/commits/main)

**OpenPark** is an open-source, next-generation smart mobility, urban parking discovery, 1 km AI small-ground scanner, India place search, and real-time GPS telemetry platform built with **FastAPI** and **MapLibre GL JS**. It provides sub-second parking discovery, OSRM turn-by-turn routing, Apple-grade luxury vector motion animations, circadian surge pricing, smart EV slot scheduling, and IoT barrier gate control.

---

## 🚀 Live Deployment & URLs

- **Driver Web App**: [https://openpark-web-production.up.railway.app/app/](https://openpark-web-production.up.railway.app/app/)
- **Operator Touch Dashboard**: [https://openpark-web-production.up.railway.app/dashboard/](https://openpark-web-production.up.railway.app/dashboard/)
- **Interactive API Docs (Swagger)**: [https://openpark-web-production.up.railway.app/docs](https://openpark-web-production.up.railway.app/docs)
- **Container**: `docker build -t openpark . && docker run -p 8000:8000 openpark`

---

## 🌟 Core Features & Architecture (v2.7.0)

### 1. 💎 Apple-Grade Luxury Vector Motion & UI Glassmorphism
- **Poised Living Markers**: Parking bay badges remain solidly anchored to real-world coordinates with dark glass styling (`backdrop-filter: blur(12px)`) and spring-loaded hover lift (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Find My Style Sonar Radars**: Status dots emit calm, hairline telemetry waves (`.fable-sonar-ring`) with exponential opacity decay.
- **Specular 3D Destination Beacon**: Realistic ground contact shadow (`.fable-ground-shadow`), expanding ground aperture wave (`.fable-ground-wave`), and metallic specular gloss drop pin (`#applePinSpecular`).
- **iOS Fluid Touch Glass Ripple**: Map taps emit an optical glass diffusion ring (`.fable-map-shockwave`) that dissipates in 0.52s.
- **iOS Control Center Sheet**: Interactive pull-down control center with gesture handling for 1-tap neighborhood selection and quick head-outs.
- **Route Energy Gliding Stream**: Luminous photon beam (`.fable-route-orb`) gliding along active navigation paths towards destinations.

### 2. ⚡ Algorithmic Computing Suite (`backend/algorithms/`)
- **Dynamic Traffic-Weighted ETA**: Adjusts travel times based on time-of-day corridor congestion decay (`dynamic_eta.py`).
- **Circadian Surge Pricing**: Dual-peak Gaussian pricing curve modeling morning (09:30) and evening (18:30) urban rush hours (`circadian_surge.py`).
- **Smart EV Slot Scheduling**: Power delivery optimizer matching battery capacity, arrival SoC, and charger kW (`ev_slot_scheduler.py`).
- **Spatial Hash Grid Engine**: O(1) grid cell hashing for sub-millisecond k-nearest neighbor parking lookups (`spatial_hash_grid.py`).
- **Markov-Chain Occupancy Simulation**: Stochastic arrival/departure probability modeling for predictive vacancy forecasting (`occupancy_markov.py`).
- **IoT Barrier Gate FSM**: Complete finite state machine (`IDLE`, `OPENING`, `OPEN`, `CLOSING`, `FAULT`) for automated gate access (`barrier_gate_fsm.py`).
- **Valet Dispatch Optimizer**: Nearest-neighbor driver assignment for automated vehicle drop-off (`valet_dispatch.py`).
- **Greenhouse Gas CO2 Offset Tracker**: Calculates emission grams avoided by eliminating cruising search time (`co2_savings.py`).

### 3. 🔍 Unified 1 km AI Small-Ground Scanner (`/api/ai/scan-parking`)
- Strictly scoped to a `<= 1 km` radius around the searched destination or user location.
- Identifies small unused pockets (`45–550 m²`, ~3–6 cars), mall plazas, and legal surface bays using local OSM/Overpass caches plus fast CGImap and Photon enrichment.
- Supports crowd verification (`✅ Parkable` / `🚫 Blocked`) via `POST /api/ai/verify-pocket`.

### 4. 🇮🇳 India-Scoped Offline & Live Place Search (`/api/places/search`)
- Full-text SQLite FTS5 index (`backend/places_db.py`) hydrated on startup from [data/overture_places_openpark.json.gz](data/overture_places_openpark.json.gz) and constrained to the India bounding box (`6.5 <= lat <= 37.5`, `68.0 <= lon <= 97.5`).
- Multi-provider fallback support across Photon, Ola Maps, Mappls, and Overpass.

### 5. 🗺️ MapLibre GL JS Basemaps & Overlays
- High-performance vector engine defaulting to **Google Maps Satellite Hybrid** with instant 1-tap switcher to **GMap Retina Road**.
- Offline vector grid fallback style for zero-connectivity environments.
- Autonomous Service Worker (`app/sw.js`) precaching core mobility assets for offline PWA launch.

### 6. ⏱️ 15-Minute Spot Holds & Operator Dashboard (`dashboard/index.html`)
- Pre-seeded Bengaluru parking dataset (`data/bengaluru_parking_opencity.json`).
- 15-minute spot reservations (`POST /lots/{lot_id}/hold`, `DELETE /lots/{lot_id}/hold`) with `OP-*` pass codes, plus live crowd reporting (`POST /lots/{lot_id}/reports`).
- Dedicated operator touch dashboard (`/dashboard/`) with live WebSocket broadcasts (`/ws/lots/{lot_id}`).

### 7. 🛰️ OSRM Navigation & Traccar GPS Telemetry
- Turn-by-turn routes (`/api/traccar/route`) and alternative corridor comparison (`/api/traccar/routes/compare`).
- OsmAnd / Traccar HTTP telemetry ingestion (`GET` & `POST /api/traccar`) and WebSocket live vehicle updates (`/ws/vehicle`).
- Smooth heading interpolation via exponential moving average filter (`app/js/utils/heading_filter.js`).

---

## 🔌 Verified API Endpoints Reference

### Smart Parking & AI Scanner
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/lots` | List all loaded parking facilities |
| `GET` | `/lots/nearby` | Parking lots strictly within `<= 1 km` (`radius_m` capped at `1000`) |
| `GET` | `/lots/{lot_id}` | Single lot details and real-time bay availability |
| `GET` | `/lots/{lot_id}/telemetry` | Multi-zone occupancy, EV, and heuristic telemetry |
| `POST` | `/lots/{lot_id}/hold` | Reserve a 15-minute hold and issue an `OP-*` entry pass |
| `DELETE` | `/lots/{lot_id}/hold` | Release an active hold |
| `POST` | `/lots/{lot_id}/reports` | Submit crowd report (`got_spot`, `has_space`, `lot_full`) |
| `POST` | `/lots/{lot_id}/availability` | Operator availability update (requires `X-API-Key`) |
| `GET` | `/api/ai/scan-parking` | Scan `<= 1 km` for 45–550 m² small grounds, malls, and bays |
| `POST` | `/api/ai/verify-pocket` | Vote `open` or `blocked` on an AI-detected pocket |
| `GET` | `/api/ai/verified-pockets` | List crowd-verified pocket votes |

### Places, Routing, Overpass & Telemetry
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/places/search` | India-scoped SQLite FTS5 + Photon search |
| `GET` | `/api/places/nearby` | Spatial Haversine nearby POI lookup |
| `GET` | `/api/places/stats` | Indexed places counts and top categories |
| `GET` | `/api/osm/overpass` | OSM parking outlines, fuel stations, and toll booths |
| `GET` | `/api/traccar/route` | OSRM driving route geometry and turn-by-turn steps |
| `GET` | `/api/traccar/routes/compare` | Compare fastest vs alternative driving routes |
| `GET` / `POST` | `/api/traccar` | Ingest OsmAnd / Traccar HTTP GPS fixes |
| `GET` | `/api/geolocate` | Approximate IP geolocation |
| `GET` | `/api/config/public` | Public frontend runtime config & map style defaults |
| `GET` | `/health` & `/health/details` | Service health and dataset diagnostics |
| `WS` | `/ws/lots/{lot_id}`, `/ws/vehicle`, `/api/socket` | Real-time lot availability and vehicle position streams |

---

## 📚 Architecture Decision Records (ADRs)

Key architectural decisions are documented in [`docs/architecture/`](docs/architecture/):
- **[ADR-001: SQLite FTS5 for India Geocoding](docs/architecture/c4_model.md)**
- **[ADR-002: Service Worker Offline-First Strategy](docs/architecture/offline_capabilities.md)**
- **[ADR-003: Ephemeral GPS Telemetry Processing](docs/architecture/data_flow.md)**
- **[ADR-004: Multi-Provider Proxy Resilience](docs/architecture/resilience_and_fallbacks.md)**
- **[ADR-005: Apple-Grade Luxury Vector Motion Architecture](docs/architecture/adr_005_luxury_motion.md)**
- **[ADR-006: Spatial Hash Grid Indexing vs R-Tree](docs/architecture/adr_006_spatial_indexing.md)**
- **[ADR-007: Circadian Surge Pricing Mathematical Curve](docs/architecture/adr_007_circadian_surge.md)**

---

## 🚀 Quickstart (Local Development)

### 1. Create Environment & Install Dependencies
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r requirements.txt
```

### 2. Optional Environment Variables
Copy `.env.example` to `.env` and add optional keys (`OPENPARK_API_KEY`, `OLAMAPS_API_KEY`, `OUTSCRAPER_API_KEY`, `MAPPLS_CLIENT_ID`, `MAPPLS_CLIENT_SECRET`, `DATABASE_URL`, `REDIS_URL`) if needed. Zero paid keys are required to run core search, routing, and parking discovery.

### 3. Run the Server
```bash
./backend/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- Driver Web App: [http://localhost:8000/app/](http://localhost:8000/app/)
- Operator Dashboard: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Automated Testing

Run the complete 75-test FastAPI & algorithm suite:
```bash
./backend/venv/bin/pytest backend/test_api.py backend/tests/ -v
```

---

## 🔒 Privacy & License

- **Ephemeral Vehicle Telemetry**: Real-time vehicle positions sent via WebSockets or `/api/traccar` remain in memory only during active sessions.
- **License**: [Apache-2.0 License](LICENSE).
- **Map & Place Data**: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), [Overture Maps Foundation](https://overturemaps.org/), and [MapLibre](https://maplibre.org/).
