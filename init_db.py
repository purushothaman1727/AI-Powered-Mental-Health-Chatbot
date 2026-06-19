import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Mood_Tracking Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mood_Tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mood TEXT NOT NULL,
        score INTEGER CHECK (score >= 1 AND score <= 10),
        date DATE DEFAULT CURRENT_DATE,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    # Chat_History Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chat_History (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        emotion_detected TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    # Wellness_Activities Table (Pre-populated)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Wellness_Activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,  -- e.g., 'Breathing', 'Meditation', 'Physical', 'Journaling'
        min_score_recommended INTEGER
    )
    ''')

    # Insert sample wellness activities
    sample_activities = [
        ("Deep Breathing", "4-7-8 breathing technique: Inhale 4s, hold 7s, exhale 8s.", "Breathing", 5),
        ("Mindful Walking", "Take a 10-minute walk focusing on your surroundings.", "Physical", 4),
        ("Gratitude Journaling", "Write 3 things you are grateful for today.", "Journaling", 3),
        ("Progressive Muscle Relaxation", "Tense and relax muscle groups one by one.", "Meditation", 6),
        ("Grounding 5-4-3-2-1", "Name 5 things you see, 4 you can touch, etc.", "Breathing", 7),
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO Wellness_Activities (title, description, category, min_score_recommended)
    VALUES (?, ?, ?, ?)
    ''', sample_activities)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully with tables and sample data!")

if __name__ == "__main__":
    init_database()