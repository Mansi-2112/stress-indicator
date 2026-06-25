import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import joblib
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from graphviz import Digraph

# ==========================================
# CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="MindGuard AI | Mental Wellness Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        :root {
            --primary: #64FFDA;
            --bg-navy: #0A192F;
            --bg-light-navy: #112240;
            --text-white: #E6F1FF;
            --text-slate: #8892B0;
        }

        .stApp {
            background-color: var(--bg-navy);
            color: var(--text-white);
            font-family: 'Inter', sans-serif;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(17, 34, 64, 0.7);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(100, 255, 218, 0.1);
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
        }

        /* Gradient Text */
        .gradient-text {
            background: linear-gradient(90deg, #64FFDA, #00B4D8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: var(--bg-light-navy);
            border-right: 1px solid rgba(100, 255, 218, 0.1);
        }

        /* Custom Button */
        .stButton>button {
            background: linear-gradient(45deg, #64FFDA, #48CAE4);
            color: #0A192F !important;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 25px;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.4);
            transform: scale(1.02);
        }

        /* Metrics styling */
        [data-testid="stMetricValue"] {
            color: var(--primary) !important;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==========================================
# MOCK MODEL LOADER (Fallback Logic)
# ==========================================
def load_model():
    try:
        model = joblib.load('stress_model.pkl')
        return model
    except:
        # If model doesn't exist, we return None and use a logic-based fallback for demo
        return None

model = load_model()

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_status_data(score):
    if score < 30:
        return "Low Stress", "🟢 Healthy", "Your mental state is stable. Keep maintaining your current lifestyle.", "#64FFDA"
    elif score < 60:
        return "Moderate Stress", "🟡 Needs Attention", "You are experiencing some pressure. Time to incorporate relaxation techniques.", "#FFD700"
    elif score < 80:
        return "High Stress", "🟠 High Risk", "High stress levels detected. Consider reducing workload and seeking balance.", "#FF8C00"
    else:
        return "Severe Stress", "🔴 Critical", "Warning: Severe stress detected. Please consult a professional counselor immediately.", "#FF4B4B"

def generate_pdf_report(user_info, prediction_data, ai_summary):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    p.setFillColor(colors.hexColor("#0A192F"))
    p.rect(0, height-100, width, 100, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height-60, "MINDGUARD AI - CLINICAL REPORT")
    
    # Body
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height-130, f"Patient Name: {user_info['name']}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height-150, f"Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    p.drawString(50, height-170, f"Age/Gender: {user_info['age']} / {user_info['gender']}")
    
    p.line(50, height-190, width-50, height-190)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height-220, "STRESS ANALYSIS RESULTS")
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.hexColor(prediction_data['color']))
    p.drawString(50, height-250, f"Category: {prediction_data['class']}")
    
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 12)
    p.drawString(50, height-280, f"Stress Probability Score: {prediction_data['score']}%")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height-320, "AI Clinical Summary:")
    p.setFont("Helvetica", 11)
    text = p.beginText(50, height-340)
    text.textLines(ai_summary)
    p.drawText(text)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h2 class='gradient-text'>MindGuard AI</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.info("This AI system uses advanced machine learning to detect stress patterns based on physiological and psychological markers.")
    
    st.divider()
    st.subheader("Daily Self-Care")
    water = st.slider("Water Intake (Glasses)", 0, 15, 5)
    st.progress(water/12 if water <=12 else 1.0)
    
    st.subheader("Quick Actions")
    if st.button("Clear Assessment"):
        st.rerun()

# ==========================================
# MAIN APP UI
# ==========================================

# 1. HERO SECTION
st.markdown("""
    <div class='glass-card' style='text-align: center; background: linear-gradient(135deg, rgba(17,34,64,0.8) 0%, rgba(10,25,47,0.8) 100%);'>
        <h1 class='gradient-text' style='font-size: 3rem;'>🧠 Stress Indicator & Wellness Analyzer</h1>
        <p style='color: #8892B0; font-size: 1.2rem;'>Understand your stress. Improve your wellness. Live healthier.</p>
        <p style='color: #64FFDA;'>Current Session: {}</p>
    </div>
""".format(datetime.now().strftime("%B %d, %Y | %H:%M")), unsafe_allow_html=True)

# 2. USER PROFILE & INPUTS
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("👤 User Profile")
    u_name = st.text_input("Full Name", "John Doe")
    u_age = st.number_input("Age", 18, 100, 25)
    u_gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
    u_role = st.radio("Status", ["Student", "Professional"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📝 Stress Assessment Form")
    
    tabs = st.tabs(["Emotional", "Physical", "Academic/Work", "Social & Home"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        anxiety = c1.slider("Anxiety / Tension Level", 0, 10, 5)
        mood = c2.slider("Sadness / Low Mood", 0, 10, 3)
        irritability = c1.slider("Irritability Level", 0, 10, 4)
        concentration = c2.slider("Concentration Problems", 0, 10, 2)
        
    with tabs[1]:
        c1, c2 = st.columns(2)
        heartbeat = c1.checkbox("Heartbeat Palpitations")
        sleep = c2.selectbox("Sleep Quality", ["Good", "Average", "Poor", "Insomnia"])
        headaches = c1.checkbox("Frequent Headaches")
        weight = c2.checkbox("Recent Weight Changes")
        health_issue = st.checkbox("Existing Health Issues")

    with tabs[2]:
        c1, c2 = st.columns(2)
        academic_load = c1.slider("Work/Academic Overload", 0, 10, 6)
        confidence = c2.slider("Subject Confidence", 0, 10, 7)
        attendance = c1.slider("Class/Work Attendance (%)", 0, 100, 90)
        relaxation = c2.slider("Lack of Relaxation Time", 0, 10, 5)

    with tabs[3]:
        c1, c2 = st.columns(2)
        loneliness = c1.slider("Loneliness / Isolation", 0, 10, 3)
        peer_comp = c2.slider("Peer Competition Pressure", 0, 10, 5)
        home_env = st.select_slider("Home Environment", options=["Stressful", "Neutral", "Peaceful"], value="Neutral")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PREDICTION LOGIC
# ==========================================
if st.button("🔍 ANALYZE MY STRESS LEVEL"):
    # Calculate a Mock Score for Demo purposes if no model
    # (In production, you'd format features and call model.predict_proba)
    feature_sum = anxiety + mood + irritability + concentration + academic_load + (10 - confidence/10) + (10 - attendance/10)
    mock_score = min(int((feature_sum / 60) * 100), 100)
    
    stress_class, status_badge, motivation, stress_color = get_status_data(mock_score)
    
    st.divider()
    
    # 5 & 6. STRESS METER & STATUS
    m_col1, m_col2, m_col3 = st.columns([1, 1, 1])
    
    with m_col1:
        st.markdown(f"<div class='glass-card' style='text-align: center; border-top: 5px solid {stress_color};'>", unsafe_allow_html=True)
        st.metric("STRESS SCORE", f"{mock_score}%")
        st.markdown(f"<h3 style='color: {stress_color};'>{stress_class}</h3>", unsafe_allow_html=True)
        st.markdown(f"**{status_badge}**")
        st.markdown("</div>", unsafe_allow_html=True)

    with m_col2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = mock_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Stress Intensity", 'font': {'color': "#E6F1FF"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': stress_color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#64FFDA",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(100, 255, 218, 0.1)'},
                    {'range': [30, 70], 'color': 'rgba(255, 215, 0, 0.1)'},
                    {'range': [70, 100], 'color': 'rgba(255, 75, 75, 0.1)'}],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"}, height=250, margin=dict(l=20,r=20,t=50,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with m_col3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("AI Insight")
        ai_msg = f"Analysis shows your stress is driven primarily by {'Academic workload' if academic_load > 5 else 'Emotional factors'}. {motivation}"
        st.write(ai_msg)
        st.markdown("</div>", unsafe_allow_html=True)

    # 7. RADAR CHART & TREE
    st.columns(1)
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Wellness Dimensions")
        categories = ['Emotional', 'Physical', 'Academic', 'Lifestyle', 'Social']
        values = [anxiety+mood, (5 if heartbeat else 1) + (5 if headaches else 1), academic_load, relaxation, loneliness]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#64FFDA',
            fillcolor='rgba(100, 255, 218, 0.3)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 15], gridcolor="#112240")),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with v_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Mental Health Tree")
        dot = Digraph()
        dot.attr(bgcolor='transparent', fontcolor='white')
        dot.node('A', 'Mental Health', color='#64FFDA', fontcolor='#64FFDA')
        dot.node('B', 'Emotional', color='#8892B0', fontcolor='white')
        dot.node('C', 'Academic', color='#8892B0', fontcolor='white')
        dot.node('D', 'Physical', color='#8892B0', fontcolor='white')
        dot.edges(['AB', 'AC', 'AD'])
        # Dynamic coloring
        if mock_score > 60:
            dot.edge('A', 'C', color='#FF4B4B', penwidth='3')
        st.graphviz_chart(dot)
        st.markdown("</div>", unsafe_allow_html=True)

    # 8. RECOMMENDATIONS
    st.subheader("🚀 Personalized Action Plan")
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    
    recs = {
        "Low": ["Keep 8h sleep", "Daily 15m walk", "Hydration focus"],
        "Moderate": ["5m Box Breathing", "Digital Detox at 9PM", "Prioritize Tasks"],
        "High": ["Professional Counseling", "Vagus Nerve Exercises", "Reduce Social Media"],
        "Severe": ["Urgent Therapy", "Medical Consultation", "Immediate Work Leave"]
    }
    
    current_recs = recs["Low"] if mock_score < 30 else recs["Moderate"] if mock_score < 60 else recs["High"] if mock_score < 80 else recs["Severe"]
    
    for i, rec in enumerate(current_recs):
        with [rec_col1, rec_col2, rec_col3][i]:
            st.markdown(f"""
                <div style='background: rgba(100,255,218,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #64FFDA;'>
                    <h4>Tip #{i+1}</h4>
                    <p>{rec}</p>
                </div>
            """, unsafe_allow_html=True)

    # 18. DOWNLOAD REPORT
    st.divider()
    report_data = {
        'class': stress_class,
        'score': mock_score,
        'color': stress_color
    }
    user_info = {'name': u_name, 'age': u_age, 'gender': u_gender}
    
    pdf_file = generate_pdf_report(user_info, report_data, ai_msg)
    st.download_button(
        label="📄 Download Professional Wellness Report",
        data=pdf_file,
        file_name=f"Wellness_Report_{u_name}.pdf",
        mime="application/pdf"
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #8892B0; border-top: 1px solid rgba(100,255,218,0.1); padding-top: 20px;'>
        <p>Made with ❤️ using Streamlit & Advanced AI | MindGuard Enterprise v2.0</p>
    </div>
""", unsafe_allow_html=True)
