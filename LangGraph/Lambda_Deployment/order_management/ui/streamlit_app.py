# =============================================================
# Streamlit shopping UI — AnyCart
#   - Category image gallery (one image per catalog category)
#   - Product cards with modern styling
#   - Chat window (talks to the LangGraph agent via Lambda)
# Run:  streamlit run ui/streamlit_app.py  (from ordermgmt/)
# =============================================================

import os
import streamlit as st

from catalog import PRODUCTS, FEATURED_PRODUCTS, format_price, all_categories

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")

st.set_page_config(page_title="AnyCart", page_icon="🛒", layout="wide")


# ------------------------------------------------------------------
# Agent integration — invokes the deployed Lambda function
# ------------------------------------------------------------------
import json
import boto3

LAMBDA_ARN = "arn:aws:lambda:us-east-1:<ACCOUNT_ID>:function:eCommerce-app"  #1 Update with your AWS Lambda ARN
lambda_client = boto3.client("lambda", region_name="us-east-1")

def assistant_reply(text: str) -> str:
    """Invoke the LangGraph agent via AWS Lambda."""
    response = lambda_client.invoke(
        FunctionName=LAMBDA_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps({"message": text}).encode("utf-8"),
    )
    payload = json.loads(response["Payload"].read())
    # Handle both direct response and nested body formats
    if isinstance(payload, dict):
        if "response" in payload:
            return payload["response"]
        if "body" in payload:
            body = payload["body"]
            if isinstance(body, str):
                body = json.loads(body)
            return body.get("response", str(body))
        if "error" in payload:
            return f"Error: {payload['error']}"
    return str(payload)


# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

      html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
      }

      /* Hero banner */
      .hero-banner {
        background: linear-gradient(135deg, #232F3E 0%, #37475A 50%, #FF9900 100%);
        border-radius: 20px;
        padding: 36px 44px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
      }
      .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: rgba(255,153,0,0.15);
        border-radius: 50%;
      }
      .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
      }
      .hero-sub {
        color: #FFE0B2;
        font-size: 16px;
        margin-top: 0;
        opacity: 0.9;
      }

      /* Section headers */
      .category-header {
        font-size: 22px;
        font-weight: 700;
        color: #232F3E;
        margin-bottom: 16px;
      }

      /* Product cards */
      .prod-card {
        border: none;
        border-radius: 16px;
        padding: 22px;
        background: #FFFFFF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
        height: 280px;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #F0F2F5;
      }
      .prod-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.1);
        border-color: #FF9900;
      }
      .prod-id {
        background: linear-gradient(135deg, #FF9900, #FFB84D);
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 10px;
      }
      .prod-name {
        font-weight: 700;
        color: #1B2638;
        font-size: 17px;
        margin: 4px 0;
        line-height: 1.3;
      }
      .prod-category {
        color: #7A8695;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        font-weight: 600;
      }
      .prod-price {
        color: #232F3E;
        font-weight: 800;
        font-size: 22px;
      }
      .prod-desc {
        color: #5B6B7F;
        font-size: 13px;
        margin-top: auto;
        padding-top: 10px;
        line-height: 1.5;
      }

      /* Category buttons */
      .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid #E0E4EA;
        transition: all 0.2s ease;
      }
      .stButton > button:hover {
        background: #FF9900;
        color: #FFFFFF;
        border-color: #FF9900;
      }

      /* Sidebar */
      [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #232F3E 0%, #1A2433 100%);
      }
      [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
      }
      [data-testid="stSidebar"] .stRadio label {
        color: #FFE0B2 !important;
      }
      [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1);
      }

      /* Chat area */
      .chat-header {
        font-size: 20px;
        font-weight: 700;
        color: #232F3E;
        margin-bottom: 12px;
        padding-bottom: 12px;
        border-bottom: 2px solid #FF9900;
        display: inline-block;
      }

      [data-testid="stChatInput"] {
        border-radius: 12px;
        border: 1px solid #E0E4EA;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
      }
      [data-testid="stChatInput"]:focus-within {
        border-color: #FF9900;
        box-shadow: 0 0 0 3px rgba(255,153,0,0.12);
      }

      /* Chat messages */
      [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 12px 16px;
      }

      /* Divider */
      hr {
        border: none;
        border-top: 1px solid #F0F2F5;
        margin: 20px 0;
      }

      /* Hide streamlit branding */
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Hey! I'm your AnyCart shopping assistant."
                    "I can recommend products, place orders, or track existing ones. How can I help?"}
    ]
if "category" not in st.session_state:
    st.session_state.category = "All"

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛒 AnyCart")
    st.caption("AI-powered multi-agent shopping")
    st.markdown("---")
    cats = ["All"] + all_categories()
    st.session_state.category = st.radio("Browse categories", cats,
                                         index=cats.index(st.session_state.category))
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("Featured", len(FEATURED_PRODUCTS))
    col2.metric("Catalog", len(PRODUCTS))
    st.markdown("---")
    st.markdown("**Powered by**")
    st.markdown("Amazon Bedrock | LangGraph | DynamoDB")

# ------------------------------------------------------------------
# Hero banner
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
      <div class="hero-title">🛒 AnyCart</div>
      <div class="hero-sub">Your AI-powered shopping experience — browse, discover, and order with a conversational agent.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Layout: catalog (left) + chat (right)
# ------------------------------------------------------------------
left, right = st.columns([2, 1], gap="large")

with left:
    # ---- Category image gallery
    st.markdown('<div class="category-header">Shop by Category</div>', unsafe_allow_html=True)
    cat_list = all_categories()
    cols = st.columns(len(cat_list))
    for col, cat in zip(cols, cat_list):
        with col:
            img_path = os.path.join(IMG_DIR, f"{cat.lower()}.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            if st.button(f"{cat}", key=f"cat_{cat}", use_container_width=True):
                st.session_state.category = cat
                st.rerun()

    st.markdown("---")

    # ---- Product grid (featured items only)
    st.markdown('<div class="category-header">Featured Picks</div>', unsafe_allow_html=True)

    per_row = 3
    shown = FEATURED_PRODUCTS
    for i in range(0, len(shown), per_row):
        row = st.columns(per_row)
        for col, p in zip(row, shown[i:i + per_row]):
            with col:
                st.markdown(
                    f"""
                    <div class="prod-card">
                      <span class="prod-id">{p['product_id']}</span>
                      <div class="prod-name">{p['name']}</div>
                      <div class="prod-category">{p['category']}</div>
                      <div class="prod-price">{format_price(p['price'])}</div>
                      <div class="prod-desc">{p['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write("")

with right:
    st.markdown('<span class="chat-header">💬 AI Assistant</span>', unsafe_allow_html=True)

    # message history
    chat_box = st.container(height=620)
    with chat_box:
        for msg in st.session_state.messages:
            avatar = "🧑" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                # Handle content that may be a list (LangGraph message format) or string
                raw_content = msg["content"]
                if isinstance(raw_content, list):
                    # Extract text from list of content blocks
                    parts = []
                    for block in raw_content:
                        if isinstance(block, dict) and "text" in block:
                            parts.append(block["text"])
                        elif isinstance(block, str):
                            parts.append(block)
                    content = "\n".join(parts)
                else:
                    content = str(raw_content)
                # Format order confirmation messages nicely
                import re as _re
                import ast as _ast

                order_match = _re.search(
                    r"Order placed!\s*Details:\s*(\{.*\})", content
                )
                status_match = _re.search(
                    r"status:\s*(\{.*\})", content, _re.IGNORECASE
                )

                if order_match:
                    try:
                        details = _ast.literal_eval(order_match.group(1))
                        order_id = details.get("order_id", "N/A")
                        prefix = content[: order_match.start()].strip()
                        if prefix:
                            st.markdown(prefix)
                        st.success("Order placed successfully!")
                        st.code(order_id, language=None)
                        st.caption("Order ID — save this to track your order.")
                    except Exception:
                        content = content.replace("$", "\\$")
                        st.markdown(content)
                elif status_match:
                    try:
                        details = _ast.literal_eval(status_match.group(1))
                        order_id = details.get("order_id", "N/A")
                        status = details.get("status", "Unknown")
                        quantity = details.get("quantity")

                        lines = [f"**Status:** {status}", f"**Order ID:** `{order_id}`"]
                        if quantity:
                            lines.append(f"**Quantity:** {quantity}")
                        st.markdown("\n\n".join(lines))
                    except Exception:
                        content = content.replace("$", "\\$")
                        st.markdown(content)
                else:
                    # Escape dollar signs so Streamlit doesn't render them as LaTeX
                    content = content.replace("$", "\\$")
                    st.markdown(content)

    # input
    prompt = st.chat_input("Ask about products, place an order, or track one...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            reply = assistant_reply(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
