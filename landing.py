import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="Rezoomé - AI-Powered Resume Enhancement",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #0f0f1a 0%, #1f1f3f 100%);
        color: white;
    }
    
    /* Premium Glassmorphism */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%);
        color: black;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 245, 160, 0.4);
    }
    
    /* Premium Headers */
    h1, h2, h3 {
        background: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 245, 160, 0.2);
    }
    
    /* Premium Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    
    /* Premium File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="glass-container" style="text-align: center; padding: 4rem 2rem;">
    <h1 style="font-size: 4rem; margin-bottom: 1rem;">Rezoomé</h1>
    <h2 style="font-size: 2rem; margin-bottom: 2rem;">AI-Powered Resume Enhancement</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Transform your resume with cutting-edge AI technology. Get personalized insights, improve your ATS score, and land your dream job.</p>
    <a href="/main" class="stButton">Get Started</a>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div style="padding: 2rem 0;">
    <h2 style="text-align: center; margin-bottom: 2rem;">Powerful Features</h2>
    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
        <div class="feature-card" style="width: 300px;">
            <h3>🔍 ATS Score Checker</h3>
            <p>Get instant feedback on your resume's ATS compatibility and improve your chances of getting noticed.</p>
        </div>
        <div class="feature-card" style="width: 300px;">
            <h3>✨ Resume Improver</h3>
            <p>Enhance your resume with AI-powered suggestions and optimize it for your target role.</p>
        </div>
        <div class="feature-card" style="width: 300px;">
            <h3>🎯 Keyword Gap Detector</h3>
            <p>Identify missing keywords and skills to make your resume more competitive.</p>
        </div>
        <div class="feature-card" style="width: 300px;">
            <h3>📚 Learning Plan AI Coach</h3>
            <p>Get personalized learning recommendations to bridge skill gaps.</p>
        </div>
        <div class="feature-card" style="width: 300px;">
            <h3>🪄 Multi-Version Resume Creator</h3>
            <p>Generate tailored resumes for different job roles and companies.</p>
        </div>
        <div class="feature-card" style="width: 300px;">
            <h3>🥊 Resume vs Resume Showdown</h3>
            <p>Compare multiple resumes and see which one performs better.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works Section
st.markdown("""
<div class="glass-container" style="margin-top: 2rem;">
    <h2 style="text-align: center;">How It Works</h2>
    <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
        <div style="text-align: center; width: 200px;">
            <h3>1️⃣ Upload</h3>
            <p>Upload your resume in PDF format</p>
        </div>
        <div style="text-align: center; width: 200px;">
            <h3>2️⃣ Analyze</h3>
            <p>Let our AI analyze your resume</p>
        </div>
        <div style="text-align: center; width: 200px;">
            <h3>3️⃣ Improve</h3>
            <p>Get personalized suggestions</p>
        </div>
        <div style="text-align: center; width: 200px;">
            <h3>4️⃣ Succeed</h3>
            <p>Land your dream job</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Testimonials Section
st.markdown("""
<div style="margin-top: 2rem;">
    <h2 style="text-align: center;">What Our Users Say</h2>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
        <div class="glass-container" style="width: 300px;">
            <p>"Rezoomé helped me improve my resume and land multiple interviews. The ATS score checker is a game-changer!"</p>
            <p style="text-align: right;">- Sarah, Software Engineer</p>
        </div>
        <div class="glass-container" style="width: 300px;">
            <p>"The keyword gap detector helped me identify missing skills and improve my resume significantly."</p>
            <p style="text-align: right;">- John, Data Scientist</p>
        </div>
        <div class="glass-container" style="width: 300px;">
            <p>"The multi-version resume creator saved me hours of work. Highly recommended!"</p>
            <p style="text-align: right;">- Emily, Product Manager</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class="glass-container" style="text-align: center; margin-top: 2rem; padding: 3rem;">
    <h2>Ready to Transform Your Resume?</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Join thousands of professionals who have improved their resumes with Rezoomé.</p>
    <a href="/main" class="stButton">Get Started Now</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <p>© 2024 Rezoomé. All rights reserved.</p>
    <p>Made with ❤️ for job seekers worldwide</p>
</div>
""", unsafe_allow_html=True) 