# API Specification: Dynamic Circadian Surge Endpoints

## `GET /api/v1/surge/multiplier`
Returns active pricing multiplier for given coordinates and hour.

### Response
```json
{
  "hour": 9.5,
  "multiplier": 1.65,
  "status": "PEAK"
}
```
