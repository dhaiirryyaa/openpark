# Geospatial Indexing & PostGIS Spatial Queries

Parking lots and roadside bays are indexed using `ST_DWithin` and `ST_DistanceSphere`:
- Coordinate Reference System: `EPSG:4326` (WGS 84).
- Spatial Indexes: GIST on `geom` columns for sub-millisecond bounding box lookups.
- Fallback Haversine: Pure Python vectorized Haversine for edge-mode computation without spatial database.
