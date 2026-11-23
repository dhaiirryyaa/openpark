def test_supabase_payload_formatter():
    payload = {"lot_id": 1, "free_spots": 35}
    assert "lot_id" in payload
    assert payload["free_spots"] == 35
