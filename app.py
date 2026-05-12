import streamlit as st
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Return & Refund Assistant",
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

.chat-container {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.user-box {
    background-color: #1E293B;
}

.bot-box {
    background-color: #111827;
}

.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🤖 Return & Refund Assistant")
st.caption("AI-powered customer support system")

# =========================
# SIDEBAR SETTINGS
# =========================
with st.sidebar:

    st.header("⚙️ Company Settings")

    company_name = st.text_input(
        "Company Name",
        value="ShopEasy"
    )

    refund_days = st.slider(
        "Refund Window",
        1,
        30,
        7
    )

    support_email = st.text_input(
        "Support Email",
        value="support@shopeasy.com"
    )

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# RESPONSE ENGINE
# =========================
def generate_response(user_query):

    query = user_query.lower()

    greetings = [
        "Hello 👋 How can I help you today?",
        "Hi there! Need help with returns or refunds?",
        "Welcome! Tell me your issue."
    ]

    # GREETING
    if any(word in query for word in ["hi", "hello", "hey"]):
        return random.choice(greetings)

    # REFUND STATUS
    elif "refund" in query and "status" in query:
        return f"""
Your refund is usually processed within 5 business days.

If the refund is delayed, contact:
📧 {support_email}
"""

    # RETURN POLICY
    elif "return policy" in query or "return" in query:
        return f"""
📦 Return Policy for {company_name}

✅ Products can be returned within {refund_days} days.

✅ Items must be unused and in original packaging.

✅ Damaged products are eligible for full refund.
"""

    # DAMAGED PRODUCT
    elif "damaged" in query or "broken" in query:
        return f"""
We're sorry your product arrived damaged.

✅ You are eligible for:
- Full refund
- Replacement
- Return shipping support

Please contact:
📧 {support_email}
"""

    # CANCEL ORDER
    elif "cancel" in query:
        return """
Orders can only be cancelled before shipping.

If already shipped:
- You can initiate a return request after delivery.
"""

    # DIGITAL PRODUCTS
    elif "digital" in query:
        return """
❌ Digital products are non-refundable once purchased.
"""

    # SHIPPING
    elif "shipping" in query:
        return """
🚚 Standard shipping takes 3-7 business days.

Express shipping takes 1-2 business days.
"""

    # DEFAULT RESPONSE
    else:
        return f"""
I couldn't fully understand your request.

Please contact our support team:

📧 {support_email}

Or ask about:
- Refund status
- Return policy
- Damaged items
- Shipping
- Order cancellation
"""

# =========================
# DISPLAY CHAT
# =========================
for msg in st.session_state.messages:

    role_class = "user-box" if msg["role"] == "user" else "bot-box"

    st.markdown(
        f"""
        <div class="chat-container {role_class}">
        <b>{msg["role"].capitalize()}:</b><br><br>
        {msg["content"]}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# CHAT INPUT
# =========================
user_input = st.chat_input(
    "Ask about refunds, returns, shipping..."
)

# =========================
# PROCESS MESSAGE
# =========================
if user_input:

    # SAVE USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # GENERATE BOT RESPONSE
    response = generate_response(user_input)

    # SAVE BOT RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
