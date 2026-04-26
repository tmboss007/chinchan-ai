import streamlit as st
import requests
from streamlit_lottie import st_lottie
from google import genai
from google.genai import types
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Chinchan Core AI", page_icon="⚡", layout="centered")

# --- 2. BOOT-UP SEQUENCE ---
if "booted" not in st.session_state:
    st.toast("Booting Chinchan Core...", icon="⚡")
    time.sleep(0.4)
    st.toast("Establishing Secure Node...", icon="🔐")
    time.sleep(0.4)
    st.toast("Neural Networks Loaded.", icon="🧠")
    time.sleep(0.3)
    st.toast("Systems Online.", icon="🟢")
    st.session_state.booted = True

# --- 3. MOTION GRAPHICS LOADER ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_robot = load_lottieurl("https://lottie.host/8026117d-2965-4f74-8833-8991a030f296/FmGk1s7mQG.json")

# --- 4. PERSONALITY SYSTEM PROMPTS ---
PERSONALITIES = {
    "🎭 Shinchan": "You are Chinchan, an AI with the playful, mischievous personality of Shinchan Nohara. You're funny, cheeky, and sometimes say silly things, but you're secretly very smart. Use casual language, throw in jokes, and occasionally reference Shinchan catchphrases. Still give helpful and accurate answers.",
    "💼 Professional": "You are Chinchan Core AI, a professional and efficient assistant. Give clear, concise, and well-structured responses. Use formal language and focus on accuracy and helpfulness.",
    "🎨 Creative": "You are Chinchan Core AI in Creative Mode. You think outside the box, use vivid metaphors, and approach problems from unique angles. Your responses are imaginative, inspiring, and full of creative energy.",
    "💻 Coder": "You are Chinchan Core AI in Coder Mode. You are an expert programmer. Always provide clean, well-commented code with explanations. Use code blocks, mention best practices, and suggest optimizations. You think like a senior software engineer.",
}

# --- 5. ADVANCED CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

    .stApp {
        background-color: #050510;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(255, 77, 77, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 50%, rgba(0, 242, 255, 0.04) 0%, transparent 50%),
            linear-gradient(rgba(0, 242, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 242, 255, 0.04) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
        animation: scrollGrid 30s linear infinite;
        will-change: background-position;
        color: #e0e0e0;
    }

    @keyframes scrollGrid {
        0% { background-position: 0 0, 0 0, 0px 0px, 0px 0px; }
        100% { background-position: 0 0, 0 0, 28px 28px, 28px 28px; }
    }

    /* Scanline — static overlay for performance */
    .stApp::after {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.08) 0px,
            rgba(0, 0, 0, 0.08) 1px,
            transparent 1px,
            transparent 4px
        );
        z-index: 998;
        pointer-events: none;
    }

    /* Header */
    .tech-header {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #ff4d4d, #ff8c42, #fdfd96, #00f2ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 3px;
        padding: 18px;
        border: 2px solid rgba(0, 242, 255, 0.3);
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.15), inset 0 0 30px rgba(255, 77, 77, 0.05);
        animation: gradientShift 4s ease infinite;
        will-change: background-position;
        position: relative;
        z-index: 10;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #00f2ff;
        text-align: center;
        font-size: 13px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 8px;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }

    /* Chat Bubbles — GPU-accelerated smooth transitions */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.9), rgba(15, 15, 30, 0.8)) !important;
        border-left: 4px solid #ff4d4d !important;
        border-radius: 12px !important;
        box-shadow: 0 0 15px rgba(255, 77, 77, 0.1), 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: fadeSlideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
        position: relative;
        z-index: 10;
        margin-bottom: 12px !important;
        backdrop-filter: blur(10px);
        transition: transform 0.35s cubic-bezier(0.25, 0.8, 0.25, 1),
                    box-shadow 0.35s cubic-bezier(0.25, 0.8, 0.25, 1),
                    border-color 0.35s ease;
        will-change: transform;
    }

    [data-testid="stChatMessage"]:nth-child(even) {
        border-left: 4px solid #00f2ff !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1), 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stChatMessage"]:hover {
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.3), 0 8px 30px rgba(0, 0, 0, 0.4);
        transform: translateX(4px) scale(1.005);
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(12px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06060f 0%, #0a0a18 50%, #06060f 100%) !important;
        border-right: 2px solid rgba(255, 77, 77, 0.4);
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
        letter-spacing: 2px;
    }

    .sidebar-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }

    .status-online { color: #39FF14; font-weight: bold; text-shadow: 0 0 8px rgba(57, 255, 20, 0.5); }

    .stat-value {
        font-family: 'Share Tech Mono', monospace;
        color: #00f2ff;
        font-size: 22px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
    }

    .stat-label {
        font-family: 'Share Tech Mono', monospace;
        color: #888;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Chat Input */
    [data-testid="stBottomBlockContainer"] {
        z-index: 9999 !important;
        background: linear-gradient(180deg, transparent, #050510 30%) !important;
        padding-top: 20px !important;
        padding-bottom: 15px !important;
    }

    .stChatInputContainer {
        border: 1px solid rgba(0, 242, 255, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1) !important;
        background: rgba(10, 10, 20, 0.9) !important;
    }

    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 10px 0;
    }

    .typing-indicator .dot {
        width: 8px;
        height: 8px;
        background: #00f2ff;
        border-radius: 50%;
        animation: typingBounce 1.4s ease-in-out infinite;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.5);
    }

    .typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }

    /* Quick Prompt Buttons */
    .prompt-chip {
        display: inline-block;
        background: rgba(0, 242, 255, 0.08);
        border: 1px solid rgba(0, 242, 255, 0.25);
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 13px;
        color: #00f2ff;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .prompt-chip:hover {
        background: rgba(0, 242, 255, 0.15);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        transform: translateY(-2px);
    }

    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(255, 77, 77, 0.08), rgba(0, 242, 255, 0.08));
        border: 1px solid rgba(0, 242, 255, 0.15);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        animation: fadeSlideIn 0.6s ease-out;
    }

    .welcome-card h3 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #ff4d4d, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 22px;
        margin-bottom: 10px;
    }

    .welcome-card p {
        font-family: 'Share Tech Mono', monospace;
        color: #999;
        font-size: 14px;
    }

    /* Timestamp */
    .msg-time {
        font-family: 'Share Tech Mono', monospace;
        font-size: 10px;
        color: #555;
        text-align: right;
        margin-top: 5px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #050510; }
    ::-webkit-scrollbar-thumb { background: #ff4d4d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #00f2ff; }

    /* Button overrides */
    .stButton > button {
        font-family: 'Share Tech Mono', monospace;
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 8px;
        background: rgba(0, 242, 255, 0.05);
        color: #00f2ff;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: rgba(0, 242, 255, 0.15);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        border-color: #00f2ff;
        color: #fff;
    }

    .stDownloadButton > button {
        font-family: 'Share Tech Mono', monospace;
        border: 1px solid rgba(57, 255, 20, 0.3);
        background: rgba(57, 255, 20, 0.05);
        color: #39FF14;
    }

    .stDownloadButton > button:hover {
        background: rgba(57, 255, 20, 0.15);
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.3);
    }

    </style>
""", unsafe_allow_html=True)

# --- 6. HEADER LAYOUT ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_robot:
        st_lottie(lottie_robot, height=150, key="main_robot")
    else:
        st.markdown("<h1 style='text-align: center;'>🤖</h1>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="tech-header">CHINCHAN CORE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">▸ Robotic Intelligence System V2.0 ◂</div>', unsafe_allow_html=True)

# --- 7. SIDEBAR ---
st.sidebar.markdown('<h2 style="color:#ff4d4d;">🔐 ACCESS CONTROL</h2>', unsafe_allow_html=True)
api_key = st.sidebar.text_input("GENAI_API_KEY:", type="password", help="Enter your Google Gemini API key")
st.sidebar.markdown("---")

# Personality Mode
st.sidebar.markdown('<h2 style="color:#00f2ff;">🧠 PERSONALITY MODE</h2>', unsafe_allow_html=True)
personality = st.sidebar.selectbox(
    "Select AI Persona:",
    list(PERSONALITIES.keys()),
    index=0,
    help="Choose how Chinchan responds"
)

# Temperature Slider
st.sidebar.markdown('<h2 style="color:#00f2ff;">🌡️ CREATIVITY LEVEL</h2>', unsafe_allow_html=True)
temperature = st.sidebar.slider(
    "Temperature:", min_value=0.0, max_value=2.0, value=0.8, step=0.1,
    help="Higher = more creative, Lower = more focused"
)

st.sidebar.markdown("---")

# Status & Stats
st.sidebar.markdown('<h2 style="color:#00f2ff;">📊 SESSION STATS</h2>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

total_msgs = len(st.session_state.messages)
user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
ai_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
total_words = sum(len(m["content"].split()) for m in st.session_state.messages)

stats_col1, stats_col2 = st.sidebar.columns(2)
with stats_col1:
    st.markdown(f'<div class="stat-value">{total_msgs}</div><div class="stat-label">Messages</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{user_msgs}</div><div class="stat-label">Your Msgs</div>', unsafe_allow_html=True)
with stats_col2:
    st.markdown(f'<div class="stat-value">{total_words}</div><div class="stat-label">Words</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{ai_msgs}</div><div class="stat-label">AI Msgs</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# Connection Status
status = "CONNECTED" if api_key else "AWAITING KEY"
status_class = "status-online" if api_key else ""
status_icon = "🟢" if api_key else "🟡"
st.sidebar.markdown(f'{status_icon} STATUS: <span class="{status_class}">{status}</span>', unsafe_allow_html=True)
st.sidebar.markdown(f"**Mode:** {personality}")
st.sidebar.markdown(f"**Model:** Gemini 2.0 Flash")
st.sidebar.markdown(f"**Temp:** {temperature}")

st.sidebar.markdown("---")

# Action Buttons
col_clear, col_export = st.sidebar.columns(2)
with col_clear:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with col_export:
    if st.session_state.messages:
        export_text = f"# Chinchan Core — Chat Export\n"
        export_text += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        export_text += f"**Mode:** {personality}\n\n---\n\n"
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Chinchan"
            ts = msg.get("time", "")
            export_text += f"**{role}** ({ts}):\n{msg['content']}\n\n---\n\n"
        st.download_button(
            "📥 Export",
            data=export_text,
            file_name=f"chinchan_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

# --- 8. CHAT DISPLAY ---
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "time" in message:
            st.markdown(f'<div class="msg-time">{message["time"]}</div>', unsafe_allow_html=True)

# --- 9. WELCOME MESSAGE & QUICK PROMPTS ---
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-card">
            <h3>⚡ Welcome to Chinchan Core</h3>
            <p>Your cyberpunk AI companion is online and ready.<br>
            Enter your API key in the sidebar, then start chatting below.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**💡 Try a quick prompt:**")
    prompt_cols = st.columns(2)
    quick_prompts = [
        "Explain quantum computing simply",
        "Write a Python snake game",
        "Tell me a joke, Shinchan style",
        "Create a workout plan for beginners",
    ]
    for i, qp in enumerate(quick_prompts):
        with prompt_cols[i % 2]:
            if st.button(f"▸ {qp}", key=f"qp_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": qp,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

# --- 10. CHAT INPUT & GEMINI API ---
def call_gemini_with_retry(client, history_contents, system_prompt, temp, max_retries=3):
    """Call Gemini API with automatic retry on rate limit errors."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=history_contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temp,
                ),
            )
            return response, None
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 15  # 15s, 30s, 45s
                    st.toast(f"⏳ Rate limited. Retrying in {wait_time}s... (attempt {attempt + 2}/{max_retries})", icon="🔄")
                    time.sleep(wait_time)
                    continue
                else:
                    return None, "rate_limit"
            else:
                return None, error_str
    return None, "unknown"


if prompt := st.chat_input("Enter command..."):
    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        st.markdown(f'<div class="msg-time">{now}</div>', unsafe_allow_html=True)

    # Generate AI Response
    with st.chat_message("assistant", avatar="🤖"):
        if not api_key:
            error_msg = "⚠️ **ACCESS DENIED** — Enter your Gemini API key in the sidebar to activate Chinchan Core."
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg, "time": now})
        else:
            # Typing indicator
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
                <div class="typing-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <span style="font-family: 'Share Tech Mono', monospace; color: #555; margin-left: 8px; font-size: 12px;">
                        Chinchan is thinking...
                    </span>
                </div>
            """, unsafe_allow_html=True)

            try:
                client = genai.Client(api_key=api_key)

                # Build conversation history for context
                history_contents = []
                system_prompt = PERSONALITIES[personality]

                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history_contents.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    ))

                response, error = call_gemini_with_retry(
                    client, history_contents, system_prompt, temperature
                )

                typing_placeholder.empty()

                if error == "rate_limit":
                    rate_msg = (
                        "⏳ **RATE LIMIT REACHED** — Your free-tier Gemini API quota is exhausted.\n\n"
                        "**What you can do:**\n"
                        "- ⏰ **Wait 1-2 minutes** and try again\n"
                        "- 🔑 **Upgrade** to a paid plan at [ai.google.dev](https://ai.google.dev)\n"
                        "- 📊 **Check usage** at [ai.dev/rate-limit](https://ai.dev/rate-limit)\n\n"
                        "_Chinchan tried 3 times automatically before showing this._"
                    )
                    st.markdown(rate_msg)
                    st.session_state.messages.append({"role": "assistant", "content": rate_msg, "time": now})
                elif error:
                    error_msg = f"❌ **SYSTEM ERROR:** {error}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg, "time": now})
                else:
                    reply = response.text
                    resp_time = datetime.now().strftime("%H:%M")
                    st.markdown(reply)
                    st.markdown(f'<div class="msg-time">{resp_time}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": reply, "time": resp_time})

            except Exception as e:
                typing_placeholder.empty()
                error_msg = f"❌ **SYSTEM ERROR:** {str(e)}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "time": now})
