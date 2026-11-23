from backend.validators.geocoding_validator import sanitize_geocoding_query

def test_sanitize_query():
    valid, clean = sanitize_geocoding_query("  MG Road, Bengaluru! <script> ")
    assert valid is True
    assert "<script>" not in clean
    assert "MG Road" in clean
