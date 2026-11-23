# Parking API Endpoints

### GET `/api/parking/lots`
Retrieves nearby parking lots within a radius.
- **Parameters**: `lat` (float), `lon` (float), `radius_km` (float, default: 5.0)
- **Response**: Array of `ParkingLot` objects with real-time bay availability.
