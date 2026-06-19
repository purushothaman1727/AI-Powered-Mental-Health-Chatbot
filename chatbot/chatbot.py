import re
from transformers import pipeline
import os

# Load model once (efficient)
try:
    emotion_classifier = pipeline("text-classification", 
                                model="j-hartmann/emotion-english-distilroberta-base", 
                                top_k=1)
    print("[SUCCESS] Emergency emotion detector loaded.")
except Exception as e:
    print("[WARNING] Emotion model failed to load:", e)
    emotion_classifier = None

CRISIS_KEYWORDS = {
    "suicide": ["suicide", "kill myself", "end my life", "better off dead", "want to die", "end it all"],
    "self_harm": ["cut myself", "hurt myself", "self harm", "self-harm", "bleed"],
    "severe": ["hopeless", "worthless", "can't take it", "no reason to live", "give up"]
}

def detect_crisis(message: str):
    if not message:
        return False, None
    
    text = message.lower().strip()
    
    # Keyword detection
    for category, keywords in CRISIS_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return True, category
    
    # Emotion-based detection (backup)
    if emotion_classifier:
        try:
            result = emotion_classifier(message)[0][0]
            if result['label'] in ['sadness', 'fear'] and result['score'] > 0.80:
                return True, "severe_distress"
        except:
            pass
    
    return False, None

def get_emergency_response():
    return """
🛑 **You are not alone. Help is available right now.**

I’m really concerned about how you’re feeling. Please reach out to someone who can support you immediately.

**🇮🇳 India Helplines (24x7 or extended hours):**
• **iCall (TISS)**: 022-25521111  
• **AASRA**: 9820466726  
• **Vandrevala Foundation**: 9999666555  
• **Sneha Foundation**: 044-24640050  

**🌍 International**: https://www.befrienders.org/find-help

**Please talk to a friend, family member, or go to the nearest hospital.**

I’m here to listen if you want to continue, but professional help is most important right now. Take care ❤️
"""

def get_chatbot_response(user_message: str):
    is_crisis, _ = detect_crisis(user_message)
    
    if is_crisis:
        return get_emergency_response()
    
    try:
        if emotion_classifier:
            emotion = emotion_classifier(user_message)[0][0]['label']
            responses = {
                "joy": "That's great to hear! 😊 Keep doing things that make you happy.",
                "sadness": "I'm sorry you're feeling down. Would you like a breathing exercise or to talk about it?",
                "anger": "It's okay to feel angry. Take a deep breath. How can I support you?",
                "fear": "I hear you're anxious. Try 4-7-8 breathing: Inhale 4s, hold 7s, exhale 8s."
            }
            return responses.get(emotion, "Thank you for sharing. I'm here with you.")
    except:
        pass
    
    return "Thank you for trusting me. How are you feeling today? I'm listening."