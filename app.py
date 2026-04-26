import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Professional Tech Design
st.set_page_config(page_title="Chinchan Core", page_icon="⚡", layout="centered")

# Custom CSS for the "Ultra-Tech" aesthetic
st.markdown("""
    <style>
    /* Main Background with a deep space theme */
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #0a0a12 100%);
        color: #e0e0e0;
    }

    /* Neon Glowing Title with Typewriter Animation */
    .tech-header {
        font-family: 'Share Tech Mono', monospace;
        color: #00f2ff;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        text-align: center;
        border: 2px solid #00f2ff;
        padding: 20px;
        background: rgba(0, 242, 255, 0.05);
        border-radius: 5px;
        margin-bottom: 30px;
    }

    /* Chat Bubbles with Glassmorphism and Neon Accents */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px);
        border-left: 5px solid #00f2ff !important;
        border-radius: 0px 15px 15px 0px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    /* Styling the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #00f2ff;
    }

    /* Neon Sidebar Status */
    .status-text {
        color: #39FF14;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
    }

    /* Custom Input Box */
    .stChatInputContainer {
        border: 1px solid #00f2ff !important;
        border-radius: 5px !important;
        background-color: #050505 !important;
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# 2. Tech Header Section
st.markdown('<div class="tech-header">CHINCHAN_CORE_v2.0 // STATUS: ENCRYPTED</div>', unsafe_allow_html=True)

# Tech Robot Visual
# Replace the old st.image section with this "Digital Heartbeat"
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
        <div style="
            width: 100px; 
            height: 100px; 
            background-color: #00f2ff; 
            border-radius: 50%; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            font-size: 50px;
            box-shadow: 0 0 20px #00f2ff;
            animation: pulse 2s infinite;">
            🤖
        </div>
    </div>

    <style>
    @keyframes pulse {
        0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0, 242, 255, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0, 242, 255, 0); }
        100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0, 242, 255, 0); }
    }
    </style>
""", unsafe_allow_html=True)
# 3. Sidebar System Panel
st.sidebar.markdown('<h2 style="color:#00f2ff; font-family:Share Tech Mono;">🔐 AUTHENTICATION</h2>',
                    unsafe_allow_html=True)
api_key = st.sidebar.text_input("ENTER_API_KEY:", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="status-text">● CORE_SYSTEM: ONLINE</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="status-text">● NETWORK: SECURE</p>', unsafe_allow_html=True)
st.sidebar.info("Chinchan is currently utilizing Gemini-2.5-Flash processing.")

# 4. Session State (The Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display History with Tech Icons
for message in st.session_state.messages:
    # Chinchan gets a robot icon, you get a user icon
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. Interaction Logic
if user_input := st.chat_input("Enter command for Chinchan..."):

    if not api_key:
        st.warning("SYSTEM_ERROR: API_KEY_REQUIRED. Please provide authentication in the sidebar.")
    else:
        # Show User Input
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Connect to AI
        client = genai.Client(api_key=api_key)

        with st.chat_message("assistant", avatar="🤖"):
            # Prepare memory for AI
            formatted_history = []
            for msg in st.session_state.messages:
                role = "model" if msg["role"] == "assistant" else "user"
                formatted_history.append({"role": role, "parts": [{"text": msg["content"]}]})

            # --- THE SAFETY NET STARTS HERE ---
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction="Your name is Chinchan. You are a high-tech robotic intelligence. You are logical, extremely clever, and helpful. Use a few tech-related words like 'Processing', 'Data verified', or 'Analyzing', but keep your tone friendly and cool."
                    )
                )
                # If successful, show the message and save it to memory
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                # If the server is busy, show this warning instead of crashing
                st.error("🚦 CONNECTION_TIMEOUT: Google servers are at max capacity. Retrying in 15s...")
            # --- THE SAFETY NET ENDS HERE ---