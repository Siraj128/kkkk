import streamlit as st
import time
import random
import pandas as pd
import user_logic as ul
import jwt

# Configure the page
st.set_page_config(page_title="QuizMaster Live", page_icon="🎯", layout="wide")

# ENHANCED: Complete styling for entire platform with OAuth integration
st.markdown("""
<style>
    /* Hide Streamlit branding for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Beautiful gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* OAuth Login Container */
    .login-container, .profile-setup-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    
    /* ENHANCED: Beautiful gradient buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        text-transform: none;
        letter-spacing: 0.5px;
    }
    
    /* Hover effect with beautiful animation */
    .stButton > button:hover {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 50%, #FF6B6B 100%);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Beautiful shimmer effect on hover */
    .stButton > button:hover::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 0.8s ease-in-out;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Special styling for primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B6B 100%);
        font-size: 18px;
        padding: 18px 35px;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFD700 50%, #FFA500 100%);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.6);
        transform: translateY(-5px) scale(1.08);
    }
    
    /* Glass morphism containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 20px 0;
        position: relative;
    }
    
    /* Animated title */
    .main-title {
        text-align: center;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: bold;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .main-title:hover {
        transform: scale(1.05);
        text-shadow: 0 0 20px #FFD700;
    }
    
    /* Dashboard cards with hover effects */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        cursor: pointer;
    }
    
    .dashboard-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-color: #FFD700;
        background: rgba(255, 255, 255, 0.25);
    }
    
    /* Statistics cards */
    .stat-card {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        cursor: pointer;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) rotate(2deg);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        border: 2px solid #FFD700;
    }
    
    /* Form input hover effects */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        transition: all 0.3s ease;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:hover {
        border: 2px solid #FFD700;
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        transform: scale(1.02);
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #4ECDC4;
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 25px rgba(78, 205, 196, 0.4);
    }
    
    /* Success/Error message hover effects */
    .stSuccess {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        border-radius: 15px;
        padding: 15px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stSuccess:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 8px 20px rgba(86, 171, 47, 0.4);
    }
    
    /* Pulsing animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Quiz interface styles */
    .quiz-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .question-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Leaderboard styles */
    .leaderboard-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: black;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(255, 215, 0, 0.4);
    }
    
    .podium-place {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 10px;
    }
    
    .podium-place:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .podium-first {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: black;
        border: 3px solid #FFD700;
        height: 200px;
    }
    
    .podium-second {
        background: linear-gradient(135deg, #C0C0C0, #808080);
        color: white;
        border: 3px solid #C0C0C0;
        height: 160px;
    }
    
    .podium-third {
        background: linear-gradient(135deg, #CD7F32, #8B4513);
        color: white;
        border: 3px solid #CD7F32;
        height: 120px;
    }
    
    .player-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .player-card:hover {
        transform: translateX(10px) scale(1.02);
        border-color: #FFD700;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .player-you {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: 2px solid #FFD700;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    }
    
    .stat-box {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        margin: 10px;
    }
    
    .stat-box:hover {
        transform: translateY(-5px) rotate(2deg);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'page' not in st.session_state: 
    st.session_state.page = 'login'
if 'token' not in st.session_state: 
    st.session_state.token = None
if 'user_record' not in st.session_state: 
    st.session_state.user_record = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Quiz-specific session state
def initialize_quiz_state():
    """Initialize quiz session state"""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'quiz_questions' not in st.session_state:
        QUIZ_QUESTIONS = [
            {"id": 1, "question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correct": 2, "explanation": "Paris is the capital and most populous city of France."},
            {"id": 2, "question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "correct": 1, "explanation": "Mars appears red due to iron oxide (rust) on its surface."},
            {"id": 3, "question": "What is 15 + 27?", "options": ["40", "41", "42", "43"], "correct": 2, "explanation": "15 + 27 = 42. Don't panic, it's also the answer to everything!"},
            {"id": 4, "question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"], "correct": 2, "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503-1519."},
            {"id": 5, "question": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "correct": 3, "explanation": "The Pacific Ocean covers about 46% of Earth's water surface."},
            {"id": 6, "question": "Which programming language is known for web development?", "options": ["Python", "JavaScript", "C++", "Java"], "correct": 1, "explanation": "JavaScript is the primary language for web development."},
            {"id": 7, "question": "What does 'AI' stand for?", "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Intelligence", "Algorithmic Intelligence"], "correct": 1, "explanation": "AI stands for Artificial Intelligence."},
            {"id": 8, "question": "Which year did the first iPhone launch?", "options": ["2006", "2007", "2008", "2009"], "correct": 1, "explanation": "The first iPhone was launched by Apple in 2007."},
            {"id": 9, "question": "What is the speed of light?", "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s"], "correct": 0, "explanation": "The speed of light in vacuum is approximately 300,000 km/s."},
            {"id": 10, "question": "Which element has the chemical symbol 'O'?", "options": ["Gold", "Oxygen", "Iron", "Silver"], "correct": 1, "explanation": "Oxygen has the chemical symbol 'O' on the periodic table."}
        ]
        st.session_state.quiz_questions = random.sample(QUIZ_QUESTIONS, min(5, len(QUIZ_QUESTIONS)))
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False

# --- Page Navigation ---
def go_to_page(page_name): 
    st.session_state.page = page_name

def go_to_quiz_page(page_name):
    st.session_state.current_page = page_name

# --- OAuth Component ---
try:
    CLIENT_ID = st.secrets["google_credentials"]["client_id"]
    CLIENT_SECRET = st.secrets["google_credentials"]["client_secret"]
    REDIRECT_URI = "http://localhost:8501"
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, "https://accounts.google.com/o/oauth2/v2/auth", "https://oauth2.googleapis.com/token", "https://oauth2.googleapis.com/token", "https://oauth2.googleapis.com/revoke")
    OAUTH_AVAILABLE = True
except Exception as e:
    OAUTH_AVAILABLE = False
    st.error("⚠️ Google OAuth not configured. Using demo mode.")

# Quiz Functions
def show_quiz_page():
    """Quiz interface with questions and scoring"""
    initialize_quiz_state()
    
    # Back button
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("""
    <div class="quiz-container">
        <h1 style="text-align: center; color: #FFD700;">🎯 Quiz Challenge</h1>
        <p style="text-align: center; font-size: 1.2rem;">Test your knowledge and compete with others!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.quiz_started:
        # Quiz start screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="question-card">
                <h2 style="text-align: center;">🚀 Ready to Start?</h2>
                <div style="text-align: center; margin: 30px 0;">
                    <h3>📋 Quiz Details:</h3>
                    <p>• <strong>5 Questions</strong> randomly selected</p>
                    <p>• <strong>Multiple choice</strong> format</p>
                    <p>• <strong>Instant feedback</strong> on each answer</p>
                    <p>• <strong>Final score</strong> and performance analysis</p>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <h3>🎯 Tips for Success:</h3>
                    <p>• Read questions carefully</p>
                    <p>• Trust your first instinct</p>
                    <p>• Stay calm and focused</p>
                    <p>• Learn from explanations</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎯 Start Quiz Challenge", use_container_width=True, type="primary"):
                st.session_state.quiz_started = True
                st.balloons()
                st.rerun()
    
    elif st.session_state.quiz_completed:
        # Quiz results
        total_questions = len(st.session_state.quiz_questions)
        final_score = st.session_state.quiz_score
        accuracy = (final_score / total_questions) * 100
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFD700, #FFA500); 
                    border-radius: 20px; padding: 40px; text-align: center; 
                    color: black; margin: 30px 0; box-shadow: 0 15px 35px rgba(255, 215, 0, 0.4);">
            <h1>🎉 Quiz Completed!</h1>
            <h2>Congratulations on finishing the challenge!</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(45deg, #4ECDC4, #44A08D); 
                        border-radius: 15px; padding: 30px; text-align: center; 
                        color: white; margin: 20px 0;">
                <h2>📊 Final Results</h2>
                <h1 style="font-size: 4rem; margin: 20px 0;">{final_score}/{total_questions}</h1>
                <h3>Accuracy: {accuracy:.1f}%</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if accuracy == 100:
                st.success("🏆 PERFECT SCORE! You're a quiz master!")
                st.markdown("🎖️ **Achievement Unlocked**: Perfect Game")
            elif accuracy >= 80:
                st.success("🌟 EXCELLENT! Outstanding performance!")
                st.markdown("🏅 **Achievement Unlocked**: Quiz Expert")
            elif accuracy >= 60:
                st.info("👍 GOOD JOB! Solid performance!")
                st.markdown("🥉 **Achievement Unlocked**: Quiz Apprentice")
            else:
                st.warning("📚 KEEP PRACTICING! You'll do better next time!")
                st.markdown("📖 **Tip**: Review the explanations below")
            
            # Detailed answers review
            st.markdown("### 📝 Answer Review")
            
            for i, answer in enumerate(st.session_state.answers, 1):
                if answer['is_correct']:
                    st.success(f"**Q{i}**: {answer['question']}")
                    st.markdown(f"✅ Your answer: **{answer['selected']}** *(Correct!)*")
                else:
                    st.error(f"**Q{i}**: {answer['question']}")
                    if answer['selected'] == 'Skipped':
                        st.markdown(f"⏭️ You skipped this question")
                    else:
                        st.markdown(f"❌ Your answer: **{answer['selected']}**")
                    st.markdown(f"✅ Correct answer: **{answer['correct']}**")
                st.markdown(f"💡 {answer['explanation']}")
                st.markdown("---")
            
            col_restart, col_leaderboard, col_home = st.columns(3)
            
            with col_restart:
                if st.button("🔄 Take Quiz Again", use_container_width=True, type="primary"):
                    for key in ['quiz_started', 'current_question', 'quiz_score', 'answers', 'quiz_questions', 'quiz_completed']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            with col_leaderboard:
                if st.button("🏆 View Leaderboard", use_container_width=True):
                    st.session_state.current_page = "leaderboard"
                    st.rerun()
            
            with col_home:
                if st.button("🏠 Back to Home", use_container_width=True):
                    st.session_state.current_page = "home"
                    st.rerun()
    
    else:
        # Quiz questions
        current_q = st.session_state.quiz_questions[st.session_state.current_question]
        
        # Progress
        progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
        st.progress(progress, f"Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_questions)}")
        
        # Question
        st.markdown(f"""
        <div class="question-card">
            <h2 style="color: #FFD700; margin-bottom: 30px;">
                Q{current_q['id']}: {current_q['question']}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Answers
        col1, col2 = st.columns([1, 2])
        
        with col2:
            selected_answer = st.radio("Choose your answer:", current_q['options'], key=f"q_{st.session_state.current_question}")
            
            col_submit, col_skip = st.columns(2)
            
            with col_submit:
                if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
                    selected_index = current_q['options'].index(selected_answer)
                    is_correct = selected_index == current_q['correct']
                    
                    # Store answer
                    st.session_state.answers.append({
                        'question': current_q['question'],
                        'selected': selected_answer,
                        'correct': current_q['options'][current_q['correct']],
                        'is_correct': is_correct,
                        'explanation': current_q['explanation']
                    })
                    
                    if is_correct:
                        st.session_state.quiz_score += 1
                        st.success(f"🎉 Correct! {current_q['explanation']}")
                        st.balloons()
                    else:
                        st.error(f"❌ Incorrect. The right answer was: {current_q['options'][current_q['correct']]}. {current_q['explanation']}")
                    
                    st.session_state.current_question += 1
                    if st.session_state.current_question >= len(st.session_state.quiz_questions):
                        st.session_state.quiz_completed = True
                    
                    time.sleep(2)
                    st.rerun()
            
            with col_skip:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.answers.append({
                        'question': current_q['question'],
                        'selected': 'Skipped',
                        'correct': current_q['options'][current_q['correct']],
                        'is_correct': False,
                        'explanation': current_q['explanation']
                    })
                    
                    st.session_state.current_question += 1
                    if st.session_state.current_question >= len(st.session_state.quiz_questions):
                        st.session_state.quiz_completed = True
                    
                    st.warning("⏭️ Question skipped!")
                    time.sleep(1)
                    st.rerun()
        
        with col1:
            # Live stats
            st.markdown("### 📊 Your Progress")
            st.metric("Questions Answered", st.session_state.current_question)
            st.metric("Current Score", st.session_state.quiz_score)
            
            if st.session_state.current_question > 0:
                accuracy = (st.session_state.quiz_score / st.session_state.current_question) * 100
                st.metric("Accuracy", f"{accuracy:.1f}%")
            
            # Motivational messages
            if st.session_state.quiz_score == st.session_state.current_question and st.session_state.current_question > 0:
                st.success("🔥 Perfect score so far!")
            elif st.session_state.current_question > 0:
                accuracy = (st.session_state.quiz_score / st.session_state.current_question) * 100
                if accuracy > 80:
                    st.success("🌟 Excellent performance!")
                elif accuracy > 60:
                    st.info("👍 Good job, keep going!")

def show_leaderboard():
    """Beautiful animated leaderboard - FIXED VERSION"""
    
    # Back button
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    
    # Animated header
    st.markdown("""
    <div class="leaderboard-header">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px;">🏆 Global Leaderboard</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Top Quiz Masters from Around the World</p>
        <p style="font-size: 1rem; opacity: 0.8;">🔥 Updated in real-time • Last refresh: Just now</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current user's name safely
    try:
        if st.session_state.user_record and 'name' in st.session_state.user_record:
            current_user_name = st.session_state.user_record['name']
        else:
            current_user_name = "Anonymous Player"
    except:
        current_user_name = "Anonymous Player"
    
    # Create mock leaderboard data with real user
    leaderboard_data = [
        {
            "rank": 1, "name": "QuizMaster Elite", "score": 2850, "games": 47, 
            "accuracy": 95.2, "avg_time": "1.8s", "streak": 15, "badge": "🏆 Legend",
            "country": "🇺🇸", "level": "Grandmaster"
        },
        {
            "rank": 2, "name": "Brain Champion", "score": 2720, "games": 52, 
            "accuracy": 92.8, "avg_time": "2.1s", "streak": 12, "badge": "🥇 Expert",
            "country": "🇬🇧", "level": "Master"
        },
        {
            "rank": 3, "name": str(current_user_name), "score": 2650, "games": 15, 
            "accuracy": 89.5, "avg_time": "2.3s", "streak": 8, "badge": "🎯 Rising Star",
            "country": "🌍", "level": "Expert"
        },
        {
            "rank": 4, "name": "Quiz Ninja", "score": 2490, "games": 41, 
            "accuracy": 85.1, "avg_time": "2.4s", "streak": 7, "badge": "⚡ Fast",
            "country": "🇯🇵", "level": "Advanced"
        },
        {
            "rank": 5, "name": "Smart Cookie", "score": 2380, "games": 29, 
            "accuracy": 82.7, "avg_time": "2.8s", "streak": 4, "badge": "🍪 Sweet",
            "country": "🇦🇺", "level": "Intermediate"
        }
    ]
    
    # Winner's podium (Top 3)
    st.markdown("### 🥇 Champions Podium")
    
    col1, col2, col3 = st.columns(3)
    
    # 2nd Place (Silver)
    with col1:
        second = leaderboard_data[1]
        st.markdown(f"""
        <div class="podium-place podium-second">
            <h2>🥈</h2>
            <h3>{second['name']}</h3>
            <h4>{second['score']} pts</h4>
            <p>{second['accuracy']}% accuracy</p>
            <p>{second['country']} {second['level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 1st Place (Gold) 
    with col2:
        first = leaderboard_data[0]
        st.markdown(f"""
        <div class="podium-place podium-first">
            <h1>👑</h1>
            <h2>{first['name']}</h2>
            <h3>{first['score']} pts</h3>
            <p>{first['accuracy']}% accuracy</p>
            <p>🔥 {first['streak']} win streak</p>
            <p>{first['country']} {first['level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 3rd Place (Bronze) - Current User
    with col3:
        third = leaderboard_data[2]
        st.markdown(f"""
        <div class="podium-place podium-third">
            <h2>🥉</h2>
            <h3>{third['name']} (YOU!)</h3>
            <h4>{third['score']} pts</h4>
            <p>{third['accuracy']}% accuracy</p>
            <p>{third['country']} {third['level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Celebration button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎉 Celebrate Winners!", use_container_width=True, type="primary"):
            st.balloons()
            st.success("🏆 Congratulations to our amazing quiz champions!")
    
    # Complete Rankings
    st.markdown("### 📊 Complete Rankings")
    
    for player in leaderboard_data:
        # FIXED: Safe string comparison
        is_you = str(player['name']) == str(current_user_name)
        card_class = "player-card player-you" if is_you else "player-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3>#{player['rank']} {player['name']} {'👑 (YOU!)' if is_you else ''}</h3>
                    <p>{player['badge']} • {player['country']} {player['level']}</p>
                </div>
                <div style="text-align: right;">
                    <h3 style="color: #FFD700;">{player['score']} pts</h3>
                    <p>{player['accuracy']}% accuracy • {player['avg_time']} avg</p>
                    <p>🔥 {player['streak']} streak • {player['games']} games</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Platform Statistics
    st.markdown("### 📈 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-box">
            <h3>👥</h3>
            <h2>12,847</h2>
            <p>Total Players</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-box" style="background: linear-gradient(135deg, #4ECDC4, #44A08D);">
            <h3>🎯</h3>
            <h2>234,891</h2>
            <p>Questions Answered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-box" style="background: linear-gradient(135deg, #FFD700, #FFA500);">
            <h3>🏆</h3>
            <h2>1,456</h2>
            <p>Competitions Won</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-box" style="background: linear-gradient(135deg, #96CEB4, #FFEAA7);">
            <h3>⚡</h3>
            <h2>2.4s</h2>
            <p>Avg Response Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Take New Quiz", use_container_width=True, type="primary"):
            st.session_state.current_page = "quiz"
            st.rerun()
    
    with col2:
        if st.button("🏆 Challenge Top Player", use_container_width=True):
            st.success("🔥 Challenge sent to QuizMaster Elite!")
    
    with col3:
        if st.button("🎮 Join Tournament", use_container_width=True):
            st.info("🏆 Next tournament starts in 2 hours!")


# =================================================================================================
# === MAIN APP LOGIC ==============================================================================
# =================================================================================================

# --- LOGIN PAGE (INTEGRATED FROM YOUR login_page.py) ---
if st.session_state.page == 'login':
    # Animated header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 class="main-title">🎯 QuizMaster Live</h1>
        <h2 style="color: #FFD700; font-size: 1.8rem; margin: 0;">Interactive Multiplayer Quiz Platform</h2>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-top: 15px;">
            🚀 Join thousands of players in epic quiz battles!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.header("🧠 Welcome to QuizMaster Live!")
        
        if OAUTH_AVAILABLE:
            st.markdown("### 🔐 Secure Authentication with Google")
            
            # OAuth login button (from your login_page.py)
            result = oauth2.authorize_button(
                name="🚀 Sign in with Google",
                icon="https://www.google.com/favicon.ico",
                redirect_uri=REDIRECT_URI,
                scope="openid email profile",
                key="google",
                use_container_width=True
            )
            
            if result:
                st.session_state.token = result.get('token')
                user_record = ul.handle_user_login(st.session_state.token)
                st.session_state.user_record = user_record
                
                if user_record is not None and not user_record['profile_complete']:
                    go_to_page('profile_setup')
                else:
                    go_to_page('authenticated')
                st.rerun()
        else:
            # Demo mode fallback
            st.markdown("### 🎮 Demo Mode Available")
            st.warning("⚠️ Google OAuth not configured. Using demo accounts.")
            
            col_demo1, col_demo2 = st.columns(2)
            
            with col_demo1:
                if st.button("👑 Demo User", use_container_width=True, type="primary"):
                    st.session_state.user_record = {
                        'name': 'Demo Player',
                        'email': 'demo@quizmaster.com',
                        'profile_complete': True
                    }
                    go_to_page('authenticated')
                    st.rerun()
            
            with col_demo2:
                if st.button("🎯 Guest Mode", use_container_width=True):
                    st.session_state.user_record = {
                        'name': 'Anonymous Player',
                        'email': 'guest@quizmaster.com',
                        'profile_complete': True
                    }
                    go_to_page('authenticated')
                    st.rerun()
        
        st.markdown("""
        <div style="margin: 30px 0; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px;">
            <h4>✨ Why Choose QuizMaster Live?</h4>
            <p>🎯 Interactive quizzes with real-time feedback</p>
            <p>🏆 Global leaderboards and competitions</p>  
            <p>🎮 Engaging gameplay with achievements</p>
            <p>📊 Track your progress and improvement</p>
            <p>🔒 Secure authentication with Google OAuth</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- PROFILE SETUP PAGE (INTEGRATED FROM YOUR login_page.py) ---
elif st.session_state.page == 'profile_setup':
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="profile-setup-container">', unsafe_allow_html=True)
        st.header("🛠 Complete Your Profile!")
        st.write("Choose a username that will appear on leaderboards and competitions.")
        
        with st.form("profile_form"):
            new_username = st.text_input(
                "🌟 Public Username", 
                value=st.session_state.user_record['name'],
                help="This name will appear on leaderboards and in competitions"
            )
            submitted = st.form_submit_button("✅ Save and Continue", use_container_width=True, type="primary")
            
            if submitted:
                if ul.complete_profile_setup(st.session_state.user_record['email'], new_username):
                    st.success("🎉 Profile updated successfully!")
                    st.session_state.user_record['profile_complete'] = True
                    st.session_state.user_record['name'] = new_username
                    go_to_page('authenticated')
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Could not update profile. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- AUTHENTICATED MAIN APP ---
elif st.session_state.page == 'authenticated':
    # Handle page navigation within the authenticated app
    if st.session_state.current_page == "quiz":
        show_quiz_page()
    elif st.session_state.current_page == "leaderboard":
        show_leaderboard()
    else:
        # Main dashboard
        username = st.session_state.user_record['name']
        
        # Beautiful sidebar
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 20px; 
                        background: rgba(255,255,255,0.1); 
                        border-radius: 15px; margin-bottom: 20px;">
                <h2>🎯 QuizMaster</h2>
                <p style="opacity: 0.8;">Live Dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"### 👋 Hey {username}!")
            auth_status = "🟢 OAuth Authenticated" if OAUTH_AVAILABLE else "🔶 Demo Mode"
            st.markdown(f"**📊 Status:** {auth_status}")
            st.markdown("---")
            
            # Navigation buttons
            st.markdown("### 🧭 Quick Navigation")
            
            if st.button("🎯 Take Quiz", use_container_width=True, type="primary"):
                st.session_state.current_page = "quiz"
                st.rerun()
            
            if st.button("🏆 Leaderboard", use_container_width=True):
                st.session_state.current_page = "leaderboard"
                st.rerun()
            
            if st.button("📊 My Stats", use_container_width=True):
                st.info("📋 Statistics dashboard coming soon...")
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                go_to_page('login')
                st.success("👋 Logged out successfully!")
                time.sleep(1)
                st.rerun()
        
        # Welcome message
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="background: linear-gradient(45deg, #FFD700, #FFA500); 
                       -webkit-background-clip: text; 
                       -webkit-text-fill-color: transparent; 
                       font-size: 3rem;">
                🎉 Welcome, {username}!
            </h1>
            <p style="font-size: 1.3rem; opacity: 0.8;">
                Ready for an amazing quiz experience with secure authentication!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Live platform stats
        st.markdown("### 📊 Live Platform Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <h3>🔥</h3>
                <h1>127</h1>
                <p>Active Games</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card" style="background: linear-gradient(135deg, #4ECDC4, #44A08D);">
                <h3>👥</h3>
                <h1>2,845</h1>
                <p>Players Online</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card" style="background: linear-gradient(135deg, #FFD700, #FFA500);">
                <h3>⚡</h3>
                <h1>15,439</h1>
                <p>Questions Ready</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-card" style="background: linear-gradient(135deg, #96CEB4, #FFEAA7);">
                <h3>🏆</h3>
                <h1>89</h1>
                <p>Weekly Competitions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Main dashboard
        st.markdown("### 🎮 Your Game Zone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="dashboard-card">
                <h3>🎯 Your Profile</h3>
                <h2 style="color: #4ECDC4; font-size: 2rem; text-align: center;">{username}</h2>
                <p style="text-align: center;">{"Authenticated Player" if OAUTH_AVAILABLE else "Demo Player"}</p>
                <p style="text-align: center; color: #FFD700;">🏆 Ready to compete</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown("### 🚀 Ready to Play?")
            
            if st.button("🎯 Start Quiz Now", use_container_width=True, type="primary"):
                st.session_state.current_page = "quiz"
                st.rerun()
            
            if st.button("🏆 View Rankings", use_container_width=True):
                st.session_state.current_page = "leaderboard"
                st.rerun()
            
            if st.button("🎲 Practice Mode", use_container_width=True):
                st.session_state.current_page = "quiz"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # System status
        st.markdown("### 🎯 System Status")
        if OAUTH_AVAILABLE:
            st.success("✅ Google OAuth: **CONFIGURED & READY**")
            st.success("✅ User Authentication: **ACTIVE**")
        else:
            st.warning("⚠️ OAuth: **DEMO MODE** (Configure secrets.toml for production)")
        st.success("✅ User Profile: **COMPLETE**")
        st.success("✅ Quiz System: **READY**")
        st.success("✅ Leaderboard: **LIVE**")
        st.info("🎮 Status: **READY TO PLAY!**")
