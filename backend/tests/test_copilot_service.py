from backend.models.copilot_query import CopilotQueryModel

def test_copilot_query_model():
    q = CopilotQueryModel(
        prompt="parking near church street",
        user_lat=12.975, user_lon=77.605,
        detected_intent="find_parking",
        target_categories=["commercial", "garage"]
    )
    assert "church street" in q.prompt
    assert q.detected_intent == "find_parking"
