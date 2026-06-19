import os
import pandas as pd
from datasets import load_dataset

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def download_emotion_dataset():
    """Download the Emotion classification dataset from Hugging Face"""
    print("[INFO] Downloading dair-ai/emotion dataset...")
    try:
        dataset = load_dataset("dair-ai/emotion")
        df = pd.DataFrame(dataset['train'])
        df.to_csv('data/emotion_dataset.csv', index=False)
        print("[SUCCESS] Emotion dataset downloaded and saved to data/emotion_dataset.csv!")
    except Exception as e:
        print(f"[ERROR] Failed to download emotion dataset: {e}")

def download_mental_health_chatbot_dataset():
    """Download the Mental Health Chatbot Q&A dataset from Hugging Face"""
    print("[INFO] Downloading heliosbrahma/mental_health_chatbot_dataset...")
    try:
        dataset = load_dataset("heliosbrahma/mental_health_chatbot_dataset")
        df = pd.DataFrame(dataset['train'])
        df.to_csv('data/mental_health_chatbot.csv', index=False)
        print("[SUCCESS] Mental health chatbot dataset downloaded and saved to data/mental_health_chatbot.csv!")
    except Exception as e:
        print(f"[ERROR] Failed to download mental health chatbot dataset: {e}")

def download_counseling_conversations_dataset():
    """Download the Mental Health Counseling Conversations dataset from Hugging Face"""
    print("[INFO] Downloading Amod/mental_health_counseling_conversations...")
    try:
        dataset = load_dataset("Amod/mental_health_counseling_conversations")
        df = pd.DataFrame(dataset['train'])
        df.to_csv('data/counseling_conversations.csv', index=False)
        print("[SUCCESS] Counseling conversations dataset downloaded and saved to data/counseling_conversations.csv!")
    except Exception as e:
        print(f"[ERROR] Failed to download counseling conversations dataset: {e}")

def load_mental_health_data():
    """Example loader function to verify files are present and loadable"""
    try:
        emotion_df = pd.read_csv('data/emotion_dataset.csv')
        chatbot_df = pd.read_csv('data/mental_health_chatbot.csv')
        counseling_df = pd.read_csv('data/counseling_conversations.csv')
        print("\n--- Dataset Summary ---")
        print(f"- Emotion Dataset: {emotion_df.shape[0]} rows. Labels count:\n{emotion_df['label'].value_counts()}")
        print(f"- Chatbot Q&A Dataset: {chatbot_df.shape[0]} rows.")
        print(f"- Counseling Conversations: {counseling_df.shape[0]} rows.")
        return emotion_df, chatbot_df, counseling_df
    except FileNotFoundError as e:
        print(f"[ERROR] Some datasets are missing. Please run download functions first. Error: {e}")
        return None

if __name__ == "__main__":
    download_emotion_dataset()
    download_mental_health_chatbot_dataset()
    download_counseling_conversations_dataset()
    load_mental_health_data()
