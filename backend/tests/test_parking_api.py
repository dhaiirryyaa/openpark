import pytest

def test_parking_lot_schema():
    from backend.models.parking_lot import ParkingLotModel
    lot = ParkingLotModel(
        id=1, name="Test Lot", lat=12.97, lon=77.59,
        capacity=100, free_spots=40, price_car="₹40",
        price_bike="₹20", status="Available", address="MG Road"
    )
    assert lot.id == 1
    assert lot.free_spots == 40
    assert lot.status == "Available"
