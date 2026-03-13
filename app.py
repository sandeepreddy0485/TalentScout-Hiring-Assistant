import os
import json
import re
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from utils import (
    is_exit_command,
    validate_input,
    parse_tech_stack,
    collect_candidate_value,
    save_candidate,
    generate_questions_for_tech_stack,
    analyze_sentiment,
)
from prompt_templates import (
    GREETING_TEXT,
    EXIT_TEXT,
    CONFUSED_TEXT,
    THANK_YOU_TEXT,
    ABOUT_TEXT,
)

load_dotenv()

CANDIDATE_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "candidates.json")

FIELDS = [
    ("full_name", "Full Name", "Please enter your full name"),
    ("email", "Email Address", "Please enter your email address"),
    ("phone", "Phone Number", "Please enter your phone number"),
    ("experience", "Years of Experience", "How many years of experience do you have?"),
    ("position", "Desired Position(s)", "What position(s) are you applying for?"),
    ("location", "Current Location", "Where are you currently located?"),
    ("tech_stack", "Tech Stack", "List your tech stack (e.g., Python, Django, React, SQL)"),
]


def apply_custom_css():
    """Apply modern, vibrant CSS with hidden footer and attractive purple-blue gradient."""
    st.markdown("""
    <style>
        /* Import a modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* HIDE THE STREAMLIT FOOTER */
        footer {display: none !important;}
        
        /* Main container – soft gradient background */
        .main {
            background: linear-gradient(135deg, #f5f0ff 0%, #ffffff 100%);
        }
        
        /* Header – vibrant purple-blue gradient */
        .header-title {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }
        
        .header-subtitle {
            font-size: 1rem;
            color: #5f6b7a;
            margin-bottom: 1.8rem;
            font-weight: 400;
            border-bottom: 1px solid #e0d9ff;
            padding-bottom: 1rem;
        }
        
        /* Sidebar cards – white with vibrant left accent */
        .info-card {
            background: white;
            padding: 14px 16px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(106,17,203,0.08), 0 1px 2px rgba(0,0,0,0.05);
            border-left: 4px solid #6a11cb;
            margin-bottom: 12px;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
        }
        .info-card:hover {
            box-shadow: 0 8px 20px rgba(106,17,203,0.15);
        }
        
        /* Status badge – purple-blue gradient */
        .status-badge {
            display: inline-block;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 6px rgba(106,17,203,0.3);
        }
        
        /* Sentiment badges – updated colors */
        .sentiment-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 8px;
        }
        .sentiment-positive {
            background-color: #d9f0e1;
            color: #1f7b4d;
        }
        .sentiment-neutral {
            background-color: #fff3cd;
            color: #856404;
        }
        .sentiment-negative {
            background-color: #f8d7da;
            color: #a12b3a;
        }
        
        /* Chat message avatars – use brand colors */
        [data-testid="chatAvatarIcon-assistant"] {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
        }
        [data-testid="chatAvatarIcon-user"] {
            background: #6a11cb;
        }
        
        /* Chat bubbles */
        .stChatMessageContent {
            border-radius: 20px !important;
            padding: 12px 18px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            max-width: 75% !important;
        }
        /* Assistant bubbles: light gray */
        .stChatMessage:nth-child(odd) .stChatMessageContent {
            background-color: #f0f2f5 !important;
            color: #1a1e24 !important;
            border-bottom-left-radius: 4px !important;
        }
        /* User bubbles: vibrant purple-blue gradient */
        .stChatMessage:nth-child(even) .stChatMessageContent {
            background: linear-gradient(135deg, #6a11cb, #2575fc) !important;
            color: white !important;
            border-bottom-right-radius: 4px !important;
        }
        
        /* Input field – subtle border, focus with purple glow */
        .stTextInput > div > div > input {
            border-radius: 30px !important;
            border: 1px solid #d0bfff !important;
            padding: 12px 20px !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 6px rgba(106,17,203,0.05) !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #6a11cb !important;
            box-shadow: 0 0 0 3px rgba(106,17,203,0.15) !important;
        }
        
        /* Submit button – vibrant gradient */
        .stButton > button {
            border-radius: 30px !important;
            background: linear-gradient(135deg, #6a11cb, #2575fc) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 10px 24px !important;
            box-shadow: 0 4px 10px rgba(106,17,203,0.3) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 18px rgba(106,17,203,0.4) !important;
        }
        
        /* Progress bar – match gradient */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #6a11cb, #2575fc) !important;
        }
        
        /* Sidebar headers */
        .css-1d391kg p, .css-1d391kg h3 {
            font-weight: 600;
            color: #1e2b3c;
        }
    </style>
    """, unsafe_allow_html=True)


def greeting():
    st.session_state.state["messages"].append({
        "sender": "assistant",
        "text": GREETING_TEXT,
        "time": datetime.now().strftime("%H:%M")
    })


def handle_user_input(text: str):
    # Always check for exit command first
    if is_exit_command(text):
        st.session_state.state["messages"].append({
            "sender": "user",
            "text": text,
            "time": datetime.now().strftime("%H:%M")
        })
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": EXIT_TEXT,
            "time": datetime.now().strftime("%H:%M")
        })
        st.session_state.state["ended"] = True
        return

    # ------------------- Q&A MODE -------------------
    if st.session_state.state.get("qa_mode", False):
        qa_questions = st.session_state.state["qa_questions"]
        qa_index = st.session_state.state["qa_index"]
        qa_answers = st.session_state.state["qa_answers"]

        # Add user answer
        st.session_state.state["messages"].append({
            "sender": "user",
            "text": text,
            "time": datetime.now().strftime("%H:%M")
        })

        # Store the answer
        current_q = qa_questions[qa_index]
        qa_answers.append({
            "tech": current_q["tech"],
            "question": current_q["question"],
            "answer": text
        })
        st.session_state.state["qa_answers"] = qa_answers

        # Move to next question
        next_index = qa_index + 1
        if next_index < len(qa_questions):
            st.session_state.state["qa_index"] = next_index
            next_q = qa_questions[next_index]
            st.session_state.state["messages"].append({
                "sender": "assistant",
                "text": f"**{next_q['tech']}** – {next_q['question']}",
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            # All questions answered – save and finish
            st.session_state.state["candidate"]["answers"] = qa_answers
            st.session_state.state["candidate"]["timestamp"] = datetime.utcnow().isoformat() + "Z"
            save_candidate(CANDIDATE_DB_PATH, st.session_state.state["candidate"])

            st.session_state.state["messages"].append({
                "sender": "assistant",
                "text": THANK_YOU_TEXT,
                "time": datetime.now().strftime("%H:%M")
            })
            st.session_state.state["ended"] = True
            st.session_state.state["qa_mode"] = False
        return

    # ------------------- INFORMATION GATHERING MODE -------------------
    field_key, _, prompt_text = FIELDS[st.session_state.state["step"]]
    current_candidate = st.session_state.state["candidate"]

    if not validate_input(field_key, text):
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": CONFUSED_TEXT,
            "time": datetime.now().strftime("%H:%M")
        })
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": prompt_text,
            "time": datetime.now().strftime("%H:%M")
        })
        return

    st.session_state.state["messages"].append({
        "sender": "user",
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    })

    sentiment = analyze_sentiment(text)
    st.session_state.state["last_sentiment"] = sentiment

    if "uncertain" in sentiment or "Negative" in sentiment:
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": "Take your time, there's no rush. Just answer as best you can.",
            "time": datetime.now().strftime("%H:%M")
        })

    value = collect_candidate_value(field_key, text)
    current_candidate[field_key] = value

    st.session_state.state["step"] += 1

    if st.session_state.state["step"] < len(FIELDS):
        next_prompt = FIELDS[st.session_state.state["step"]][2]
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": next_prompt,
            "time": datetime.now().strftime("%H:%M")
        })
    else:
        tech_stack_items = parse_tech_stack(current_candidate.get("tech_stack", ""))
        current_candidate["tech_stack_items"] = tech_stack_items

        with st.spinner("Generating tailored technical questions..."):
            question_blocks = generate_questions_for_tech_stack(tech_stack_items)

        # Flatten questions for sequential asking
        flat_questions = []
        for tech, qlist in question_blocks.items():
            for q in qlist:
                flat_questions.append({"tech": tech, "question": q})

        st.session_state.state["qa_mode"] = True
        st.session_state.state["qa_questions"] = flat_questions
        st.session_state.state["qa_index"] = 0
        st.session_state.state["qa_answers"] = []

        current_candidate["generated_questions"] = question_blocks

        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": "Thanks! Now let's go through the technical questions one by one. Please provide your answers.",
            "time": datetime.now().strftime("%H:%M")
        })

        # Ask first question
        first_q = flat_questions[0]
        st.session_state.state["messages"].append({
            "sender": "assistant",
            "text": f"**{first_q['tech']}** – {first_q['question']}",
            "time": datetime.now().strftime("%H:%M")
        })


def render_messages():
    """Display all messages using Streamlit's native chat components with avatars."""
    for msg in st.session_state.state["messages"]:
        # Determine avatar based on sender
        avatar = "🤖" if msg["sender"] == "assistant" else "👤"
        with st.chat_message(msg["sender"], avatar=avatar):
            # Display message text and optional timestamp
            if "time" in msg:
                st.markdown(f"{msg['text']}\n\n<span style='font-size:0.7rem; color:#8e9aaf;'>{msg['time']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(msg["text"])


def show_candidate_summary():
    if "candidate" not in st.session_state.state:
        return
    candidate = st.session_state.state["candidate"]
    if not candidate:
        return

    st.markdown("---")
    st.subheader("📋 Candidate Summary")
    
    sentiment = st.session_state.state.get("last_sentiment", "Not analyzed")
    sentiment_class = "sentiment-neutral"
    if "Positive" in sentiment:
        sentiment_class = "sentiment-positive"
    elif "Negative" in sentiment or "uncertain" in sentiment:
        sentiment_class = "sentiment-negative"
    
    # Candidate basic info – grid layout with icons
    st.markdown(f"""
    <div style='background:white; border-radius:20px; padding:20px; box-shadow:0 8px 24px rgba(106,17,203,0.1); margin-bottom:20px;'>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:16px;'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>👤</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Full Name</span><br><span style='font-weight:600;'>{candidate.get("full_name", "—")}</span></div>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>📧</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Email</span><br><span style='font-weight:600;'>{candidate.get("email", "—")}</span></div>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>📞</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Phone</span><br><span style='font-weight:600;'>{candidate.get("phone", "—")}</span></div>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>⏳</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Experience</span><br><span style='font-weight:600;'>{candidate.get("experience", "—")} years</span></div>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>💼</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Desired Position</span><br><span style='font-weight:600;'>{candidate.get("position", "—")}</span></div>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>📍</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Location</span><br><span style='font-weight:600;'>{candidate.get("location", "—")}</span></div>
            </div>
            <div style='grid-column:span 2; display:flex; align-items:center; gap:8px;'>
                <span style='font-size:1.3rem;'>🛠️</span>
                <div><span style='color:#5f6b7a; font-size:0.9rem;'>Tech Stack</span><br><span style='font-weight:600;'>{candidate.get("tech_stack", "—")}</span></div>
            </div>
        </div>
        <div style='margin-top:16px; display:flex; gap:12px; align-items:center;'>
            <span class="sentiment-badge {sentiment_class}">{sentiment}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Answers section – collapsible if many answers
    if "answers" in candidate and candidate["answers"]:
        with st.expander("💬 View Answers Provided", expanded=False):
            # Group answers by technology for better organization
            answers_by_tech = {}
            for ans in candidate["answers"]:
                tech = ans["tech"]
                if tech not in answers_by_tech:
                    answers_by_tech[tech] = []
                answers_by_tech[tech].append(ans)
            
            for tech, tech_answers in answers_by_tech.items():
                st.markdown(f"### {tech}")
                for idx, ans in enumerate(tech_answers, 1):
                    st.markdown(f"""
                    <div style='background:white; border-radius:16px; padding:16px; margin:12px 0; box-shadow:0 4px 12px rgba(106,17,203,0.05); border-left:4px solid #6a11cb;'>
                        <div style='display:flex; gap:12px; align-items:flex-start;'>
                            <span style='background:#6a11cb; color:white; width:24px; height:24px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:0.9rem; font-weight:600;'>{idx}</span>
                            <div style='flex:1;'>
                                <p style='margin:0 0 8px 0; font-weight:500; color:#1e2b3c;'>{ans['question']}</p>
                                <p style='margin:0; color:#2575fc; font-weight:400; background:#f5f0ff; padding:10px; border-radius:12px;'><span style='font-weight:600;'>Answer:</span> {ans['answer']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No answers recorded.")


def main():
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        layout="wide",
        page_icon="🤖",
        initial_sidebar_state="expanded"
    )
    
    apply_custom_css()
    
    if "state" not in st.session_state:
        st.session_state.state = {
            "step": 0,
            "candidate": {},
            "messages": [],
            "ended": False,
            "last_sentiment": "Neutral tone.",
            "qa_mode": False,
            "qa_questions": [],
            "qa_index": 0,
            "qa_answers": [],
        }
        greeting()
    
    with st.sidebar:
        st.markdown("### 📋 Progress")
        total_steps = len(FIELDS)
        current_step = st.session_state.state["step"]
        if st.session_state.state.get("qa_mode", False):
            qa_total = len(st.session_state.state["qa_questions"])
            qa_current = st.session_state.state["qa_index"]
            progress = (qa_current / qa_total) if qa_total > 0 else 0
            st.progress(progress)
            st.markdown(f"<span class='status-badge'>Q&A {qa_current+1}/{qa_total}</span>", unsafe_allow_html=True)
        else:
            progress = min(current_step / total_steps, 1.0) if total_steps > 0 else 1.0
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(progress)
            with col2:
                st.markdown(f"<span class='status-badge'>{current_step}/{total_steps}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📝 Candidate Info")
        
        candidate = st.session_state.state["candidate"]
        for field_key, label, _ in FIELDS:
            value = candidate.get(field_key, "—")
            st.markdown(f"<div class='info-card'><strong>{label}</strong><br>{value}</div>", unsafe_allow_html=True)
        
        sentiment = st.session_state.state.get("last_sentiment", "")
        if sentiment:
            st.markdown("### 😶‍🌫️ Sentiment")
            st.info(sentiment)
        
        st.markdown("---")
        if st.session_state.state["ended"]:
            if st.button("🔄 Restart Session", key="restart", use_container_width=True):
                st.session_state.pop("state")
                st.experimental_rerun()
    
    # Main chat area
    st.markdown("<div class='header-title'>🤖 TalentScout</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Intelligent Tech Recruiter · AI-Powered Screening</div>", unsafe_allow_html=True)
    
    if st.session_state.state["ended"]:
        st.success("✅ Interview Complete!")
        st.markdown("---")
        render_messages()
        st.markdown("---")
        show_candidate_summary()
        return
    
    # Chat messages area
    chat_space = st.container()
    with chat_space:
        render_messages()
    
    # Spacing for fixed input
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    
    # Fixed input area at bottom
    st.markdown("---")
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Your response",
                placeholder="Type your answer here...",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send ➤", use_container_width=True)
        
        if submitted and user_input:
            handle_user_input(user_input.strip())
            st.experimental_rerun()


if __name__ == "__main__":
    main()