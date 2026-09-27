import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import uuid

from database import init_db
from agent import (
    build_agent,
    get_totals,
    get_category_breakdown,
    get_daily_trend,
    get_all_transactions,
)

st.set_page_config(
    page_title="Finance AI",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #1e1b4b 0%, #0f0c29 35%, #0a0a12 100%);
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1200px;
    }

    /* ---- Hero header ---- */
    .hero {
        background: linear-gradient(120deg, #7c3aed, #ec4899 45%, #f59e0b 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        border-radius: 22px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.35);
    }
    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.3rem;
        color: white;
        margin: 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.25);
    }
    .hero-sub {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin-top: 0.3rem;
    }

    /* ---- Glass metric cards ---- */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }
    .metric-icon { font-size: 1.6rem; }
    .metric-label {
        color: #a5b4fc;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-top: 0.4rem;
    }
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #f9fafb;
        margin-top: 0.1rem;
    }
    .metric-value.income { color: #34d399; }
    .metric-value.expense { color: #fb7185; }
    .metric-value.balance { color: #a78bfa; }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14122b 0%, #0c0b1a 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] h3 {
        font-family: 'Poppins', sans-serif;
        color: #f3f4f6 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #e5e7eb !important;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] small {
        color: #9ca3af !important;
    }
    section[data-testid="stSidebar"] [data-testid="stDataFrame"] * {
        color: #e5e7eb !important;
    }

    /* ---- Section headers ---- */
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #f3f4f6;
        font-size: 1.15rem;
        margin: 1.4rem 0 0.6rem 0;
    }

    /* ---- Chat bubbles ---- */
    .stChatMessage {
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stChatMessage p,
    .stChatMessage span,
    .stChatMessage div {
        color: #f3f4f6 !important;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        color: #f3f4f6 !important;
    }

    /* Dataframe polish */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi there! 👋 Tell me about any expense or income and I'll record it for you."}
    ]

with st.sidebar:
    st.markdown("### 📊 Dashboard")

    income, expense, balance = get_totals()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="glass-card">
                <div class="metric-icon">💵</div>
                <div class="metric-label">Income</div>
                <div class="metric-value income">Rs {income:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="glass-card">
                <div class="metric-icon">💳</div>
                <div class="metric-label">Expense</div>
                <div class="metric-value expense">Rs {expense:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="glass-card" style="margin-top:0.7rem;">
            <div class="metric-icon">🏦</div>
            <div class="metric-label">Net Balance</div>
            <div class="metric-value balance">Rs {balance:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🧾 Expense Split</div>', unsafe_allow_html=True)
    expense_df = get_category_breakdown("expense")
    if not expense_df.empty:
        fig = px.pie(
            expense_df, names="category", values="total", hole=0.6,
            color_discrete_sequence=["#ec4899", "#f59e0b", "#8b5cf6", "#f43f5e", "#fb923c", "#a78bfa"],
        )
        fig.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5e7eb",
            legend=dict(font=dict(size=10), orientation="h", y=-0.15),
            height=250,
        )
        fig.update_traces(textinfo="percent", textfont_size=11, marker=dict(line=dict(color="#0c0b1a", width=2)))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No expenses recorded yet.")

    st.markdown('<div class="section-title">📈 Trend</div>', unsafe_allow_html=True)
    trend_df = get_daily_trend()
    if not trend_df.empty:
        fig2 = go.Figure()
        for t, color in [("income", "#34d399"), ("expense", "#fb7185")]:
            sub = trend_df[trend_df["type"] == t]
            if not sub.empty:
                fig2.add_trace(go.Scatter(
                    x=sub["day"], y=sub["total"], mode="lines+markers",
                    name=t.capitalize(), line=dict(color=color, width=3),
                    fill="tozeroy", fillcolor=color + "22",
                ))
        fig2.update_layout(
            margin=dict(t=10, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5e7eb",
            height=220,
            legend=dict(orientation="h", y=-0.25, font=dict(size=10)),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.caption("No trend data yet.")

    st.markdown('<div class="section-title">📜 Recent Activity</div>', unsafe_allow_html=True)
    history_df = get_all_transactions()
    if not history_df.empty:
        st.dataframe(
            history_df.head(8)[["date", "type", "category", "amount"]],
            hide_index=True,
            use_container_width=True,
            height=230,
        )
    else:
        st.caption("Nothing logged yet — start chatting!")

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

st.markdown("""
    <div class="hero">
        <p class="hero-title">💸 AI Finance Assistant</p>
        <p class="hero-sub">Log expenses, track income, and get instant summaries — chat in English or Roman Urdu.</p>
    </div>
""", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

user_input = st.chat_input('e.g. "I spent 500 on petrol" or "show my summary"')

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            result = st.session_state.agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )
            reply = result["messages"][-1].content
        st.markdown(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()