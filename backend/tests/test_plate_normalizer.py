from backend.algorithms.plate_normalizer import normalize_indian_plate, is_valid_plate_format

def test_plate_normalizer():
    assert normalize_indian_plate('ka-01 ab 1234') == 'KA01AB1234'
    assert is_valid_plate_format('KA01AB1234') is True
    assert is_valid_plate_format('INVALID') is False
