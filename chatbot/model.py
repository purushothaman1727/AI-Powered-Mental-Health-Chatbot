from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import joblib
import torch
import re
from preprocessing.preprocessor import preprocess_text

# Load models (lazy loading for performance)
emotion_pipeline = None
tfidf_vectorizer = None
traditional_models = {}

EMOTION_MAP = {
    'sadness': 'Sadness',
    'joy': 'Joy',
    'love': 'Love',
    'anger': 'Anger',
    'fear': 'Fear',
    'surprise': 'Surprise'
}

def load_models():
    global emotion_pipeline, tfidf_vectorizer, traditional_models
    try:
        # DistilBERT Emotion Model (Hugging Face)
        emotion_pipeline = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1
        )
        print("[SUCCESS] DistilBERT Emotion Model loaded successfully!")
    except Exception as e:
        print(f"[WARNING] Failed to load Transformer: {e}. Using fallback.")
        emotion_pipeline = None

    # Load traditional models as fallback
    try:
        tfidf_vectorizer = joblib.load('models/saved_models/tfidf_vectorizer.pkl')
        for name in ["logistic_regression", "random_forest", "naive_bayes"]:
            traditional_models[name] = joblib.load(f'models/saved_models/{name}.pkl')
    except:
        pass

def detect_emotion(text: str):
    """Return top emotion with confidence"""
    processed = preprocess_text(text)
    if not processed:
        return "neutral", 0.5

    if emotion_pipeline:
        try:
            results = emotion_pipeline(processed)[0]
            top = max(results, key=lambda x: x['score'])
            label = top['label']
            score = top['score']
            return label, score
        except:
            pass

    # Fallback to traditional model
    if tfidf_vectorizer and traditional_models:
        X = tfidf_vectorizer.transform([processed])
        model = traditional_models.get("logistic_regression")
        if model:
            pred = model.predict(X)[0]
            # Map numeric label back if needed
            return list(EMOTION_MAP.values())[pred % len(EMOTION_MAP)], 0.75

    return "neutral", 0.6

load_models()  # Load on import