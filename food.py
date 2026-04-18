import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import os

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="🍽️ Food Demand AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CUSTOM CSS — BEAUTIFUL UI
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * {
    color: #e8e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label {
    color: #a0a0c0 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Sidebar header */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 18px !important;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 24px 0;
}
.kpi-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 24px 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 20px 20px 0 0;
}
.kpi-card.blue::before   { background: linear-gradient(90deg,#4facfe,#00f2fe); }
.kpi-card.green::before  { background: linear-gradient(90deg,#43e97b,#38f9d7); }
.kpi-card.orange::before { background: linear-gradient(90deg,#fa8231,#f7b733); }
.kpi-card.purple::before { background: linear-gradient(90deg,#a18cd1,#fbc2eb); }

.kpi-icon {
    font-size: 28px;
    margin-bottom: 8px;
    display: block;
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.5);
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.35);
}

/* Title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 40px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.45);
    margin-top: 6px;
    font-weight: 400;
    letter-spacing: 0.04em;
}
.badge {
    display: inline-block;
    background: linear-gradient(135deg,#43e97b22,#38f9d722);
    border: 1px solid #43e97b55;
    color: #43e97b;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 12px;
    vertical-align: middle;
    letter-spacing: 0.08em;
}

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin: 28px 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Insight cards */
.insight-card {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 12px;
}
.insight-card.success { border-left: 4px solid #43e97b; }
.insight-card.info    { border-left: 4px solid #4facfe; }
.insight-card.warn    { border-left: 4px solid #fa8231; }
.insight-card p {
    margin: 0;
    color: #e0e0f0;
    font-size: 14px;
    line-height: 1.5;
}
.insight-card .tag {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
    color: rgba(255,255,255,0.4);
}

/* Predict button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #43e97b, #38f9d7) !important;
    color: #0f0c29 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: 0.04em;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
}

/* Summary table */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}
.summary-item {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.06);
}
.summary-key {
    font-size: 12px;
    color: rgba(255,255,255,0.45);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.summary-val {
    font-size: 14px;
    color: #ffffff;
    font-weight: 600;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.06); }

/* Charts: transparent bg */
.element-container { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ============================
# MODEL LOADER (with fallback)
# ============================
@st.cache_resource
def load_model():
    try:
        import pickle
        model = pickle.load(open("model.pkl", "rb"))
        features = pickle.load(open("features.pkl", "rb"))
        return model, features, True
    except Exception:
        return None, None, False

model, features, model_loaded = load_model()


# ============================
# WEATHER EFFECT
# ============================
WEATHER_FX = {
    "☀️ Sunny": 1.05,
    "☁️ Cloudy": 1.02,
    "🌧️ Rainy": 0.92,
    "🔥 Hot": 0.95,
    "❄️ Cold": 1.03,
    "🌤️ Normal": 1.00
}

CATEGORY_MAP = {0: "Main Course", 1: "Biryani", 2: "Starter"}
CATEGORY_REV = {v: k for k, v in CATEGORY_MAP.items()}


# ============================
# AI FORECAST (fallback = smart heuristic)
# ============================
def forecast_demand(item, category, price, prev_day, prev_week,
                    last_month, avg7, item_avg, month, dow,
                    is_holiday, weather, buffer_pct, model, features):
    
    weather_mult = WEATHER_FX.get(weather, 1.0)
    
    if model_loaded and model is not None:
        input_dict = {
            "Item": item, "Category": CATEGORY_REV[category],
            "Price": price, "Revenue": price * prev_day,
            "month": month, "day_of_week": dow, "is_holiday": is_holiday,
            "previous_day_sales": prev_day, "previous_week_sales": prev_week,
            "same_day_last_month": last_month, "avg_last_7_days": avg7,
            "item_avg_sales": item_avg
        }
        input_df = pd.DataFrame([input_dict])[features]
        pred_log = model.predict(input_df)
        try:
            base = np.expm1(pred_log[0])
        except Exception:
            base = np.exp(pred_log[0])
        pred = base * weather_mult
    else:
        # Smart heuristic forecast when no model
        weights = [0.35, 0.20, 0.25, 0.15, 0.05]
        vals = [prev_day, prev_week / 7, last_month, avg7, item_avg]
        base = sum(w * v for w, v in zip(weights, vals)) if any(v > 0 for v in vals) else 80.0
        
        holiday_bump = 1.18 if is_holiday else 1.0
        dow_factor = [0.85, 1.0, 1.0, 1.05, 1.15, 1.25, 1.10][dow % 7]
        season_factor = [1.0, 1.0, 1.05, 1.05, 0.95, 0.90, 0.90, 0.90, 0.95, 1.05, 1.10, 1.15][month - 1]
        price_penalty = max(0.7, 1 - (price / 1000) * 0.3) if price > 0 else 1.0
        
        pred = max(5, base * weather_mult * holiday_bump * dow_factor * season_factor * price_penalty)
    
    expected = int(round(pred))
    prepared = int(expected * (1 + buffer_pct / 100))
    waste = prepared - expected
    return expected, prepared, waste


# ============================
# HEADER
# ============================
st.markdown("""
<div style="padding: 24px 0 8px;">
    <p class="hero-title">🍽️ Food Demand AI <span class="badge">LIVE</span></p>
    <p class="hero-sub">Smart Forecasting • Revenue Analytics • Stock Optimization</p>
</div>
<hr/>
""", unsafe_allow_html=True)


# ============================
# SIDEBAR
# ============================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    item = st.number_input("Item ID", min_value=0, value=1)
    category_name = st.selectbox("Category", list(CATEGORY_MAP.values()))
    
    st.markdown("**Pricing**")
    col_a, col_b = st.columns(2)
    with col_a:
        price = st.number_input("Sell ₹", min_value=0.0, value=150.0)
    with col_b:
        cost_price = st.number_input("Cost ₹", min_value=0.0, value=60.0)

    st.markdown("**Time**")
    col_c, col_d = st.columns(2)
    with col_c:
        month = st.selectbox("Month", list(range(1, 13)), index=3)
    with col_d:
        day_of_week = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    dow_idx = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].index(day_of_week)
    
    is_holiday = st.toggle("🎉 Holiday / Special Event", value=False)
    weather = st.selectbox("🌦️ Weather", list(WEATHER_FX.keys()), index=5)
    
    st.markdown("**Historical Sales**")
    prev_day   = st.number_input("Yesterday's Sales", min_value=0.0, value=95.0)
    prev_week  = st.number_input("Last Week Sales", min_value=0.0, value=620.0)
    last_month = st.number_input("Same Day Last Month", min_value=0.0, value=88.0)
    avg7       = st.number_input("7-Day Average", min_value=0.0, value=91.0)
    item_avg   = st.number_input("Item All-Time Avg", min_value=0.0, value=85.0)

    buffer = st.slider("📦 Safety Buffer %", 0, 30, 10)
    
    st.markdown("---")
    predict_btn = st.button("🔮 Generate Forecast")

    if not model_loaded:
        st.markdown("""
        <div style="background:rgba(250,130,49,0.12);border:1px solid rgba(250,130,49,0.3);
        border-radius:10px;padding:10px 12px;margin-top:8px;">
        <span style="color:#fa8231;font-size:11px;font-weight:600;">⚠️ MODEL NOT FOUND</span><br/>
        <span style="color:rgba(255,255,255,0.5);font-size:11px;">
        Running smart heuristic forecast. Upload model.pkl to Streamlit Cloud for ML predictions.
        </span></div>
        """, unsafe_allow_html=True)


# ============================
# MAIN CONTENT
# ============================
if predict_btn:
    with st.spinner("🤖 Analyzing demand patterns..."):
        time.sleep(0.6)  # brief load for UX feel
    
    expected, prepared, waste = forecast_demand(
        item, category_name, price, prev_day, prev_week,
        last_month, avg7, item_avg, month, dow_idx,
        int(is_holiday), weather, buffer, model, features
    )
    
    revenue = expected * price
    cost    = prepared * cost_price
    profit  = revenue - cost
    margin  = ((profit / revenue) * 100) if revenue > 0 else 0
    
    # ── Recommendation ──
    if waste > 40:
        rec_icon, rec_txt, rec_class = "⚠️", "Reduce prep quantity — high projected waste", "warn"
    elif expected > 200:
        rec_icon, rec_txt, rec_class = "🚀", "Increase stock — very high demand expected", "success"
    elif profit < 0:
        rec_icon, rec_txt, rec_class = "🔴", "Review pricing — projected loss on this item", "warn"
    else:
        rec_icon, rec_txt, rec_class = "✅", "Optimal stock level — all metrics healthy", "success"

    # ── KPI Cards ──
    st.markdown('<div class="section-title">📊 Live Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <span class="kpi-icon">📦</span>
            <div class="kpi-label">Expected Sales</div>
            <div class="kpi-value">{expected}</div>
            <div class="kpi-sub">units today</div>
        </div>
        <div class="kpi-card green">
            <span class="kpi-icon">🛒</span>
            <div class="kpi-label">Prepare Qty</div>
            <div class="kpi-value">{prepared}</div>
            <div class="kpi-sub">+{buffer}% buffer</div>
        </div>
        <div class="kpi-card orange">
            <span class="kpi-icon">🗑️</span>
            <div class="kpi-label">Est. Waste</div>
            <div class="kpi-value">{waste}</div>
            <div class="kpi-sub">units</div>
        </div>
        <div class="kpi-card purple">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">Net Profit</div>
            <div class="kpi-value">₹{int(profit):,}</div>
            <div class="kpi-sub">{margin:.1f}% margin</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts Row ──
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-title">📈 Sales Trend</div>', unsafe_allow_html=True)
        labels = ["Prev\nDay", "Prev\nWeek÷7", "Last\nMonth", "7-Day\nAvg", "Item\nAvg", "Forecast"]
        values = [prev_day, prev_week / 7, last_month, avg7, item_avg, expected]
        colors = ['#4facfe'] * 5 + ['#43e97b']

        fig, ax = plt.subplots(figsize=(7, 3.2))
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3,
                      edgecolor='none', linewidth=0)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                    f'{val:.0f}', ha='center', va='bottom', fontsize=9,
                    color='white', fontweight='600')
        ax.set_ylim(0, max(values) * 1.20)
        ax.tick_params(colors='#aaaacc', labelsize=9)
        ax.spines[['top', 'right', 'left']].set_visible(False)
        ax.spines['bottom'].set_color((1, 1, 1, 0.1))
        ax.yaxis.set_visible(False)
        ax.grid(axis='y', color=(1, 1, 1, 0.07), linewidth=0.8, zorder=0)
        for label in ax.get_xticklabels():
            label.set_color('#aaaacc')
        fig.tight_layout(pad=0.5)
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="section-title">💹 P&L Breakdown</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(3.5, 3.2))
        fig2.patch.set_alpha(0)
        ax2.set_facecolor('none')
        pl_labels = ["Revenue", "Cost", "Profit"]
        pl_values = [revenue, cost, max(0, profit)]
        pl_colors = ['#43e97b', '#fa8231', '#4facfe' if profit >= 0 else '#ff4444']
        wedges, texts, autotexts = ax2.pie(
            pl_values, labels=pl_labels, colors=pl_colors,
            autopct='%1.0f%%', startangle=140,
            wedgeprops=dict(width=0.55, edgecolor='none'),
            textprops=dict(color='#ccccee', fontsize=10)
        )
        for at in autotexts:
            at.set_color('white')
            at.set_fontsize(9)
            at.set_fontweight('bold')
        fig2.tight_layout(pad=0.2)
        st.pyplot(fig2)

    # ── Insights Row ──
    st.markdown('<div class="section-title">🧠 AI Insights</div>', unsafe_allow_html=True)
    
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""
        <div class="insight-card {rec_class}">
            <div class="tag">Recommendation</div>
            <p>{rec_icon} {rec_txt}</p>
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""
        <div class="insight-card info">
            <div class="tag">Revenue Analysis</div>
            <p>💰 Revenue: ₹{int(revenue):,} &nbsp;|&nbsp; Cost: ₹{int(cost):,}<br/>
            📊 Margin: <strong>{margin:.1f}%</strong></p>
        </div>""", unsafe_allow_html=True)
    with ic3:
        weather_effect = (WEATHER_FX.get(weather, 1.0) - 1) * 100
        holiday_note = "Holiday boost (+18%)" if is_holiday else "Regular day"
        st.markdown(f"""
        <div class="insight-card info">
            <div class="tag">Demand Factors</div>
            <p>{weather} Weather: {weather_effect:+.0f}%<br/>
            📅 {holiday_note}<br/>
            📆 {day_of_week} demand index active</p>
        </div>""", unsafe_allow_html=True)

    # ── Summary ──
    st.markdown('<div class="section-title">📌 Order Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-item">
            <span class="summary-key">Category</span>
            <span class="summary-val">{category_name}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Item ID</span>
            <span class="summary-val">#{item}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Sell Price</span>
            <span class="summary-val">₹{price:.2f}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Cost Price</span>
            <span class="summary-val">₹{cost_price:.2f}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Weather</span>
            <span class="summary-val">{weather}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Holiday</span>
            <span class="summary-val">{'🎉 Yes' if is_holiday else 'No'}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Month / Day</span>
            <span class="summary-val">Month {month} · {day_of_week}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Forecast Mode</span>
            <span class="summary-val">{'🤖 ML Model' if model_loaded else '📐 Smart Heuristic'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <div style="font-size:72px;margin-bottom:20px;">🍽️</div>
        <p style="font-family:'Syne',sans-serif;font-size:24px;font-weight:700;color:#fff;margin:0;">
            Ready to Forecast
        </p>
        <p style="color:rgba(255,255,255,0.4);font-size:15px;margin-top:10px;">
            Configure your inputs in the sidebar and click <strong style="color:#43e97b;">Generate Forecast</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)