# Fault Tolerance & Graceful Fallbacks

- **External Maps API Downtime**: Falls back from Google Places to OpenStreetMap Overpass, then to internal curated catalog.
- **Network Loss**: Service Worker transparently serves cached UI shell and synthetic offline sensor updates.
- **Telemetry Hardware Dropout**: Predictive temporal model estimates spot decay rate based on historical day-of-week trends.
