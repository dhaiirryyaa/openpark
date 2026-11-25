# API Specification: Smart EV Slot Reservation Endpoints

## `POST /api/v1/ev/reserve`
Reserves an EV charging bay with power delivery requirements.

### Payload
```json
{
  "lot_id": "lot-indiranagar-01",
  "charger_type": "CCS2_60KW",
  "target_soc": 80
}
```
