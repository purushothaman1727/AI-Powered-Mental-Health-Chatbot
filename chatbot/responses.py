from chatbot.model import detect_emotion

def get_supportive_response(user_message: str, detected_emotion: str = None):
    if not detected_emotion:
        detected_emotion, confidence = detect_emotion(user_message)
    else:
        confidence = 0.8

    message_lower = user_message.lower()

    # Emergency / Crisis Detection (detailed in Phase 12)
    crisis_keywords = ['suicide', 'kill myself', 'self harm', 'end it', 'hopeless', 'want to die']
    if any(kw in message_lower for kw in crisis_keywords):
        return {
            "response": "I'm really concerned about what you're going through. Please reach out to a professional immediately. Help is available 24/7.",
            "emotion": "crisis",
            "suggestion": "Emergency Helplines"
        }

    responses = {
        "sadness": "I'm sorry you're feeling down. It's okay to not be okay. Would you like to talk about it or try a quick breathing exercise?",
        "anger": "It sounds like you're frustrated. Take a moment to breathe. Remember, this feeling will pass.",
        "fear": "It's completely valid to feel scared. Let's ground ourselves: name 5 things you can see right now.",
        "joy": "That's wonderful to hear! Celebrate this moment. What made you feel this way?",
        "love": "Love is beautiful. Cherish those connections!",
        "surprise": "Wow, that sounds unexpected! How are you feeling about it?",
        "neutral": "I'm here to listen. What's on your mind today?"
    }

    base_response = responses.get(detected_emotion.lower(), responses["neutral"])

    # Add coping strategy
    coping = get_coping_strategy(detected_emotion)

    return {
        "response": f"{base_response} {coping}",
        "emotion": detected_emotion,
        "confidence": confidence,
        "suggestion": get_wellness_suggestion(detected_emotion)
    }

def get_coping_strategy(emotion):
    strategies = {
        "sadness": "Try the 4-7-8 breathing: Inhale for 4 seconds, hold for 7, exhale for 8.",
        "anger": "Progressive muscle relaxation can help release tension.",
        "fear": "Grounding technique 5-4-3-2-1 works wonders.",
        "neutral": "A short walk or journaling might help center you."
    }
    return strategies.get(emotion.lower(), "Take care of yourself today.")

def get_wellness_suggestion(emotion):
    # Can query Wellness_Activities table later
    return "Consider a short mindfulness activity or reaching out to a friend."