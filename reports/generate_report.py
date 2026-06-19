from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'MindGuard - Mental Wellness Report', ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | Page {self.page_no()}', align='C')

def generate_user_report(user_id, user_name, db_path='database.db'):
    conn = sqlite3.connect(db_path)
    
    # Fetch mood data
    df = pd.read_sql_query("""
        SELECT date, mood, score, note 
        FROM mood_tracking 
        WHERE user_id = ? 
        ORDER BY date DESC
    """, conn, params=(user_id,))
    
    conn.close()

    if df.empty:
        return None  # No data

    # Calculate statistics
    avg_score = round(df['score'].mean(), 2)
    wellness_score = round((avg_score / 5) * 100, 1)  # Percentage
    most_common_mood = df['mood'].mode()[0] if not df['mood'].empty else "Neutral"
    
    stress_level = "Low" if avg_score >= 4 else "Medium" if avg_score >= 2.5 else "High"

    # Create temporary chart
    plt.figure(figsize=(8, 4))
    df['date'] = pd.to_datetime(df['date'])
    plt.plot(df['date'], df['score'], marker='o', linewidth=2)
    plt.title('Mood Trend (Last 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Mood Score')
    plt.grid(True)
    chart_path = f'reports/mood_trend_{user_id}.png'
    plt.savefig(chart_path)
    plt.close()

    # Generate PDF
    pdf = PDFReport()
    pdf.add_page()
    
    # User Info
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Report for: {user_name}", ln=1)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    pdf.ln(5)

    # Wellness Score
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Overall Wellness Score: {wellness_score}%", ln=1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Average Mood: {avg_score}/5 | Dominant Mood: {most_common_mood}", ln=1)
    pdf.cell(0, 10, f"Stress Level: {stress_level}", ln=1)
    pdf.ln(10)

    # Mood Trend Chart
    pdf.cell(0, 10, "Mood Trend Over Time:", ln=1)
    pdf.image(chart_path, x=10, w=180)
    pdf.ln(10)

    # Mood History Table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Recent Mood History:", ln=1)
    pdf.set_font('Arial', '', 10)
    
    # Table Header
    pdf.cell(40, 8, "Date", 1)
    pdf.cell(40, 8, "Mood", 1)
    pdf.cell(30, 8, "Score", 1)
    pdf.cell(80, 8, "Note", 1, ln=1)
    
    # Table Data
    for _, row in df.head(15).iterrows():  # Last 15 entries
        pdf.cell(40, 8, str(row['date']), 1)
        pdf.cell(40, 8, row['mood'], 1)
        pdf.cell(30, 8, str(row['score']), 1)
        pdf.cell(80, 8, str(row['note'])[:50] + "..." if len(str(row['note'])) > 50 else str(row['note']), 1, ln=1)

    pdf.ln(10)

    # Personalized Suggestions
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Personalized Recommendations:", ln=1)
    pdf.set_font('Arial', '', 11)
    
    suggestions = {
        "High": ["Practice deep breathing exercises daily", "Consider talking to a professional counselor", "Try 10-minute meditation sessions"],
        "Medium": ["Maintain regular physical activity", "Journal your thoughts daily", "Connect with friends/family"],
        "Low": ["Continue your positive habits", "Try new wellness activities", "Share your progress with loved ones"]
    }
    
    for sug in suggestions.get(stress_level, suggestions["Medium"]):
        pdf.cell(0, 8, f"- {sug}", ln=1)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Emergency Helplines:", ln=1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, "- India: iCall (022-25521111) | AASRA (91-9820466726)", ln=1)
    pdf.cell(0, 8, "- International: Find local helpline at befrienders.org", ln=1)

    # Save PDF
    report_path = f'reports/wellness_report_{user_id}_{datetime.now().strftime("%Y%m%d")}.pdf'
    pdf.output(report_path)
    
    # Clean up chart
    if os.path.exists(chart_path):
        os.remove(chart_path)
    
    return report_path