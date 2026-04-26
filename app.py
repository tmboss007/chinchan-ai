import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Design
st.set_page_config(page_title="Chinchan Core", page_icon="⚡", layout="centered")

# Custom CSS for the "Ultra-Tech" aesthetic
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #050505 0%, #0a0a12 100%); color: #e0e0e0; }
    .tech-header {
        font-family: 'Share Tech Mono', monospace; color: #00f2ff; text-align: center;
        border: 2px solid #00f2ff; padding: 20px; background: rgba(0, 242, 255, 0.05);
        border-radius: 5px; margin-bottom: 30px; text-shadow: 0 0 10px #00f2ff;
    }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important; border-left: 5px solid #00f2ff !important;
        border-radius: 0px 15px 15px 0px !important; margin-bottom: 20px;
    }
    .status-text { color: #39FF14; font-family: 'Share Tech Mono', monospace; font-weight: bold; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown('<div class="tech-header">CHINCHAN_CORE_v2.0 // STATUS: ENCRYPTED</div>', unsafe_allow_html=True)

# 3. Sidebar
st.sidebar.markdown('<h2 style="color:#00f2ff;">🔐 AUTHENTICATION</h2>', unsafe_allow_html=True)
api_key = st.sidebar.text_input("ENTER_API_KEY:", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="status-text">● CORE_SYSTEM: ONLINE</p>', unsafe_allow_html=True)

# 4. Session State (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display History
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. Interaction Logic
if user_input := st.chat_input("Enter command for Chinchan..."):
    if not api_key:
        st.warning("SYSTEM_ERROR: API_KEY_REQUIRED.")
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            client = genai.Client(api_key=api_key)
            
            # Format history for Chinchan
            history = []
            for msg in st.session_state.messages:
                role = "model" if msg["role"] == "assistant" else "user"
                history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

            with st.chat_message("assistant", avatar="🤖"):
                response = client.models.generate_content(
                    model='gemini-2.0-flash', # Using the stable 2026 workhorse model
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction="Your name is Chinchan. You are a robotic intelligence. Be logical and tech-focused."
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            # The specific "Wait 10 minutes" logic you requested
            st.error("🚦 CONNECTION_TIMEOUT: Google servers are currently at max capacity. Please wait 10 minutes and try again.")
