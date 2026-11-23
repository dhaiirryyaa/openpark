from datetime import datetime
from backend.models.telemetry_event import TelemetryEventModel

def test_telemetry_event_creation():
    event = TelemetryEventModel(
        lot_id=101, sensor_id="SN-01", event_type="enter",
        timestamp=datetime.utcnow(), free_spots=55, occupancy_pct=45.0
    )
    assert event.lot_id == 101
    assert event.event_type == "enter"
