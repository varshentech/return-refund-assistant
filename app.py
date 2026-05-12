import streamlit as st
from groq import Groq

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Return & Refund Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.stTextInput input {
    border-radius: 10px;
}

.chat-box {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.user-msg {
    background-color: #1E293B;
}

.bot-msg {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🤖 AI Return & Refund Assistant")
st.caption("Smart AI-powered customer support assistant")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ Settings")

    company_name = st.text_input(
        "Company Name",
        value="ShopEasy"
    )

    refund_days = st.slider(
        "Refund Window (Days)",
        1,
        30,
        7
    )

    support_email = st.text_input(
        "Support Email",
        value="support@shopeasy.com"
    )

# =========================
# GROQ CLIENT
# =========================
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = f"""
You are a professional AI customer support assistant for {company_name}.

Company Policies:
- Customers can return products within {refund_days} days.
- Refunds take 5 business days.
- Damaged products get full refunds.
- Digital products are non-refundable.
- Support Email: {support_email}

Rules:
- Be professional.
- Give clear refund guidance.
- Help users solve issues.
- Answer in a friendly tone.
- Keep responses concise but useful.
"""

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT
# =========================
for msg in st.session_state.messages:

    role_class = "user-msg" if msg["role"] == "user" else "bot-msg"

    st.markdown(
        f"""
        <div class="chat-box {role_class}">
        <b>{msg["role"].capitalize()}:</b><br>
        {msg["content"]}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# USER INPUT
# =========================
user_input = st.chat_input(
    "Ask about refunds, returns, damaged products..."
)

# =========================
# PROCESS INPUT
# =========================
if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Build conversation
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    conversation.extend(st.session_state.messages)

    # AI RESPONSE
    with st.spinner("Thinking..."):

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=conversation,
            temperature=0.5,
            max_tokens=500
        )

        ai_reply = response.choices[0].message.content

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()
