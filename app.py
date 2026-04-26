import streamlit as st
import requests
from streamlit_lottie import st_lottie
from google import genai
from google.genai import types
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Chinchan Core AI", page_icon="⚡", layout="centered")

# --- 2. MOTION GRAPHICS LOADER ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# High-tech robotic animation
lottie_robot = load_lottieurl("https://lottie.host/8026117d-2965-4f74-8833-8991a030f296/FmGk1s7mQG.json")

# --- 3. ULTRA-TECH & SHINCHAN DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Main Tech Background */
    .stApp {
        background: radial-gradient(circle at top, #0a0a12 0%, #000000 100%);
        color: #e0e0e0;
    }

    /* Shinchan-style Tech Header */
    .tech-header {
        font-family: 'Share Tech Mono', monospace;
        background: linear-gradient(90deg, #ff4d4d, #fdfd96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 50px;
        font-weight: 800;
        border: 2px solid #00f2ff;
        padding: 15px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        margin-bottom: 20px;
    }

    /* Animated Chat Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-left: 5px solid #ff4d4d !important;
        border-radius: 10px !important;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateX(10px);
        border-left: 5px solid #00f2ff !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #ff4d4d;
    }

    .status-online { color: #39FF14; font-weight: bold; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- 4. HEADER & ANIMATION ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_robot:
        st_lottie(lottie_robot, height=180, key="main_robot")
    else:
        st.write("🤖")

with col2:
    st.markdown('<div class="tech-header">CHINCHAN CORE</div>', unsafe_allow_html=True)
    st.write("🤖 **SYSTEM V2.0 // ROBOTIC INTELLIGENCE**")

# --- 5. SIDEBAR AUTHENTICATION ---
st.sidebar.markdown('<h2 style="color:#ff4d4d;">🔐 ACCESS CONTROL</h2>', unsafe_allow_html=True)
api_key = st.sidebar.text_input("ENTER_GENAI_KEY:", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown('🌐 STATUS: <span class="status-online">CONNECTED</span>', unsafe_allow_html=True)
st.sidebar.info("Shinchan theme active. AI: Gemini-2.0-Flash.")

# --- 6. SESSION MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 7. CHAT LOGIC ---
if user_input := st.chat_input("Input command for Chinchan..."):
    
    if not api_key:
        st.warning("⚠️ AUTH_REQUIRED: Please enter your API Key in the sidebar.")
    else:
        # User input
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            client = genai.Client(api_key=api_key)
            
            # Prepare memory
            history = []
            for msg in st.session_state.messages:
                role = "model" if msg["role"] == "assistant" else "user"
                history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

            with st.chat_message("assistant", avatar="🤖"):
                # Processing animation
                with st.spinner("ANALYZING DATA..."):
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction="Your name is Chinchan. You are a clever, high-tech robotic intelligence. You are helpful but have a cool, slightly cheeky tech vibe. Use words like 'Processing', 'Scanning', or 'System Optimized'."
                        )
                    )
                
                # Show AI output
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            # Server Busy / Error Logic
            st.error("🚦 SYSTEM_OVERLOAD: Servers are at max capacity. Please wait 10 minutes and try again.")
            st.toast("Connection Error: Retrying in 600s...", icon="⚠️")
