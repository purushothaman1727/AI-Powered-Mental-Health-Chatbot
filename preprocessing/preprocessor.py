import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Download NLTK resources (run once)
def download_nltk_resources():
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    print("[INFO] NLTK resources downloaded.")

download_nltk_resources()

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """Comprehensive text cleaning"""
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove user mentions and hashtags (optional keep for context)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_text(text):
    """Full preprocessing pipeline"""
    text = clean_text(text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    processed_tokens = [
        lemmatizer.lemmatize(token) for token in tokens 
        if token not in stop_words and len(token) > 2
    ]
    
    return ' '.join(processed_tokens)

def preprocess_dataset(input_csv, output_csv, text_column='text', label_column='label'):
    """Preprocess entire dataset"""
    df = pd.read_csv(input_csv)
    
    print(f"Original shape: {df.shape}")
    
    # Apply cleaning
    df['cleaned_text'] = df[text_column].apply(clean_text)
    
    # Apply full preprocessing
    df['processed_text'] = df['cleaned_text'].apply(preprocess_text)
    
    # Drop rows with empty text
    df = df[df['processed_text'].str.strip() != '']
    
    # Save processed dataset
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"[SUCCESS] Preprocessed dataset saved to {output_csv}")
    print(f"Final shape: {df.shape}")
    return df

def create_tfidf_vectorizer(train_texts, max_features=5000):
    """Create and fit TF-IDF vectorizer"""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),      # unigrams + bigrams
        min_df=2
    )
    X = vectorizer.fit_transform(train_texts)
    print(f"[SUCCESS] TF-IDF vocabulary size: {len(vectorizer.vocabulary_)}")
    return vectorizer, X

# Example usage
if __name__ == "__main__":
    # Preprocess emotion dataset
    preprocess_dataset(
        'datasets/emotion_dataset.csv',
        'datasets/preprocessed/emotion_preprocessed.csv',
        text_column='text',
        label_column='label'
    )