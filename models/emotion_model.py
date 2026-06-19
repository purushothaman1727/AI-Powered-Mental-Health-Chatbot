import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Emotion label mapping (from dair-ai/emotion dataset)
EMOTION_LABELS = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

def load_preprocessed_data():
    df = pd.read_csv('datasets/preprocessed/emotion_preprocessed.csv')
    print(f"Loaded dataset: {df.shape}")
    print("Class Distribution:\n", df['label'].value_counts())
    return df

def train_and_evaluate_models():
    df = load_preprocessed_data()
    
    X = df['processed_text']
    y = df['label']
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_tfidf = vectorizer.fit_transform(X)
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42, stratify=y
    )
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        "Naive Bayes": MultinomialNB()
    }
    
    results = {}
    os.makedirs('models/saved_models', exist_ok=True)
    
    for name, model in models.items():
        print(f"\n[INFO] Training {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=[EMOTION_LABELS[i] for i in range(6)])
        
        print(f"[SUCCESS] {name} Accuracy: {accuracy:.4f}")
        print(report)
        
        # Save model and vectorizer
        joblib.dump(model, f'models/saved_models/{name.lower().replace(" ", "_")}.pkl')
        
        # Save confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=[EMOTION_LABELS[i] for i in range(6)],
                    yticklabels=[EMOTION_LABELS[i] for i in range(6)])
        plt.title(f'Confusion Matrix - {name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'models/saved_models/{name.lower().replace(" ", "_")}_cm.png')
        plt.close()
        
        results[name] = {
            'accuracy': accuracy,
            'report': report
        }
    
    # Save vectorizer
    joblib.dump(vectorizer, 'models/saved_models/tfidf_vectorizer.pkl')
    print("\n[SUCCESS] All models and vectorizer saved successfully!")
    
    return results

if __name__ == "__main__":
    train_and_evaluate_models()