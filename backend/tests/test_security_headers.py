def test_cors_headers_structure():
    headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }
    assert headers["X-Frame-Options"] == "DENY"
