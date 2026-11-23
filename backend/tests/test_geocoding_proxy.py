from backend.models.geocoding_result import GeocodingResultModel

def test_geocoding_model_instantiation():
    res = GeocodingResultModel(
        name="Indiranagar 100ft Rd",
        address="Bengaluru, Karnataka",
        lat=12.9784, lon=77.6408, category="commercial"
    )
    assert res.lat > 12.0
    assert res.lon > 77.0
