# Geocoding API Endpoints

### GET `/api/geocode`
Unified multi-provider geocoding proxy:
- Providers: Google Maps Geocoding, Ola Maps API, OpenStreetMap Nominatim.
- Fallback: Local landmark catalog with fuzzy string matching.
