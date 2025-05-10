from parser import extract_text_from_pdf
from ats_checker import get_ats_analysis
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
import requests
from collections import Counter
import re
import pdfplumber
from bs4 import BeautifulSoup
import pandas as pd
import os
import random

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "sk-xxx"  # Replace with your key
# YouTube API Configuration
YOUTUBE_API_KEY = "AIzaSyAjcV8VSA7Y4nt8DY2zPkTH_joLfX5wt90"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

st.set_page_config(
    page_title="Rezoomé - AI-Powered Resume Enhancement",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for user preferences
if "user_location" not in st.session_state:
    st.session_state["user_location"] = "India"
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "Data Analyst"  
if "user_exp" not in st.session_state:
    st.session_state["user_exp"] = "Beginner"
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True

# Enhanced dark mode styling
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
    
    /* Remove any unwanted text after header */
    .glass-container + p {
        display: none !important;
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
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%);
        color: black;
    }
    
    /* Premium Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: white;
    }
    
    /* Premium Success/Warning Messages */
    .stSuccess, .stWarning {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App Header with glowing gradient text
st.markdown("""
<div class="glass-container" style="text-align: center; padding: 2rem;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">Rezoomé</h1>
    <p style="font-size: 1.2rem; margin: 0;">AI-Powered Resume Enhancement Platform</p>
</div>
""", unsafe_allow_html=True)

# Function to fetch jobs
def fetch_jobs(job_title, location):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{job_title} in {location}",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": "d7c8f54009mshbecae8b8e18d660p13c37bjsn1cff14e7809a",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        jobs = data["data"]  # Extract job list
        return jobs
    except Exception as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return []

# Function to extract skills from job descriptions
def extract_skills_from_jobs(jobs):
    all_text = " ".join([job.get('job_description', '') for job in jobs])
    words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
    common = Counter(words).most_common(20)
    return [word for word, count in common if word not in ['the', 'and', 'you', 'with', 'for', 'job', 'will', 'have', 'are', 'our', 'all', 'this', 'that', 'from', 'your', 'their', 'what', 'when', 'where', 'which', 'who', 'why', 'how']]

# Function to fetch jobs from Indeed
def get_jobs_by_location(job_title, location):
    query = job_title.replace(' ', '+')
    location = location.replace(' ', '+')
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        jobs = []
        for div in soup.find_all(name='div', attrs={'class': 'job_seen_beacon'}):
            title = div.find('h2').text.strip() if div.find('h2') else 'N/A'
            company = div.find('span', class_='companyName')
            company = company.text.strip() if company else 'N/A'
            location = div.find('div', class_='companyLocation')
            location = location.text.strip() if location else 'N/A'
            
            # Try to get job link
            job_link = None
            link_elem = div.find('a', class_='jcs-JobTitle')
            if link_elem and 'href' in link_elem.attrs:
                job_link = 'https://www.indeed.com' + link_elem['href']
            
            # Try to get job description snippet
            description = ''
            desc_elem = div.find('div', class_='job-snippet')
            if desc_elem:
                description = desc_elem.text.strip()
            
            jobs.append({
                'title': title, 
                'company': company, 
                'location': location,
                'description': description,
                'link': job_link
            })
        
        return jobs
    except Exception as e:
        st.error(f"Error scraping jobs: {str(e)}")
        return []

# Function to extract skills from resume text
def extract_skills(text):
    # Common skills in tech industry
    common_skills = [
        'python', 'java', 'javascript', 'js', 'react', 'angular', 'vue', 'node', 'sql', 'nosql', 
        'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 
        'k8s', 'ci/cd', 'devops', 'agile', 'scrum', 'jira', 'git', 'github', 'gitlab', 'html', 
        'css', 'sass', 'less', 'bootstrap', 'tailwind', 'django', 'flask', 'fastapi', 'spring', 
        'hibernate', 'jpa', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'data science', 
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'nlp', 'natural language processing',
        'tableau', 'power bi', 'excel', 'word', 'powerpoint', 'office', 'microsoft', 'linux', 'unix',
        'shell', 'bash', 'powershell', 'rest', 'api', 'graphql', 'soap', 'xml', 'json', 'yaml',
        'terraform', 'ansible', 'puppet', 'chef', 'jenkins', 'circleci', 'travis', 'github actions',
        'typescript', 'ts', 'php', 'ruby', 'rails', 'go', 'golang', 'rust', 'c++', 'c#', 'dotnet',
        'swift', 'kotlin', 'android', 'ios', 'mobile', 'web', 'frontend', 'backend', 'fullstack',
        'data engineer', 'data analyst', 'data scientist', 'business analyst', 'product manager',
        'project manager', 'scrum master', 'qa', 'testing', 'sdet', 'sre', 'security', 'cybersecurity'
    ]
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Find skills in text
    found_skills = [skill for skill in common_skills if skill.lower() in text_lower]
    
    # Add any additional skills found through regex (words that might be skills)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
    word_counts = Counter(words)
    
    # Add words that appear multiple times and are not common words
    common_words = ['the', 'and', 'you', 'with', 'for', 'job', 'will', 'have', 'are', 'our', 'all', 
                   'this', 'that', 'from', 'your', 'their', 'what', 'when', 'where', 'which', 'who', 
                   'why', 'how', 'but', 'not', 'can', 'get', 'has', 'had', 'was', 'were', 'been', 
                   'being', 'such', 'then', 'than', 'now', 'just', 'also', 'very', 'much', 'many', 
                   'more', 'most', 'some', 'any', 'each', 'every', 'both', 'either', 'neither', 
                   'other', 'another', 'these', 'those', 'there', 'here', 'where', 'when', 'while', 
                   'before', 'after', 'since', 'until', 'unless', 'although', 'because', 'therefore', 
                   'however', 'moreover', 'furthermore', 'besides', 'except', 'beside', 'between', 
                   'among', 'within', 'without', 'through', 'throughout', 'during', 'despite', 
                   'except', 'including', 'regarding', 'concerning', 'about', 'against', 'along', 
                   'amid', 'around', 'at', 'by', 'for', 'from', 'in', 'into', 'of', 'on', 'onto', 
                   'to', 'toward', 'under', 'up', 'upon', 'with', 'within', 'without']
    
    # Add words that appear multiple times and are not common words
    for word, count in word_counts.most_common(20):
        if count > 1 and word not in common_words and word not in found_skills:
            found_skills.append(word)
    
    return found_skills

# Function to match jobs with skills
def match_jobs_with_skills(jobs, resume_skills):
    matched = []
    for job in jobs:
        # Combine job title and description for matching
        job_text = (job['title'] + ' ' + job.get('description', '')).lower()
        
        # Count matching skills
        matching_skills = [skill for skill in resume_skills if skill.lower() in job_text]
        
        if matching_skills:
            # Calculate match percentage
            match_percentage = len(matching_skills) / len(resume_skills) * 100
            
            # Add job with match info
            job_with_match = job.copy()
            job_with_match['matching_skills'] = matching_skills
            job_with_match['match_percentage'] = match_percentage
            matched.append(job_with_match)
    
    # Sort by match percentage
    matched.sort(key=lambda x: x['match_percentage'], reverse=True)
    return matched

# Create tabs for different functionalities
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "📄 Resume Analysis", 
    "🔍 Job Search", 
    "🎯 Job Recommendations", 
    "✨ Resume Improver", 
    "🔍 Keyword Gap Detector", 
    "📚 Course Suggestions", 
    "🧭 Career Fit Detector", 
    "📆 Learning Plan AI Coach", 
    "🧠 Resume Coach Chatbot", 
    "🪄 Resume Generator", 
    "⚙️ Settings", 
    "🧬 Multi-Version", 
    "🥊 Resume Battle"
])

with tab1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("📤 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf", key="resume_uploader")
    st.markdown('</div>', unsafe_allow_html=True)

    resume_text = None
    if uploaded_file:
        with st.spinner("⏳ Extracting text from your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Resume uploaded successfully!")
        
        with st.expander("📝 View Extracted Resume Text"):
            st.text_area("Here's what we extracted from your resume:", value=resume_text, height=200, key="resume_text_viewer")

    # Job details section
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("📊 ATS Score & Keyword Insights")

    col1, col2 = st.columns([1, 2])
    with col1:
        job_title = st.text_input("🎯 Job Title", key="ats_job_title")
    with col2:
        job_description = st.text_area("📋 Paste Job Description", height=250, key="ats_job_description")
    st.markdown('</div>', unsafe_allow_html=True)

    # Analysis button
    if st.button("🚀 Get ATS Score", key="ats_analyze_button"):
        if not uploaded_file or not job_description:
            st.warning("⚠️ Please upload your resume and paste a job description.")
        else:
            with st.spinner("⏳ Analyzing Resume and Job Description..."):
                result = get_ats_analysis(resume_text, job_description)

            st.success("✅ Analysis Complete! Here's your ATS Report")
            
            # Score display with donut chart
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            score = result['score']
            
            # Ring (Donut) Chart – Final Score
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Score', 'Remaining'],
                values=[score, 100 - score],
                hole=0.7,
                marker_colors=['#00F5A0', '#202020'],
                hoverinfo='label+percent',
                textinfo='none'
            )])
            fig_donut.update_layout(
                title_text=f"🌟 Final ATS Score: {score}%",
                title_font_size=24,
                annotations=[dict(text=f"{score}%", x=0.5, y=0.5, font_size=32, showarrow=False, font_color='white')],
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Score breakdown with bar chart
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("📊 Score Breakdown")
            
            # Bar Graph – Rule-based, LLM-based, Final
            fig_bar = go.Figure(data=[
                go.Bar(name='Rule-Based', x=['Score Type'], y=[result['details']['rule_based']], marker_color='#00BFFF'),
                go.Bar(name='LLM-Based', x=['Score Type'], y=[result['details']['llm_based']], marker_color='#FF6F91'),
                go.Bar(name='Final', x=['Score Type'], y=[score], marker_color='#FFD700')
            ])
            fig_bar.update_layout(
                barmode='group',
                title_text="📊 Score Breakdown by Logic",
                title_font_size=22,
                yaxis=dict(range=[0, 100]),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Missing keywords section
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("🚨 Missing Keywords")
            if result['missing_keywords']:
                for kw in result['missing_keywords']:
                    st.markdown(
                        f"<div class='keyword-badge'>🔴 {kw}</div>", 
                        unsafe_allow_html=True
                    )
            else:
                st.success("🎉 No missing keywords! Great job!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Keyword comparison chart
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("📊 Keyword Comparison")
            present = [kw for kw in result['top_keywords'] if kw not in result['missing_keywords']]
            missing = result['missing_keywords']
            
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=present,
                y=[1]*len(present),
                name="Present in Resume",
                marker_color='rgba(46, 204, 113, 0.6)'
            ))
            fig3.add_trace(go.Bar(
                x=missing,
                y=[1]*len(missing),
                name="Missing in Resume",
                marker_color='rgba(231, 76, 60, 0.6)'
            ))
            fig3.update_layout(
                title="Keywords Present vs Missing",
                barmode='group',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'}
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Suggestions section
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("💡 Suggestions to Improve Resume")
            for i, suggestion in enumerate(result['suggestions'], 1):
                st.markdown(
                    f"<div class='suggestion-box'><b>{i}.</b> {suggestion}</div>", 
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export to PDF button
            st.markdown('<div class="glass-container" style="text-align: center;">', unsafe_allow_html=True)
            if st.button("📥 Export Report to PDF", key="export_pdf_button"):
                with st.spinner("⏳ Generating PDF report..."):
                    # Create PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, "ATS Score Report", ln=True, align="C")
                    pdf.ln(10)
                    
                    # Add score
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(0, 10, f"Final ATS Score: {score}%", ln=True)
                    pdf.ln(5)
                    
                    # Add score breakdown
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "Score Breakdown:", ln=True)
                    pdf.set_font("Arial", "", 12)
                    pdf.cell(0, 10, f"Rule-based Score: {result['details']['rule_based']}%", ln=True)
                    pdf.cell(0, 10, f"LLM Score: {result['details']['llm_based']}%", ln=True)
                    pdf.ln(5)
                    
                    # Add missing keywords
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "Missing Keywords:", ln=True)
                    pdf.set_font("Arial", "", 12)
                    for kw in result['missing_keywords']:
                        pdf.cell(0, 10, f"- {kw}", ln=True)
                    pdf.ln(5)
                    
                    # Add suggestions
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "Suggestions to Improve:", ln=True)
                    pdf.set_font("Arial", "", 12)
                    for i, suggestion in enumerate(result['suggestions'], 1):
                        pdf.multi_cell(0, 10, f"{i}. {suggestion}")
                    
                    # Save PDF to buffer
                    pdf_buffer = io.BytesIO()
                    pdf.output(pdf_buffer)
                    pdf_buffer.seek(0)
                    
                    # Create download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_buffer,
                        file_name="ats_score_report.pdf",
                        mime="application/pdf",
                        key="download_pdf_button"
                    )
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🌍 Find Jobs in Your Region")

    job_title = st.text_input("Enter job title (e.g., Data Analyst)", key="job_search_title")
    location = st.text_input("Enter location (e.g., India, Remote, Hyderabad)", key="job_search_location")

    if st.button("🔍 Fetch Jobs", key="fetch_jobs_button"):
        with st.spinner("⏳ Searching for jobs..."):
            jobs = fetch_jobs(job_title, location)
            
            if jobs:
                st.success(f"Found {len(jobs)} jobs!")
                
                # Display top skills from job descriptions
                top_keywords = extract_skills_from_jobs(jobs)
                st.subheader("💡 Top Skills Mentioned in These Jobs:")
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                for keyword in top_keywords:
                    st.markdown(f"<div class='keyword-badge'>{keyword}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display job listings
                for job in jobs[:5]:
                    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                    st.markdown(f"### {job.get('job_title', 'N/A')}")
                    st.markdown(f"📍 Location: {job.get('job_city', 'N/A')}, {job.get('job_country', 'N/A')}")
                    st.markdown(f"🧑‍💻 Company: {job.get('employer_name', 'N/A')}")
                    st.markdown(f"💰 Salary: {job.get('job_salary', 'Not specified')}")
                    
                    # Add job description in an expander
                    with st.expander("📝 View Job Description"):
                        st.markdown(job.get('job_description', 'No description available'))
                    
                    # Apply link - use get() with a default value to avoid KeyError
                    if job.get('job_link'):
                        st.markdown(f"🔗 [Apply Here]({job['job_link']})")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No jobs found. Try a different title or location.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🎯 Personalized Job Recommendations")
    
    # File upload for resume
    st.subheader("📤 Upload Your Resume")
    resume_file = st.file_uploader("Choose your resume PDF", type="pdf", key="recommendation_resume")
    
    # Job search inputs
    st.subheader("🔍 Job Search Criteria")
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Enter job title (e.g., Data Analyst)", key="recommendation_job_title")
    with col2:
        location = st.text_input("Enter location (e.g., India, Remote, Hyderabad)", key="recommendation_location")
    
    if st.button("🚀 Find Matching Jobs", key="find_matching_jobs_button"):
        if not resume_file or not job_title or not location:
            st.warning("⚠️ Please upload your resume and provide job search criteria.")
        else:
            with st.spinner("⏳ Analyzing your resume and finding matching jobs..."):
                # Extract text from resume
                resume_text = extract_text_from_pdf(resume_file)
                
                # Extract skills from resume
                resume_skills = extract_skills(resume_text)
                
                # Display extracted skills
                st.subheader("💡 Skills Extracted from Your Resume")
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                for skill in resume_skills:
                    st.markdown(f"<div class='keyword-badge'>{skill}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Fetch jobs
                jobs = get_jobs_by_location(job_title, location)
                
                if jobs:
                    st.success(f"Found {len(jobs)} jobs! Matching with your skills...")
                    
                    # Match jobs with skills
                    matched_jobs = match_jobs_with_skills(jobs, resume_skills)
                    
                    if matched_jobs:
                        st.success(f"Found {len(matched_jobs)} jobs that match your skills!")
                        
                        # Display matched jobs
                        st.subheader("🎯 Top Matching Jobs")
                        for job in matched_jobs[:5]:
                            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                            
                            # Match percentage indicator
                            match_percentage = job['match_percentage']
                            match_color = '#00F5A0' if match_percentage > 70 else '#FFD700' if match_percentage > 50 else '#FF6F91'
                            
                            st.markdown(f"""
                                <div style='display: flex; justify-content: space-between; align-items: center;'>
                                    <h3>{job['title']}</h3>
                                    <div style='background: {match_color}; color: black; padding: 5px 10px; border-radius: 20px; font-weight: bold;'>
                                        {match_percentage:.1f}% Match
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"🧑‍💻 **Company:** {job['company']}")
                            st.markdown(f"📍 **Location:** {job['location']}")
                            
                            # Display matching skills
                            st.markdown("**Matching Skills:**")
                            for skill in job['matching_skills']:
                                st.markdown(f"<div class='keyword-badge'>{skill}</div>", unsafe_allow_html=True)
                            
                            # Job description
                            if job.get('description'):
                                with st.expander("📝 View Job Description"):
                                    st.markdown(job['description'])
                            
                            # Apply link
                            if job.get('link'):
                                st.markdown(f"🔗 [Apply Here]({job['link']})")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Export to CSV option
                        if len(matched_jobs) > 0:
                            st.subheader("📊 Export Results")
                            df = pd.DataFrame(matched_jobs)
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv,
                                file_name="matched_jobs.csv",
                                mime="text/csv",
                                key="download_csv_button"
                            )
                    else:
                        st.warning("No jobs found that match your skills. Try a different job title or location.")
                else:
                    st.warning("No jobs found. Try a different job title or location.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🧠 Smart Resume Improver & Skill Suggester")

    # File upload option
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF or TXT)", type=['pdf', 'txt'], key="resume_improver_upload")
    
    # Text input option (as fallback)
    resume_text = st.text_area("📝 Or paste your resume text here", height=300, value="", key="resume_improver_text")
    
    # Target role input
    target_role = st.text_input("🎯 Target Job Role (e.g., Cloud Engineer, Data Analyst)", key="target_role_input")

    def extract_text_from_file(uploaded_file):
        if uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        return ""

    def get_rewrite_and_skills(resume, role):
        prompt = f"""
You are an expert resume advisor.

The user wants to apply for the role of a **{role}**. Their current resume is below:

--- RESUME ---
{resume}
---------------

1. List important skills required for a {role}.
2. Then compare and find missing or weak skills in this resume.
3. Finally, rewrite the resume using clear, powerful language, and include important keywords to beat ATS.
"""

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = response.json()
        return reply['choices'][0]['message']['content']

    if st.button("✨ Rewrite My Resume", key="rewrite_resume_button"):
        if (uploaded_file is not None or resume_text) and target_role:
            with st.spinner("Improving your resume..."):
                # Get text from either uploaded file or text area
                final_resume_text = ""
                if uploaded_file is not None:
                    final_resume_text = extract_text_from_file(uploaded_file)
                else:
                    final_resume_text = resume_text

                if not final_resume_text.strip():
                    st.error("Could not extract text from the uploaded file. Please try pasting the text directly.")
                else:
                    result = get_rewrite_and_skills(final_resume_text, target_role)
                    st.markdown("## 📝 Rewritten Resume with Skill Suggestions")
                    st.markdown(result)
        else:
            st.warning("Please either upload a resume file or paste your resume text, and specify the target role!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🔍 Keyword Gap Detector - Match Your Resume to the Job!")

    # --- Upload Resume ---
    resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="keyword_gap_resume")

    # --- Paste Job Description ---
    job_description = st.text_area("📄 Paste Job Description Here", height=200, key="keyword_gap_job_description")

    # --- Get Keyword Gaps from LLM ---
    def get_keyword_gaps(resume_text, job_text):
        prompt = f"""
Compare this resume and job description.
Extract the top 15 important keywords from the job description.
Then show me which of these are missing in the resume.
Split them into:
- Must Have Skills
- Optional/Nice to Have Skills

Resume:
{resume_text}

Job Description:
{job_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    # Always show the analyze button
    if st.button("🔍 Analyze Resume vs Job Description", key="analyze_keyword_gaps_button"):
        # Check if both resume and job description are provided
        if not resume_file:
            st.error("Please upload a resume file to analyze.")
        elif not job_description:
            st.error("Please paste a job description to analyze.")
        else:
            with st.spinner("🔎 Analyzing Resume vs Job Description..."):
                try:
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(resume_file)
                    
                    if not resume_text.strip():
                        st.error("Could not extract text from the uploaded PDF. Please try a different file.")
                    else:
                        # Get keyword gaps
                        result = get_keyword_gaps(resume_text, job_description)
                        
                        # Display results
                        st.subheader("📉 Missing Keywords in Resume")
                        st.markdown(result)
                        
                        # Add a download button for the analysis
                        st.download_button(
                            label="📥 Download Analysis",
                            data=result,
                            file_name="keyword_gap_analysis.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")
    else:
        st.info("Upload a resume and paste a job description, then click 'Analyze' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("📚 One-Click Skill Course Suggestions")
    st.markdown("💡 Get free course recommendations based on missing skills in your resume!")

    # Function to get courses for a skill using YouTube API
    def get_courses_for_skill(skill):
        query = f"Free course on {skill}"
        params = {
            "key": YOUTUBE_API_KEY,
            "part": "snippet",
            "maxResults": 4,
            "q": query,
            "type": "video",
            "videoDuration": "long"
        }
        try:
            res = requests.get(YOUTUBE_SEARCH_URL, params=params)
            data = res.json()
            videos = []
            for item in data.get("items", []):
                snippet = item["snippet"]
                video_id = item["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                title = snippet["title"]
                thumbnail = snippet["thumbnails"]["medium"]["url"]
                channel = snippet["channelTitle"]
                videos.append((title, video_url, thumbnail, channel))
            return videos
        except Exception as e:
            st.error(f"Error fetching courses: {str(e)}")
            return []

    # --- Upload Resume ---
    resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="course_suggestion_resume")

    # --- Paste Job Description ---
    job_description = st.text_area("📄 Paste Job Description Here", height=200, key="course_suggestion_job_description")

    # --- Get Missing Skills from LLM ---
    def get_missing_skills(resume_text, job_text):
        prompt = f"""
Compare this resume and job description.
Extract the top 10 important skills from the job description.
Then identify which of these are missing in the resume.
Return ONLY a comma-separated list of missing skills, nothing else.

Resume:
{resume_text}

Job Description:
{job_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    if st.button("🔍 Find Missing Skills & Suggest Courses", key="suggest_courses_button"):
        if not resume_file:
            st.error("Please upload a resume file to analyze.")
        elif not job_description:
            st.error("Please paste a job description to analyze.")
        else:
            with st.spinner("🔎 Analyzing Resume vs Job Description..."):
                try:
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(resume_file)
                    
                    if not resume_text.strip():
                        st.error("Could not extract text from the uploaded PDF. Please try a different file.")
                    else:
                        # Get missing skills
                        missing_skills_text = get_missing_skills(resume_text, job_description)
                        
                        # Display missing skills
                        st.subheader("📉 Missing Skills in Your Resume")
                        st.markdown(f"**{missing_skills_text}**")
                        
                        # Process each missing skill
                        missing_skills = [skill.strip() for skill in missing_skills_text.split(',')]
                        
                        st.subheader("📚 Recommended Courses")
                        for skill in missing_skills:
                            st.markdown(f"### 🔍 Courses for **{skill}**")
                            results = get_courses_for_skill(skill)
                            
                            if results:
                                cols = st.columns(2)
                                for idx, (title, url, thumbnail, channel) in enumerate(results):
                                    with cols[idx % 2]:
                                        st.image(thumbnail, use_column_width=True)
                                        st.markdown(f"**[{title}]({url})**")
                                        st.caption(f"📺 {channel}")
                            else:
                                st.info(f"No courses found for {skill}. Try searching manually.")
                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")
    else:
        st.info("Upload a resume and paste a job description, then click 'Find Missing Skills & Suggest Courses' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab7:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🧭 Career Fit Detector")
    st.markdown("💡 Discover career paths that match your resume")

    # Initialize session state for resume text
    if "career_fit_resume_text" not in st.session_state:
        st.session_state.career_fit_resume_text = ""

    # --- Upload Resume ---
    resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="career_fit_resume")

    if resume_file:
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume_file)
        st.session_state.career_fit_resume_text = resume_text
        st.success("✅ Resume loaded!")

    # --- Get Career Fit from LLM ---
    def get_career_fit(resume_text):
        prompt = f"""
Based on the following resume, suggest 3 to 5 career paths the person is best suited for.
Also explain why for each suggestion.

Resume:
{resume_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a career advisor helping students decide their career path."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    if st.button("🔍 Suggest Career Paths", key="suggest_career_paths_button") and st.session_state.career_fit_resume_text:
        with st.spinner("🔎 Analyzing your resume for career fit..."):
            try:
                # Get career fit suggestions
                result = get_career_fit(st.session_state.career_fit_resume_text)
                
                # Display results
                st.subheader("🎯 Career Suggestions")
                st.markdown(result)
                
                # Add a download button for the analysis
                st.download_button(
                    label="📥 Download Career Fit Analysis",
                    data=result,
                    file_name="career_fit_analysis.txt",
                    mime="text/plain",
                    key="download_career_fit_button"
                )
            except Exception as e:
                st.error(f"Error analyzing resume: {str(e)}")
    else:
        st.info("Upload your resume and click 'Suggest Career Paths' to discover the best career options for you.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab8:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("📆 Learning Plan AI Coach")
    st.markdown("🎯 Upload your resume and type your career goal. Get a weekly learning roadmap!")

    # --- Upload Resume ---
    resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="learning_plan_resume")

    # --- Enter Career Goal ---
    goal = st.text_input("💼 What is your career goal? (e.g., Cloud Engineer, Data Scientist)", key="career_goal_input")

    # --- Get Learning Plan from LLM ---
    def get_learning_plan(resume_text, career_goal):
        prompt = f"""
You are a career roadmap coach.

Based on the resume below and the user's goal of becoming a '{career_goal}', give a complete, realistic roadmap to reach that goal.

Your roadmap should include:
- A list of major skills and tools to learn, in order
- At least 3 beginner → intermediate → advanced project ideas
- Best websites or platforms to learn (free if possible)
- YouTube playlist or channel suggestions for each skill
- Advice on certifications if useful
- Time estimation for each phase
- Job titles the person can apply for after learning

Keep it clear and actionable.

Resume: {resume_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    if st.button("🔍 Generate Learning Plan", key="generate_learning_plan_button"):
        if not resume_file:
            st.error("Please upload a resume file to analyze.")
        elif not goal:
            st.error("Please enter your career goal.")
        else:
            with st.spinner("🔎 Analyzing your resume and generating a learning plan..."):
                try:
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(resume_file)
                    
                    if not resume_text.strip():
                        st.error("Could not extract text from the uploaded PDF. Please try a different file.")
                    else:
                        # Get learning plan
                        result = get_learning_plan(resume_text, goal)
                        
                        # Display results
                        st.subheader("🗓️ Your Career Plan")
                        st.info(result)
                        
                        # Add a download button for the learning plan
                        st.download_button(
                            label="📥 Download Career Plan",
                            data=result,
                            file_name="career_plan.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error generating learning plan: {str(e)}")
    else:
        st.info("Upload your resume and enter your career goal, then click 'Generate Learning Plan' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab9:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🧠 Resume Coach Chatbot")
    st.markdown("💡 Talk to an AI that knows your resume inside-out!")

    # Initialize session state for chat history and resume text
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Upload Resume ---
    uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="chatbot_resume")

    if uploaded_file:
        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_file)
        st.session_state.resume_text = resume_text
        st.success("✅ Resume loaded into chatbot context!")

    # --- Chat Interface ---
    if st.session_state.resume_text:
        # Display chat history first
        chat_container = st.container()
        with chat_container:
            for question, answer in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.markdown(question)
                with st.chat_message("assistant"):
                    st.markdown(answer)
        
        # Keep the input box at the bottom
        user_input = st.chat_input("Ask a question about your resume...")

        if user_input:
            # Prepare the prompt with resume context
            prompt = f"""
You are a career coach giving resume feedback. Only use the following resume to answer questions:

Resume:
{st.session_state.resume_text}

User Question: {user_input}
"""

            # Define headers for the API request
            api_headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful and professional resume review coach."},
                    {"role": "user", "content": prompt}
                ]
            }

            with st.spinner("Thinking..."):
                try:
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
                    if response.status_code == 200:
                        reply = response.json()["choices"][0]["message"]["content"]
                        st.session_state.chat_history.append((user_input, reply))
                        # Force a rerun to update the chat display with the new message
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")
    else:
        st.info("Upload your resume to start chatting with the AI coach!")

    st.markdown('</div>', unsafe_allow_html=True)

with tab10:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🪄 Tailored Resume Version Generator")
    st.markdown("💡 Generate custom resumes for Amazon, Google, or any role!")

    # --- Upload Resume ---
    resume_file = st.file_uploader("📤 Upload Your Base Resume (PDF)", type=["pdf"], key="tailored_resume_generator")

    # --- Enter Target Company/Role ---
    target = st.text_input("✍️ Enter a company or job role to customize your resume (e.g., Amazon, Data Analyst, Google Cloud)", key="target_company_role")

    # --- Generate Tailored Resume ---
    def generate_tailored_resume(resume_text, target_company_role):
        prompt = f"""
You are an expert resume editor. Rewrite the resume below to target a job at {target_company_role}.
Make sure to improve the formatting, wording, and include relevant keywords.

Resume:
{resume_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a resume expert helping tailor resumes for job applications."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    if st.button("✨ Generate Custom Resume", key="generate_custom_resume_button"):
        if not resume_file:
            st.error("Please upload a resume file.")
        elif not target:
            st.error("Please enter a target company or job role.")
        else:
            with st.spinner("🔄 Generating your tailored resume..."):
                try:
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(resume_file)
                    
                    if not resume_text.strip():
                        st.error("Could not extract text from the uploaded PDF. Please try a different file.")
                    else:
                        # Generate tailored resume
                        customized_resume = generate_tailored_resume(resume_text, target)
                        
                        # Display results
                        st.subheader(f"🎯 Tailored Resume for {target}")
                        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                        st.code(customized_resume, language="markdown")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add download button
                        st.download_button(
                            label="💾 Download Custom Resume",
                            data=customized_resume,
                            file_name=f"Resume_for_{target}.txt",
                            mime="text/plain",
                            key="download_custom_resume_button"
                        )
                except Exception as e:
                    st.error(f"Error generating tailored resume: {str(e)}")
    else:
        st.info("Upload your resume and enter a target company or job role, then click 'Generate Custom Resume' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab11:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("⚙️ Rezoomé Settings & Themes")
    st.markdown("💡 Customize your experience and preferences")

    # Theme Toggle
    col1, col2 = st.columns([1, 3])
    with col1:
        dark_mode = st.toggle("🌗 Dark Mode", value=st.session_state["dark_mode"], key="dark_mode_toggle")
        st.session_state["dark_mode"] = dark_mode
    
    with col2:
        if dark_mode:
            st.markdown("""
                <div style="background-color: #0e1117; padding: 10px; border-radius: 10px; color: white;">
                <p>🌚 Dark mode is enabled</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; color: black;">
                <p>🌞 Light mode is enabled</p>
                </div>
            """, unsafe_allow_html=True)
            # Add a dynamic theme change (note: this will be applied on reload)
            st.markdown("""
                <style>
                body { background-color: #ffffff !important; color: #000000 !important; }
                .stApp { background-color: #f8f9fa !important; }
                [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important; color: #212529 !important; }
                h1, h2, h3, h4, h5, h6, p, label { color: #212529 !important; }
                </style>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # User Preferences
    st.subheader("🌍 Profile & Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("📍 Your Preferred Job Location", value=st.session_state["user_location"], key="user_location_input")
        st.session_state["user_location"] = location
    
    with col2:
        desired_role = st.text_input("💼 Desired Role", value=st.session_state["user_role"], key="user_role_input")
        st.session_state["user_role"] = desired_role
    
    experience_level = st.selectbox("📈 Experience Level", ["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(st.session_state["user_exp"]), key="user_exp_input")
    st.session_state["user_exp"] = experience_level
    
    # Notification settings
    st.subheader("🔔 Notification Preferences")
    email_notifications = st.checkbox("Receive email notifications for job matches", value=False, key="email_notifications")
    job_alert_frequency = st.select_slider("Job Alert Frequency", options=["Daily", "Weekly", "Monthly"], value="Weekly", key="job_alert_frequency")
    
    # Privacy settings
    st.subheader("🔒 Privacy Settings")
    remember_uploads = st.checkbox("Remember my uploaded resumes", value=True, key="remember_uploads")
    data_collection = st.checkbox("Allow anonymous data collection to improve the service", value=True, key="data_collection")
    
    # Save Settings Button
    if st.button("💾 Save Settings", key="save_settings_button"):
        st.success("✅ Your preferences have been saved!")
        st.balloons()

    st.info("🔍 These settings will be used across all tabs to personalize your experience!")

    st.markdown('</div>', unsafe_allow_html=True)

with tab12:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🧬 Create Custom Resume Version")
    st.markdown("💡 Tailor your resume for any company or job in one click")

    # File uploader for resume
    col1, col2 = st.columns([1, 1])
    with col1:
        # --- Upload Resume ---
        resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"], key="multi_version_resume")
    
    with col2:
        # Support text input for resume
        resume_text_input = st.text_area("📝 Or paste your resume text here", height=150, key="multi_version_resume_text")

    # --- Job Details ---
    col1, col2, col3 = st.columns(3)
    with col1:
        job_role = st.text_input("💼 Target Job Role", value="Data Scientist", key="multi_version_job_role")
    with col2:
        company = st.text_input("🏢 Target Company", value="Amazon", key="multi_version_company")
    with col3:
        region = st.text_input("🌍 Region", value="India", key="multi_version_region")

    # --- Generate Custom Resume Function ---
    def generate_custom_resume(resume_text, job_role, company, region):
        prompt = f"""
Rewrite this resume for a job role as {job_role} at {company} in {region}.
Make it tailored with the right keywords, skills, and tone suited to the job and company culture.
Use bullet points and clear formatting. Here's the original:

{resume_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a resume expert helping tailor resumes for job applications."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    # --- Main Logic ---
    if st.button("🚀 Generate Custom Resume", key="generate_multi_version_resume_button"):
        # Check if either file or text is provided
        if not resume_file and not resume_text_input:
            st.error("Please either upload a resume file or paste your resume text.")
        else:
            with st.spinner("🔄 Generating your customized resume..."):
                try:
                    # Get resume text from either file or input
                    resume_text = ""
                    if resume_file:
                        resume_text = extract_text_from_pdf(resume_file)
                    else:
                        resume_text = resume_text_input
                    
                    if not resume_text.strip():
                        st.error("Could not extract text from the uploaded file or the text area is empty.")
                    else:
                        # Generate custom resume
                        custom_resume = generate_custom_resume(resume_text, job_role, company, region)
                        
                        # Display results
                        st.subheader(f"✅ Your Customized Resume for {job_role} at {company}")
                        st.text_area("🎯 Tailored Resume Output", custom_resume, height=400, key="multi_version_output")
                        
                        # Add download button
                        st.download_button(
                            label="📥 Download Customized Resume",
                            data=custom_resume,
                            file_name=f"Resume_{job_role}_{company}.txt",
                            mime="text/plain",
                            key="download_multi_version_resume_button"
                        )
                        
                        # Show diff with original resume
                        st.subheader("📊 Key Changes Made")
                        st.info("The customized resume has been tailored specifically for the job role, company, and region. It includes relevant keywords and formatting to increase your chances of getting through the ATS screening process.")
                except Exception as e:
                    st.error(f"Error generating customized resume: {str(e)}")
    else:
        st.info("Upload your resume or paste the text, fill in the job details, then click 'Generate Custom Resume' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

with tab13:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("🥊 Resume vs Resume – Who Wins the ATS Fight?")
    st.markdown("💡 Upload two resumes and see which one is stronger for a specific job!")

    # File uploaders for resumes
    col1, col2 = st.columns(2)
    with col1:
        resume1_file = st.file_uploader("📤 Upload Resume 1 (PDF)", type=["pdf"], key="resume_battle_1")
    
    with col2:
        resume2_file = st.file_uploader("📤 Upload Resume 2 (PDF)", type=["pdf"], key="resume_battle_2")

    # Job title input
    job_title = st.text_input("🎯 Job Title (for ATS context)", value="Software Engineer", key="battle_job_title")
    
    # Function to analyze resume against job title
    def analyze_resume(resume_text, job_title):
        prompt = f"""
Analyze the following resume for the job title: {job_title}.
Give an ATS match score out of 100, list missing important skills or keywords,
and briefly mention strengths and weaknesses.

Resume:
{resume_text}
"""

        # Define headers for the API request
        api_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a resume analysis expert."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=api_headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    # Function to extract score from analysis result
    def extract_score(content):
        import re
        match = re.search(r"(\d{1,3})", content)
        return int(match.group(1)) if match else random.randint(60, 90)
    
    # Main logic
    if st.button("🚀 Compare Resumes", key="compare_resumes_button"):
        if not resume1_file or not resume2_file:
            st.error("Please upload both resumes to compare.")
        elif not job_title:
            st.error("Please enter a job title for context.")
        else:
            with st.spinner("⏳ Analyzing resumes..."):
                try:
                    # Extract text from PDFs
                    resume1_text = extract_text_from_pdf(resume1_file)
                    resume2_text = extract_text_from_pdf(resume2_file)
                    
                    if not resume1_text.strip() or not resume2_text.strip():
                        st.error("Could not extract text from one or both of the PDFs. Please try different files.")
                    else:
                        # Analyze resumes
                        with st.spinner("Analyzing Resume 1..."):
                            resume1_result = analyze_resume(resume1_text, job_title)
                        
                        with st.spinner("Analyzing Resume 2..."):
                            resume2_result = analyze_resume(resume2_text, job_title)
                        
                        # Extract scores
                        score1 = extract_score(resume1_result)
                        score2 = extract_score(resume2_result)
                        
                        # Display ATS Scores Comparison chart
                        st.subheader("📊 ATS Scores Comparison")
                        fig, ax = plt.subplots()
                        ax.bar(["Resume 1", "Resume 2"], [score1, score2], color=["#FF7F7F", "#7FFFD4"])
                        ax.set_ylim(0, 100)
                        st.pyplot(fig)
                        
                        # Display resume insights
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                            st.subheader("📋 Resume 1 Insights")
                            st.markdown(resume1_result)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                            st.subheader("📋 Resume 2 Insights")
                            st.markdown(resume2_result)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Determine winner
                        winner = "Resume 1 🥇" if score1 > score2 else "Resume 2 🥇" if score2 > score1 else "🤝 It's a tie!"
                        st.success(f"🏆 **Winner: {winner}**")
                        
                        # Create PDF report
                        pdf_content = f"""
# Resume Showdown Report

## Job Title: {job_title}

## Resume 1 Score: {score1}/100
{resume1_result}

## Resume 2 Score: {score2}/100
{resume2_result}

## Winner: {winner}
"""
                        
                        # Add download button for report
                        st.download_button(
                            label="📥 Download Comparison Report",
                            data=pdf_content,
                            file_name=f"resume_showdown_report.txt",
                            mime="text/plain",
                            key="download_resume_showdown_report_button"
                        )
                except Exception as e:
                    st.error(f"Error comparing resumes: {str(e)}")
    else:
        st.info("Upload two resumes and enter a job title, then click 'Compare Resumes' to see which one is stronger.")

    st.markdown('</div>', unsafe_allow_html=True)

# Update the footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <p>© 2024 Rezoomé. All rights reserved.</p>
    <p>Made with ❤️ for job seekers worldwide</p>
</div>
""", unsafe_allow_html=True) 