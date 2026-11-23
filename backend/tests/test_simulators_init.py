from backend.simulators.ground_sensor_node import UltrasonicGroundSensor
from backend.simulators.boom_barrier_gate import BoomBarrierGate

def test_simulators():
    sensor = UltrasonicGroundSensor("B-01")
    reading = sensor.trigger_reading()
    assert reading["bay_id"] == "B-01"
    
    gate = BoomBarrierGate("G-IN")
    res = gate.process_vehicle_arrival("KA04MH9999")
    assert gate.barrier_open is True
    assert res["action"] == "barrier_opened"
