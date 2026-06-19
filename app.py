from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
from datetime import datetime
import os
from chatbot.chatbot import get_chatbot_response  # Import your Phase 8 chatbot
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Helper to get DB connection
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if not exist (run once or use init script)
def init_db():
    conn = get_db()
    # Your Phase 3 tables here...
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, 
        password TEXT, created_at TEXT)''')
    # Add other tables similarly...
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def index():
    return render_template('base.html')  # Landing / Home

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # In production: hash with bcrypt/Werkzeug
        
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)",
                        (name, email, password, datetime.now().isoformat()))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                           (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_name=session.get('user_name'))


import json
import plotly.express as px
import pandas as pd
from datetime import timedelta

# ... (previous code remains)

# Mood options with emojis and scores
MOOD_OPTIONS = {
    'Happy': {'emoji': '😊', 'score': 5},
    'Excited': {'emoji': '🎉', 'score': 4.5},
    'Neutral': {'emoji': '😐', 'score': 3},
    'Sad': {'emoji': '😢', 'score': 2},
    'Angry': {'emoji': '😠', 'score': 1.5},
    'Stressed': {'emoji': '😓', 'score': 1}
}

@app.route('/mood', methods=['GET', 'POST'])
@login_required
def mood_tracker():
    conn = get_db()
    
    if request.method == 'POST':
        mood = request.form.get('mood')
        note = request.form.get('note', '')
        
        if mood in MOOD_OPTIONS:
            score = MOOD_OPTIONS[mood]['score']
            conn.execute(
                "INSERT INTO mood_tracking (user_id, mood, score, date, note) VALUES (?, ?, ?, ?, ?)",
                (session['user_id'], mood, score, datetime.now().date().isoformat(), note)
            )
            conn.commit()
            flash(f'Mood logged: {mood} {MOOD_OPTIONS[mood]["emoji"]}', 'success')
        else:
            flash('Invalid mood selection.', 'danger')
    
    # Fetch user's mood history
    moods = conn.execute("""
        SELECT mood, score, date, note 
        FROM mood_tracking 
        WHERE user_id = ? 
        ORDER BY date DESC
    """, (session['user_id'],)).fetchall()
    
    # Prepare data for charts
    df = pd.DataFrame(moods, columns=['mood', 'score', 'date', 'note'])
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        
        # Weekly data (last 7 days)
        week_ago = datetime.now().date() - timedelta(days=7)
        weekly = df[df['date'].dt.date >= week_ago]
        
        # Monthly data (last 30 days)
        month_ago = datetime.now().date() - timedelta(days=30)
        monthly = df[df['date'].dt.date >= month_ago]
        
        # Generate Plotly JSON for frontend
        weekly_fig = px.line(weekly, x='date', y='score', 
                           title='Weekly Mood Trend', 
                           labels={'score': 'Mood Score (1-5)', 'date': 'Date'},
                           markers=True)
        monthly_fig = px.bar(monthly, x='date', y='score', color='mood',
                           title='Monthly Mood Distribution')
        
        weekly_json = weekly_fig.to_json()
        monthly_json = monthly_fig.to_json()
    else:
        weekly_json = monthly_json = None
    
    conn.close()
    
    return render_template('mood_tracker.html', 
                         moods=moods, 
                         mood_options=MOOD_OPTIONS,
                         weekly_json=weekly_json,
                         monthly_json=monthly_json)



# At the top
from reports.generate_report import generate_user_report

@app.route('/report')
@login_required
def report():
    return render_template('report.html')

# New Route
@app.route('/generate_report')
@login_required
def generate_report():
    try:
        report_path = generate_user_report(session['user_id'], session['user_name'])
        if report_path and os.path.exists(report_path):
            return send_file(report_path, as_attachment=True)
            # Note: We probably shouldn't delete the report immediately because send_file is asynchronous / streaming.
            # But the generated file resides in reports/ folder and gets generated with timestamp.
        else:
            flash('No mood data available to generate a report. Please log your mood first.', 'warning')
            return redirect(url_for('report'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('report'))

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
@login_required
def chatbot_post():
    message = request.form.get('message', '')
    response = get_chatbot_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
