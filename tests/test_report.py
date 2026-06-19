from reports.generate_report import generate_user_report
import sqlite3
import os
import datetime

def test_report_generation():
    db_path = "test_report_db.db"
    
    # Create test database and insert mock data
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS mood_tracking (
        id INTEGER PRIMARY KEY, user_id INTEGER, mood TEXT, 
        score REAL, date TEXT, note TEXT)''')
    conn.execute("INSERT INTO mood_tracking (user_id, mood, score, date, note) VALUES (?, ?, ?, ?, ?)",
                 (1, "Happy", 5.0, datetime.datetime.now().date().isoformat(), "Feeling good test"))
    conn.commit()
    conn.close()

    # Generate report
    report_path = generate_user_report(1, "Test User", db_path=db_path)
    
    assert report_path is not None
    assert report_path.endswith('.pdf')
    assert os.path.exists(report_path)
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(report_path):
        os.remove(report_path)