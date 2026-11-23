# Multi-Tier Caching & Persistence Strategy

1. **L1 In-Memory LRU Cache**: Hot parking lot metadata and sensor readings cached in FastAPI memory.
2. **L2 Local Database**: SQLite database persistent across container reboots.
3. **L3 Browser CacheStorage**: Service Worker Cache API storing tiles, app shell, and geojson catalogs.
4. **L4 LocalStorage**: Driver preferences, bookmarks, and API credentials.
