from chatbot.chatbot import get_chatbot_response, detect_crisis

def test_normal_response():
    response = get_chatbot_response("I am feeling happy today")
    assert "great" in response.lower() or "happy" in response.lower()

def test_crisis_detection():
    crisis_messages = [
        "I want to kill myself",
        "I feel hopeless and want to die",
        "I'm thinking about self harm"
    ]
    for msg in crisis_messages:
        is_crisis, _ = detect_crisis(msg)
        assert is_crisis == True

def test_emergency_response():
    response = get_chatbot_response("I want to end it all")
    assert "🛑" in response
    assert "AASRA" in response