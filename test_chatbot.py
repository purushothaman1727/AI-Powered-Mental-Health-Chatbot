from chatbot.model import detect_emotion
from chatbot.responses import get_supportive_response

if __name__ == "__main__":
    test = "I feel so anxious and overwhelmed today"
    emotion, conf = detect_emotion(test)
    print(f"Detected: {emotion} ({conf:.2f})")
    print("Response details:")
    print(get_supportive_response(test))
