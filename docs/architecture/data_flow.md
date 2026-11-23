# Real-Time Telemetry & Data Flow

```
[ IIoT Sensors / Gates ]
          |
          v (HTTP / MQTT)
[ OpenPark Backend API ]
          |
          +---> [ Local SQLite / Cache ]
          |
          +---> [ Supabase PostGIS DB ] ---> [ Realtime Channels ]
                                                      |
                                                      v
                                            [ Client PWA Web App ]
```

Events are ingested at `<50ms` latency and broadcast via WebSocket subscriptions to connected drivers.
