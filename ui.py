
import streamlit as st
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt

def setup_page():
    """Apply custom CSS and setup page (without setting page config)"""
    # Apply custom CSS only
    apply_custom_css()
    
    # Add local logo handling via JavaScript
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Try to load the logo, if it fails, show fallback text
            var logoImg = document.querySelector('.logo-image');
            if (logoImg) {
                logoImg.onerror = function() {
                    var logoContainer = document.querySelector('.logo-container');
                    if (logoContainer) {
                        logoContainer.innerHTML = '<div style="font-size: 40px;"></div>';
                    }
                };
            }
        });
    </script>
    """, unsafe_allow_html=True)

def display_header():

    try:
        with open("euron.jpg", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Euron Logo" class="logo-image" style="max-height: 100px;">'
    except:
      
        logo_html = '<div style="font-size: 50px; text-align: center;"></div>'

    st.markdown(f"""
    <style>
    /* Enhanced animated app title: typewriter, shimmer, neon pulse, pop on hover */
    .animated-title-typewriter {{
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffd700, #6a11cb, #11998e, #ffd700 80%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: #ffd700;
        letter-spacing: 2px;
        text-shadow:
            0 0 8px #ffd700,
            0 0 16px #6a11cb,
            0 0 32px #11998e;
        display: inline-block;
        border-right: 3px solid #ffd700;
        white-space: nowrap;
        overflow: hidden;
        width: 0;
        opacity: 1;
        animation:
            typing 2.5s steps(36, end) 0.3s 1 normal both,
            shimmer 3.5s linear 2.8s infinite,
            neonPulse 1.2s 2.8s infinite alternate,
            blink-caret 0.7s step-end infinite;
        animation-fill-mode: forwards, inherit, inherit, inherit;
        transition: filter 0.2s, transform 0.2s;
    }}
    /* After typewriter animation, ensure text is always visible and not clipped */
    .animated-title-typewriter.animated-title-finish {{
        width: 36ch !important;
        overflow: visible !important;
        -webkit-text-fill-color: transparent !important;
        color: #ffd700 !important;
    }}
    /* Add a small script to add the finish class after animation */
    </style>
    <script>
    setTimeout(function() {{
        var el = document.querySelector('.animated-title-typewriter');
        if (el) el.classList.add('animated-title-finish');
    }}, 3000);
    </script>
    <style>
    @keyframes typing {{
        from {{ width: 0; }}
        to {{ width: 36ch; }}
    }}
    @keyframes blink-caret {{
        from, to {{ border-color: transparent; }}
        50% {{ border-color: #ffd700; }}
    }}
    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 100% 50%; }}
    }}
    @keyframes neonPulse {{
        from {{
            text-shadow:
                0 0 8px #ffd700,
                0 0 16px #6a11cb,
                0 0 32px #11998e;
        }}
        to {{
            text-shadow:
                0 0 32px #ffd700,
                0 0 48px #6a11cb,
                0 0 64px #11998e;
        }}
    }}
    .animated-title-typewriter:hover {{
        filter: brightness(1.2) drop-shadow(0 0 24px #ffd700);
        transform: scale(1.07) rotate(-1deg);
    }}
    /* Animated subtitle with color cycling glow */
    .animated-subtitle-glow {{
        font-size: 1.25rem;
        font-weight: 600;
        color: #fff;
        letter-spacing: 1px;
        text-shadow: 0 0 12px #11998e, 0 0 24px #6a11cb, 0 0 32px #ffd700;
        opacity: 0;
        transform: translateY(20px) scale(0.98);
        animation: fadeInSubtitle 1.2s 2.7s cubic-bezier(.68,-0.55,.27,1.55) forwards, colorGlow 3.5s linear infinite;
        margin-top: 8px;
        margin-bottom: 0;
        transition: text-shadow 0.2s;
    }}
    @keyframes fadeInSubtitle {{
        0% {{ opacity: 0; transform: translateY(20px) scale(0.98); }}
        80% {{ opacity: 1; transform: translateY(-2px) scale(1.01); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes colorGlow {{
        0% {{ text-shadow: 0 0 12px #11998e, 0 0 24px #6a11cb, 0 0 32px #ffd700; }}
        33% {{ text-shadow: 0 0 18px #ffd700, 0 0 32px #11998e, 0 0 40px #6a11cb; }}
        66% {{ text-shadow: 0 0 18px #6a11cb, 0 0 32px #ffd700, 0 0 40px #11998e; }}
        100% {{ text-shadow: 0 0 12px #11998e, 0 0 24px #6a11cb, 0 0 32px #ffd700; }}
    }}
    /* Emoji bounce and hover */
    .rocket-emoji-animated {{
        display: inline-block;
        animation: rocketBounce 1.6s infinite cubic-bezier(.68,-0.55,.27,1.55);
        font-size: 2.2rem;
        margin-right: 10px;
        filter: drop-shadow(0 0 8px #ffd700);
        transition: filter 0.2s;
        cursor: pointer;
    }}
    .rocket-emoji-animated:hover {{
        filter: drop-shadow(0 0 24px #ffd700) brightness(1.3);
    }}
    @keyframes rocketBounce {{
        0%, 100% {{ transform: translateY(0) rotate(-8deg) scale(1); }}
        30% {{ transform: translateY(-10px) rotate(-2deg) scale(1.08); }}
        60% {{ transform: translateY(2px) rotate(4deg) scale(0.98); }}
    }}
    </style>
    <div class="main-header">
        <div class="header-container">
            <div class="logo-container" style="text-align: center; margin-bottom: 20px;">
                {logo_html}
            </div>
            <div class="title-container" style="text-align: center;">
                <span class="rocket-emoji-animated">🙋‍♂️</span>
                <span class="animated-title-typewriter">TechSeva IT Recruitment Agent.AI</span>
                <div class="animated-subtitle-glow">Smart Resume Analysis &amp; Interview Preparation System</div>
                <div class="tagline-fade-glow">Your AI Partner for Smarter Recruitment.</div>
                <div class="tagline-bounce-color">Smarter Hiring. Faster Decisions.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)



def apply_custom_css(accent_color="#d32f2f"):
    st.markdown(f"""
    <style>
        /* New dark neon animated gradient background */
        body, .main, .stApp {{
            background: linear-gradient(135deg, #232526 0%, #0f2027 30%, #11998e 60%, #6a11cb 85%, #ffd700 100%) !important;
            color: #fff !important;
            animation: bgMove 14s ease-in-out infinite alternate;
            background-size: 200% 200%;
        }}
        @keyframes bgMove {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 100% 50%; }}
        }}

        /* Neon glow for cards and containers */
        .card {{
            background: rgba(20,30,60,0.97);
            border-radius: 22px;
            padding: 32px;
            margin-bottom: 32px;
            border-left: 7px solid #11998e;
            box-shadow: 0 0 36px 8px #6a11cb99, 0 0 72px 16px #ffd70099;
            transition: box-shadow 0.3s, border-color 0.3s;
        }}
        .card:hover {{
            box-shadow: 0 0 72px 24px #ffd700, 0 0 144px 48px #6a11cb;
            border-left: 7px solid #ffd700;
        }}

        /* Neon tabs */
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(90deg, #11998e 0%, #6a11cb 60%, #ffd700 100%) !important;
            border-bottom: 6px solid #ffd700 !important;
            color: #fff !important;
            text-shadow: 0 0 16px #11998e, 0 0 8px #ffd700;
        }}
        .stTabs [aria-selected="false"] {{
            color: #eee !important;
        }}

        /* Neon animated buttons with ripple effect */
        .stButton button {{
            background: linear-gradient(90deg, #11998e 0%, #6a11cb 60%, #ffd700 100%) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 14px !important;
            box-shadow: 0 0 20px 6px #11998e99, 0 0 40px 12px #ffd70099;
            font-weight: bold;
            font-size: 1.2rem;
            transition: transform 0.15s, box-shadow 0.2s;
            outline: none !important;
            position: relative;
            overflow: hidden;
        }}
        .stButton button:active {{
            transform: scale(0.95) rotate(-2deg);
            box-shadow: 0 0 48px 16px #ffd700, 0 0 96px 32px #6a11cb;
        }}
        .stButton button .ripple {{
            position: absolute;
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            background: rgba(255,255,255,0.5);
            pointer-events: none;
        }}
        @keyframes ripple {{
            to {{
                transform: scale(4);
                opacity: 0;
            }}
        }}
        /* Add ripple effect via JS */
    /* Tagline 1: fade-in, slide-up, neon glow */
    .tagline-fade-glow {{
        font-size: 1.05rem;
        color: #fff;
        opacity: 0;
        margin-top: 10px;
        margin-bottom: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 0 8px #11998e, 0 0 16px #6a11cb;
        animation: taglineFadeGlow 1.2s 5.2s cubic-bezier(.68,-0.55,.27,1.55) forwards;
    }}
    @keyframes taglineFadeGlow {{
        0% {{ opacity: 0; transform: translateY(20px) scale(0.98); }}
        80% {{ opacity: 1; transform: translateY(-2px) scale(1.01); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    /* Tagline 2: bounce-in, color cycling */
    .tagline-bounce-color {{
        font-size: 1.05rem;
        color: #ffd700;
        opacity: 0;
        margin-top: 2px;
        margin-bottom: 0;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px #ffd700, 0 0 18px #6a11cb;
        animation: taglineBounceIn 1.1s 6.2s cubic-bezier(.68,-0.55,.27,1.55) forwards, taglineColorCycle 3.2s 7.3s linear infinite;
    }}
    @keyframes taglineBounceIn {{
        0% {{ opacity: 0; transform: translateY(30px) scale(0.95); }}
        60% {{ opacity: 1; transform: translateY(-8px) scale(1.08); }}
        80% {{ opacity: 1; transform: translateY(2px) scale(0.98); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes taglineColorCycle {{
        0% {{ color: #ffd700; text-shadow: 0 0 10px #ffd700, 0 0 18px #6a11cb; }}
        33% {{ color: #6a11cb; text-shadow: 0 0 14px #6a11cb, 0 0 24px #11998e; }}
        66% {{ color: #11998e; text-shadow: 0 0 14px #11998e, 0 0 24px #ffd700; }}
        100% {{ color: #ffd700; text-shadow: 0 0 10px #ffd700, 0 0 18px #6a11cb; }}
    }}
    </style>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        document.querySelectorAll('.stButton button').forEach(function(btn) {{
            btn.addEventListener('click', function(e) {{
                var ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.width = ripple.style.height = Math.max(btn.offsetWidth, btn.offsetHeight) + 'px';
                ripple.style.left = (e.offsetX - btn.offsetWidth/2) + 'px';
                ripple.style.top = (e.offsetY - btn.offsetHeight/2) + 'px';
                btn.appendChild(ripple);
                setTimeout(function() {{ ripple.remove(); }}, 600);
            }});
        }});
    }});
    </script>
    """, unsafe_allow_html=True)




def setup_sidebar():
    with st.sidebar:
        st.header("Configuration")
        
        st.subheader("API Keys")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        
        st.markdown("---")
        
        
        st.subheader("Theme")
        theme_color = st.color_picker("Accent Color", "#d32f2f")
        st.markdown(f"""
        <style>
        .stButton button, .main-header, .stTabs [aria-selected="true"] {{
            background-color: {theme_color} !important;
            border-color: {theme_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p>TechSeva IT Recruitment Agent.AI</p>
            <p style="font-size: 0.8rem; color: #666;">v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        return {
            "openai_api_key": openai_api_key,
            "theme_color": theme_color
        }



def role_selection_section(role_requirements):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        role = st.selectbox("Select the role you're applying for:", list(role_requirements.keys()))
    
    with col2:
        upload_jd = st.checkbox("Upload custom job description instead")
    
    custom_jd = None
    if upload_jd:
        custom_jd_file = st.file_uploader("Upload job description (PDF or TXT)", type=["pdf", "txt"])
        if custom_jd_file:
            st.success("Custom job description uploaded!")
            custom_jd = custom_jd_file
    
    if not upload_jd:
        st.info(f"Required skills: {', '.join(role_requirements[role])}")
        st.markdown(f"<p>Cutoff Score for selection: <b>{75}/100</b></p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return role, custom_jd



def resume_upload_section():
    st.markdown("""
    <div class="card">
        <h3>📄 Upload Your Resume</h3>
        <p>Supported format: PDF</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_resume = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    
    return uploaded_resume



def create_score_pie_chart(score):
    """Create a professional pie chart for the score visualization"""
    fig, ax = plt.subplots(figsize=(4, 4), facecolor='#111111')
    
    # Data
    sizes = [score, 100 - score]
    labels = ['', '']  # We'll use annotation instead
    colors = ["#d32f2f", "#333333"]
    explode = (0.05, 0)  # explode the 1st slice (Score)
    
    # Plot
    wedges, texts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors,
        explode=explode, 
        startangle=90,
        wedgeprops={'width': 0.5, 'edgecolor': 'black', 'linewidth': 1}
    )
    
    # Draw a circle in the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.25, fc='#111111')
    ax.add_artist(centre_circle)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_aspect('equal')
    
    # Add score text in the center
    ax.text(0, 0, f"{score}%", 
            ha='center', va='center', 
            fontsize=24, fontweight='bold', 
            color='white')
    
    # Add pass/fail indicator
    status = "PASS" if score >= 75 else "FAIL"
    status_color = "#4CAF50" if score >= 75 else "#d32f2f"
    ax.text(0, -0.15, status, 
            ha='center', va='center', 
            fontsize=14, fontweight='bold', 
            color=status_color)
    
    # Set the background color
    ax.set_facecolor('#111111')
    
    return fig




def display_analysis_results(analysis_result):
    if not analysis_result:
        return

    overall_score = analysis_result.get('overall_score', 0)
    selected = analysis_result.get("selected", False)
    skill_scores = analysis_result.get("skill_scores", {})
    detailed_weaknesses = analysis_result.get("detailed_weaknesses", [])

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align: right; font-size: 0.8rem; color: #888; margin-bottom: 10px;">Powered by Euron Recruitment</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Overall Score", f"{overall_score}/100")
        fig = create_score_pie_chart(overall_score)
        st.pyplot(fig)

    with col2:
        if selected:
            st.markdown("<h2 style='color:#4CAF50;'>✅ Congratulations! You have been shortlisted.</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#d32f2f;'>❌ Unfortunately, you were not selected.</h2>", unsafe_allow_html=True)
        st.write(analysis_result.get('reasoning', ''))

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<div class="strengths-improvements">', unsafe_allow_html=True)

    # Strengths
    st.markdown('<div>', unsafe_allow_html=True)
    st.subheader("🌟 Strengths")
    strengths = analysis_result.get("strengths", [])
    if strengths:
        for skill in strengths:
            st.markdown(f'<div class="skill-tag">{skill} ({skill_scores.get(skill, "N/A")}/10)</div>', unsafe_allow_html=True)
    else:
        st.write("No notable strengths identified.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Weaknesses
    
    st.markdown('<div>', unsafe_allow_html=True)
    st.subheader("🚩 Areas for Improvement")
    missing_skills = analysis_result.get("missing_skills", [])
    if missing_skills:
        for skill in missing_skills:
            st.markdown(f'<div class="skill-tag missing">{skill} ({skill_scores.get(skill, "N/A")}/10)</div>', unsafe_allow_html=True)
    else:
        st.write("No significant areas for improvement.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed weaknesses section
    if detailed_weaknesses:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("📊 Detailed Weakness Analysis")
        
        for weakness in detailed_weaknesses:
            skill_name = weakness.get('skill', '')
            score = weakness.get('score', 0)
            
            with st.expander(f"{skill_name} (Score: {score}/10)"):
                # Clean detail display
                detail = weakness.get('detail', 'No specific details provided.')
                # Clean JSON formatting if it appears in the text
                if detail.startswith('```json') or '{' in detail:
                    detail = "The resume lacks examples of this skill."
                
                st.markdown(f'<div class="weakness-detail"><strong>Issue:</strong> {detail}</div>', 
                           unsafe_allow_html=True)
                
                # Display improvement suggestions if available
                if 'suggestions' in weakness and weakness['suggestions']:
                    st.markdown("<strong>How to improve:</strong>", unsafe_allow_html=True)
                    for i, suggestion in enumerate(weakness['suggestions']):
                        st.markdown(f'<div class="solution-detail">{i+1}. {suggestion}</div>', 
                                   unsafe_allow_html=True)
                
                # Display example if available
                if 'example' in weakness and weakness['example']:
                    st.markdown("<strong>Example addition:</strong>", unsafe_allow_html=True)
                    st.markdown(f'<div class="example-detail">{weakness["example"]}</div>', 
                               unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        report_content = f"""
# Euron Recruitment - Resume Analysis Report

## Overall Score: {overall_score}/100

Status: {"✅ Shortlisted" if selected else "❌ Not Selected"}

## Analysis Reasoning
{analysis_result.get('reasoning', 'No reasoning provided.')}

## Strengths
{", ".join(strengths if strengths else ["None identified"])}

## Areas for Improvement
{", ".join(missing_skills if missing_skills else ["None identified"])}

## Detailed Weakness Analysis
"""
        # Add detailed weaknesses to report
        for weakness in detailed_weaknesses:
            skill_name = weakness.get('skill', '')
            score = weakness.get('score', 0)
            detail = weakness.get('detail', 'No specific details provided.')
            
            # Clean JSON formatting if it appears in the text
            if detail.startswith('```json') or '{' in detail:
                detail = "The resume lacks examples of this skill."
                
            report_content += f"\n### {skill_name} (Score: {score}/10)\n"
            report_content += f"Issue: {detail}\n"
            
            # Add suggestions to report
            if 'suggestions' in weakness and weakness['suggestions']:
                report_content += "\nImprovement suggestions:\n"
                for i, sugg in enumerate(weakness['suggestions']):
                    report_content += f"- {sugg}\n"
            
            # Add example to report
            if 'example' in weakness and weakness['example']:
                report_content += f"\nExample: {weakness['example']}\n"
            
        report_content += "\n---\nAnalysis provided by TechSeva IT Recruitment Agent.AI"
        
        report_b64 = base64.b64encode(report_content.encode()).decode()
        href = f'<a class="download-btn" href="data:text/plain;base64,{report_b64}" download="euron_resume_analysis.txt">📊 Download Analysis Report</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)





def resume_qa_section(has_resume, ask_question_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Ask Questions About the Resume")
    user_question = st.text_input("Enter your question about the resume:", placeholder="What is the candidate's most recent experience?")
    
    if user_question and ask_question_func:
        with st.spinner("Searching resume and generating response..."):
            response = ask_question_func(user_question)
            
            st.markdown('<div style="background-color: #111122; padding: 15px; border-radius: 5px; border-left: 5px solid #d32f2f;">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Add example questions
    with st.expander("Example Questions"):
        example_questions = [
            "What is the candidate's most recent role?",
            "How many years of experience does the candidate have with Python?",
            "What educational qualifications does the candidate have?",
            "What are the candidate's key achievements?",
            "Has the candidate managed teams before?",
            "What projects has the candidate worked on?",
            "Does the candidate have experience with cloud technologies?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"q_{question}"):
                st.session_state.current_question = question
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def interview_questions_section(has_resume, generate_questions_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        question_types = st.multiselect(
            "Select question types:",
            ["Basic", "Technical", "Experience", "Scenario", "Coding", "Behavioral"],
            default=["Basic", "Technical"]
        )
    
    with col2:
        difficulty = st.select_slider(
            "Question difficulty:",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
    
    num_questions = st.slider("Number of questions:", 3, 15, 5)
    
    if st.button("Generate Interview Questions"):
        if generate_questions_func:
            with st.spinner("Generating personalized interview questions..."):
                questions = generate_questions_func(question_types, difficulty, num_questions)
                
                # Create content for download
                download_content = f"# Euron Recruitment - Interview Questions\n\n"
                download_content += f"Difficulty: {difficulty}\n"
                download_content += f"Types: {', '.join(question_types)}\n\n"
                
                for i, (q_type, question) in enumerate(questions):
                    with st.expander(f"{q_type}: {question[:50]}..."):
                        st.write(question)
                        
                        # For coding questions, add code editor
                        if q_type == "Coding":
                            st.code("# Write your solution here", language="python")
                    
                    # Add to download content
                    download_content += f"## {i+1}. {q_type} Question\n\n"
                    download_content += f"{question}\n\n"
                    if q_type == "Coding":
                        download_content += "```python\n# Write your solution here\n```\n\n"
                
                # Add Euron branding to download content
                download_content += "\n---\nQuestions generated by TechSeva IT Recruitment Agent.AI"
                
                # Add download button
                if questions:
                    st.markdown("---")
                    questions_bytes = download_content.encode()
                    b64 = base64.b64encode(questions_bytes).decode()
                    href = f'<a class="download-btn" href="data:text/markdown;base64,{b64}" download="euron_interview_questions.md">📝 Download All Questions</a>'
                    st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def resume_improvement_section(has_resume, improve_resume_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    improvement_areas = st.multiselect(
        "Select areas to improve:",
        ["Content", "Format", "Skills Highlighting", "Experience Description", "Education", "Projects", "Achievements", "Overall Structure"],
        default=["Content", "Skills Highlighting"]
    )
    
    target_role = st.text_input("Target role (optional):", placeholder="e.g., Senior Data Scientist at Google")
    
    if st.button("Generate Resume Improvements"):
        if improve_resume_func:
            with st.spinner("Analyzing and generating improvements..."):
                improvements = improve_resume_func(improvement_areas, target_role)
                
                # Create content for download
                download_content = f"# Euron Recruitment - Resume Improvement Suggestions\n\nTarget Role: {target_role if target_role else 'Not specified'}\n\n"
                
                for area, suggestions in improvements.items():
                    with st.expander(f"Improvements for {area}", expanded=True):
                        st.markdown(f"<p>{suggestions['description']}</p>", unsafe_allow_html=True)
                        
                        st.subheader("Specific Suggestions")
                        for i, suggestion in enumerate(suggestions["specific"]):
                            st.markdown(f'<div class="solution-detail"><strong>{i+1}.</strong> {suggestion}</div>', unsafe_allow_html=True)
                        
                        if "before_after" in suggestions:
                            st.markdown('<div class="comparison-container">', unsafe_allow_html=True)
                            
                            st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                            st.markdown("<strong>Before:</strong>", unsafe_allow_html=True)
                            st.markdown(f"<pre>{suggestions['before_after']['before']}</pre>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                            st.markdown("<strong>After:</strong>", unsafe_allow_html=True) 
                            st.markdown(f"<pre>{suggestions['before_after']['after']}</pre>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add to download content
                    download_content += f"## Improvements for {area}\n\n"
                    download_content += f"{suggestions['description']}\n\n"
                    download_content += "### Specific Suggestions\n\n"
                    for i, suggestion in enumerate(suggestions["specific"]):
                        download_content += f"{i+1}. {suggestion}\n"
                    download_content += "\n"
                    
                    if "before_after" in suggestions:
                        download_content += "### Before\n\n"
                        download_content += f"```\n{suggestions['before_after']['before']}\n```\n\n"
                        download_content += "### After\n\n"
                        download_content += f"```\n{suggestions['before_after']['after']}\n```\n\n"
                
                # Add Euron branding to download content
                download_content += "\n---\nProvided by TechSeva IT Recruitment Agent.AI"
                
                # Add download button
                st.markdown("---")
                report_bytes = download_content.encode()
                b64 = base64.b64encode(report_bytes).decode()
                href = f'<a class="download-btn" href="data:text/markdown;base64,{b64}" download="euron_resume_improvements.md">📝 Download All Suggestions</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def improved_resume_section(has_resume, get_improved_resume_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    target_role = st.text_input("Target role:", placeholder="e.g., Senior Software Engineer")
    highlight_skills = st.text_area("Paste your JD to get updated Resume", placeholder="e.g., Python, React, Cloud Architecture")
    
    if st.button("Generate Improved Resume"):
        if get_improved_resume_func:
            with st.spinner("Creating improved resume..."):
                improved_resume = get_improved_resume_func(target_role, highlight_skills)
                
                st.subheader("Improved Resume")
                st.text_area("", improved_resume, height=400)
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    # Text file download
                    resume_bytes = improved_resume.encode()
                    b64 = base64.b64encode(resume_bytes).decode()
                    href = f'<a class="download-btn" href="data:file/txt;base64,{b64}" download="euron_improved_resume.txt">📄 Download as TXT</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
                with col2:
                    # Markdown file download
                    md_content = f"""# {target_role if target_role else 'Professional'} Resume

{improved_resume}

---
Resume enhanced by TechSeva IT Recruitment Agent.AI
"""
                    md_bytes = md_content.encode()
                    md_b64 = base64.b64encode(md_bytes).decode()
                    md_href = f'<a class="download-btn" href="data:text/markdown;base64,{md_b64}" download="euron_improved_resume.md">📝 Download as Markdown</a>'
                    st.markdown(md_href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_tabs():
    return st.tabs([
        "Resume Analysis", 
        "Resume Q&A", 
        "Interview Questions", 
        "Resume Improvement", 
        "Improved Resume"
    ])