import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="🍽️ Hari’s Mehfil AI Kitchen",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CUSTOM CSS
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }
[data-testid="stSidebar"] label {
    color: #a0a0c0 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

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

.kpi-icon  { font-size: 28px; margin-bottom: 8px; display: block; }
.kpi-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: rgba(255,255,255,0.5); margin-bottom: 6px; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #ffffff; line-height: 1; margin-bottom: 4px; }
.kpi-sub   { font-size: 12px; color: rgba(255,255,255,0.35); }

.hero-title { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; color: #ffffff; margin: 0; line-height: 1.1; }
.hero-sub   { font-size: 14px; color: rgba(255,255,255,0.45); margin-top: 6px; font-weight: 400; letter-spacing: 0.04em; }
.badge      { display: inline-block; background: linear-gradient(135deg,#43e97b22,#38f9d722); border: 1px solid #43e97b55; color: #43e97b; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; margin-left: 12px; vertical-align: middle; letter-spacing: 0.08em; }

.section-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: #ffffff; margin: 28px 0 16px; }

.insight-card { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 12px; }
.insight-card.success { border-left: 4px solid #43e97b; }
.insight-card.info    { border-left: 4px solid #4facfe; }
.insight-card.warn    { border-left: 4px solid #fa8231; }
.insight-card p   { margin: 0; color: #e0e0f0; font-size: 14px; line-height: 1.5; }
.insight-card .tag { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; color: rgba(255,255,255,0.4); }

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
    letter-spacing: 0.04em;
}

.summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
.summary-item { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.06); }
.summary-key  { font-size: 12px; color: rgba(255,255,255,0.45); font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }
.summary-val  { font-size: 14px; color: #ffffff; font-weight: 600; }

hr { border-color: rgba(255,255,255,0.06); }
</style>
""", unsafe_allow_html=True)


# ============================
# ITEM NAME MAP
# Derived from dataset: Item 0-29, Categories: Main Course / Biryani / Starter
# ============================
ITEM_NAMES = {
    # Main Course
    0:  ("Paneer Butter Masala",     "Main Course"),  # was Butter Chicken
    4:  ("Paneer Tikka Masala",      "Main Course"),  # already veg ✅
    8:  ("Dal Makhani",              "Main Course"),  # already veg ✅
    9:  ("Shahi Paneer",             "Main Course"),  # was Mutton Rogan Josh
    11: ("Kadai Paneer",             "Main Course"),  # was Chicken Kadai
    12: ("Palak Paneer",             "Main Course"),  # already veg ✅
    13: ("Veg Kolhapuri",            "Main Course"),  # was Fish Curry
    15: ("Chole Bhature",            "Main Course"),  # already veg ✅
    19: ("Paneer Do Pyaza",          "Main Course"),  # was Egg Masala Curry
    23: ("Malai Kofta",              "Main Course"),  # was Prawn Masala
    27: ("Veg Handi",                "Main Course"),  # was Lamb Keema
    28: ("Veg Kofta Curry",          "Main Course"),  # already veg ✅
    29: ("Methi Matar Malai",        "Main Course"),  # was Chicken Handi

    # Biryani
    1:  ("Veg Dum Biryani",          "Biryani"),      # was Hyderabadi Chicken Biryani
    2:  ("Mushroom Biryani",         "Biryani"),      # was Mutton Biryani
    5:  ("Veg Biryani",              "Biryani"),      # already veg ✅
    6:  ("Paneer Biryani",           "Biryani"),      # was Prawn Biryani
    7:  ("Soya Biryani",             "Biryani"),      # was Egg Biryani
    10: ("Kathal Biryani",           "Biryani"),      # was Chicken Dum Biryani
    17: ("Corn & Peas Biryani",      "Biryani"),      # was Malabar Fish Biryani
    21: ("Lucknowi Veg Biryani",     "Biryani"),      # was Lucknowi Dum Biryani
    24: ("Spl Mehfil Veg Biryani",   "Biryani"),      # was Spl Mehfil Biryani
    25: ("Rajma Biryani",            "Biryani"),      # was Kacchi Gosht Biryani
    26: ("Paneer Dum Biryani",       "Biryani"),      # already veg ✅

    # Starter
    3:  ("Paneer 65",                "Starter"),      # was Chicken 65
    14: ("Hara Bhara Kebab",         "Starter"),      # was Seekh Kebab
    16: ("Paneer Tikka",             "Starter"),      # already veg ✅
    18: ("Veg Shammi Kebab",         "Starter"),      # was Mutton Shammi Kebab
    20: ("Crispy Corn",              "Starter"),      # was Fish Fry
    22: ("Veg Spring Roll",          "Starter"),      # already veg ✅
}

CATEGORY_EMOJI = {"Main Course": "🍛", "Biryani": "🍚", "Starter": "🥙"}

WEATHER_FX = {
    "☀️ Sunny":  1.05,
    "☁️ Cloudy": 1.02,
    "🌧️ Rainy":  0.92,
    "🔥 Hot":    0.95,
    "❄️ Cold":   1.03,
    "🌤️ Normal": 1.00,
}

def item_label(iid):
    name, cat = ITEM_NAMES[iid]
    return f"{CATEGORY_EMOJI[cat]} {name}  [{cat}]"

ITEM_OPTIONS = {item_label(i): i for i in sorted(ITEM_NAMES.keys())}


# ============================
# MODEL LOADER
# ============================
@st.cache_resource
def load_model():
    try:
        import pickle
        model    = pickle.load(open("model.pkl", "rb"))
        features = pickle.load(open("features.pkl", "rb"))
        return model, features, True
    except Exception:
        return None, None, False

model, features, model_loaded = load_model()


# ============================
# FORECAST ENGINE
# ============================
def forecast_demand(item_id, category, price, prev_day, prev_week,
                    last_month, avg7, item_avg, month, dow,
                    is_holiday, weather, buffer_pct):

    weather_mult = WEATHER_FX.get(weather, 1.0)
    cat_map = {"Main Course": 1, "Biryani": 0, "Starter": 2}

    if model_loaded and model is not None:
        input_dict = {
            "Item": item_id,
            "Category": cat_map.get(category, 1),
            "Price": price,
            "Revenue": price * prev_day,
            "month": month, "day_of_week": dow, "is_holiday": is_holiday,
            "previous_day_sales": prev_day,
            "previous_week_sales": prev_week,
            "same_day_last_month": last_month,
            "avg_last_7_days": avg7,
            "item_avg_sales": item_avg,
        }
        input_df = pd.DataFrame([input_dict])[features]
        pred_log = model.predict(input_df)
        try:
            base = np.expm1(pred_log[0])
        except Exception:
            base = np.exp(pred_log[0])
        pred = base * weather_mult
    else:
        vals    = [prev_day, prev_week / 7, last_month, avg7, item_avg]
        weights = [0.35, 0.20, 0.25, 0.15, 0.05]
        base    = sum(w * v for w, v in zip(weights, vals)) if any(v > 0 for v in vals) else 85.0
        holiday_bump  = 1.18 if is_holiday else 1.0
        dow_factor    = [0.85, 1.0, 1.0, 1.05, 1.15, 1.25, 1.10][dow % 7]
        season_factor = [1.0, 1.0, 1.05, 1.05, 0.95, 0.90, 0.90, 0.90, 0.95, 1.05, 1.10, 1.15][month - 1]
        price_penalty = max(0.7, 1 - (price / 1000) * 0.3) if price > 0 else 1.0
        pred = max(5, base * weather_mult * holiday_bump * dow_factor * season_factor * price_penalty)

    expected = int(round(pred))
    prepared = int(expected * (1 + buffer_pct / 100))
    waste    = prepared - expected
    return expected, prepared, waste


# ============================
# HEADER
# ============================
st.markdown("""
<div style="padding:24px 0 8px;">
    <p class="hero-title">🍽️ Hari's Mehfil AI Kitchen<span class="badge">LIVE</span></p>
    <p class="hero-sub">Smart Forecasting • Revenue Analytics • Stock Optimization • Hyderabad</p>
</div>
<hr/>
""", unsafe_allow_html=True)


# ============================
# SIDEBAR
# ============================
with st.sidebar:
    st.markdown("### ⚙️ AI RESTAURANT")
    st.markdown("---")

    selected_label = st.selectbox("🍽️ Select Dish", list(ITEM_OPTIONS.keys()))
    item_id        = ITEM_OPTIONS[selected_label]
    item_name, category = ITEM_NAMES[item_id]

    st.markdown(f"""
    <div style="background:rgba(67,233,123,0.08);border:1px solid rgba(67,233,123,0.2);
    border-radius:10px;padding:10px 14px;margin-bottom:12px;">
        <div style="font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.1em;">Selected Item</div>
        <div style="font-size:15px;font-weight:700;color:#fff;margin-top:2px;">{item_name}</div>
        <div style="font-size:11px;color:#43e97b;margin-top:2px;">{category} &nbsp;·&nbsp; Item #{item_id}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**💰 Pricing**")
    col_a, col_b = st.columns(2)
    with col_a:
        price = st.number_input("Sell ₹", min_value=0.0, value=260.0)
    with col_b:
        cost_price = st.number_input("Cost ₹", min_value=0.0, value=100.0)

    st.markdown("**📅 Time**")
    col_c, col_d = st.columns(2)
    with col_c:
        month = st.selectbox("Month", list(range(1, 13)), index=3)
    with col_d:
        day_name = st.selectbox("Day", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    dow_idx = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(day_name)

    is_holiday = st.toggle("🎉 Holiday / Special Event", value=False)
    weather    = st.selectbox("🌦️ Weather", list(WEATHER_FX.keys()), index=5)

    st.markdown("**📊 Historical Sales**")
    prev_day   = st.number_input("Yesterday's Sales",     min_value=0.0, value=95.0)
    prev_week  = st.number_input("Last Week Total Sales", min_value=0.0, value=620.0)
    last_month = st.number_input("Same Day Last Month",   min_value=0.0, value=88.0)
    avg7       = st.number_input("7-Day Average",         min_value=0.0, value=91.0)
    item_avg   = st.number_input("Item All-Time Avg",     min_value=0.0, value=85.0)

    buffer = st.slider("📦 Safety Buffer %", 0, 30, 10)
    st.markdown("---")
    predict_btn = st.button("🔮 Generate Forecast")

    if not model_loaded:
        st.markdown("""
        <div style="background:rgba(250,130,49,0.12);border:1px solid rgba(250,130,49,0.3);
        border-radius:10px;padding:10px 12px;margin-top:8px;">
        <span style="color:#fa8231;font-size:11px;font-weight:600;">⚠️ MODEL NOT FOUND</span><br/>
        <span style="color:rgba(255,255,255,0.5);font-size:11px;">
        Running smart heuristic. Upload model.pkl to use ML predictions.
        </span></div>
        """, unsafe_allow_html=True)


# ============================
# MAIN PANEL
# ============================
if predict_btn:
    with st.spinner(f"🤖 Forecasting demand for {item_name}..."):
        time.sleep(0.5)

    expected, prepared, waste = forecast_demand(
        item_id, category, price, prev_day, prev_week,
        last_month, avg7, item_avg, month, dow_idx,
        int(is_holiday), weather, buffer
    )

    revenue = expected * price
    cost    = prepared * cost_price
    profit  = revenue - cost
    margin  = (profit / revenue * 100) if revenue > 0 else 0

    if waste > 40:
        rec_icon, rec_txt, rec_class = "⚠️", "Reduce prep — high projected waste", "warn"
    elif expected > 200:
        rec_icon, rec_txt, rec_class = "🚀", "Increase stock — very high demand expected", "success"
    elif profit < 0:
        rec_icon, rec_txt, rec_class = "🔴", "Review pricing — projected loss on this item", "warn"
    else:
        rec_icon, rec_txt, rec_class = "✅", "Optimal stock level — all metrics healthy", "success"

    cat_emoji = CATEGORY_EMOJI.get(category, "🍽️")

    # Dish banner
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:16px;padding:16px 24px;margin-bottom:8px;display:flex;align-items:center;gap:16px;">
        <span style="font-size:40px;">{cat_emoji}</span>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#fff;">{item_name}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:3px;">
                Item #{item_id} &nbsp;·&nbsp; {category} &nbsp;·&nbsp; ₹{price:.0f} sell &nbsp;·&nbsp; {day_name}, Month {month}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
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

    # Charts
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-title">📈 Sales Trend</div>', unsafe_allow_html=True)
        labels = ["Prev\nDay", "Week\n÷7", "Last\nMonth", "7-Day\nAvg", "Item\nAvg", "Forecast"]
        values = [prev_day, prev_week / 7, last_month, avg7, item_avg, float(expected)]
        bar_colors = ['#4facfe'] * 5 + ['#43e97b']

        fig, ax = plt.subplots(figsize=(7, 3.2))
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        bars = ax.bar(labels, values, color=bar_colors, width=0.55, zorder=3, edgecolor='none')
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.02,
                    f'{val:.0f}', ha='center', va='bottom',
                    fontsize=9, color='white', fontweight='600')
        ax.set_ylim(0, max(values) * 1.22)
        ax.tick_params(colors='#aaaacc', labelsize=9)
        for lbl in ax.get_xticklabels():
            lbl.set_color('#aaaacc')
        ax.spines[['top', 'right', 'left']].set_visible(False)
        ax.spines['bottom'].set_color((1, 1, 1, 0.1))
        ax.yaxis.set_visible(False)
        ax.grid(axis='y', color=(1, 1, 1, 0.07), linewidth=0.8, zorder=0)
        fig.tight_layout(pad=0.5)
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="section-title">💹 P&L Breakdown</div>', unsafe_allow_html=True)
        pl_vals   = [revenue, cost, max(0.1, profit)]
        pl_labels = ["Revenue", "Cost", "Profit"]
        pl_colors = ['#43e97b', '#fa8231', '#4facfe' if profit >= 0 else '#ff4444']

        fig2, ax2 = plt.subplots(figsize=(3.5, 3.2))
        fig2.patch.set_alpha(0)
        ax2.set_facecolor('none')
        wedges, texts, autotexts = ax2.pie(
            pl_vals, labels=pl_labels, colors=pl_colors,
            autopct='%1.0f%%', startangle=140,
            wedgeprops=dict(width=0.55, edgecolor='none'),
            textprops=dict(color='#ccccee', fontsize=10)
        )
        for at in autotexts:
            at.set_color('white'); at.set_fontsize(9); at.set_fontweight('bold')
        fig2.tight_layout(pad=0.2)
        st.pyplot(fig2)

    # Insights
    st.markdown('<div class="section-title">🧠 AI Insights</div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    weather_effect = (WEATHER_FX.get(weather, 1.0) - 1) * 100
    holiday_note   = "Holiday boost (+18%)" if is_holiday else "Regular day"

    with ic1:
        st.markdown(f"""<div class="insight-card {rec_class}">
            <div class="tag">Recommendation</div>
            <p>{rec_icon} {rec_txt}</p></div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""<div class="insight-card info">
            <div class="tag">Revenue Analysis</div>
            <p>💰 Revenue: ₹{int(revenue):,}&nbsp;|&nbsp;Cost: ₹{int(cost):,}<br/>
            📊 Margin: <strong>{margin:.1f}%</strong></p></div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""<div class="insight-card info">
            <div class="tag">Demand Factors</div>
            <p>{weather}: {weather_effect:+.0f}% effect<br/>
            📅 {holiday_note}<br/>
            📆 {day_name} demand index active</p></div>""", unsafe_allow_html=True)

    # Summary
    st.markdown('<div class="section-title">📌 Order Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-item">
            <span class="summary-key">Dish</span>
            <span class="summary-val">{cat_emoji} {item_name}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Category</span>
            <span class="summary-val">{category}</span>
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
            <span class="summary-val">Month {month} · {day_name}</span>
        </div>
        <div class="summary-item">
            <span class="summary-key">Forecast Mode</span>
            <span class="summary-val">{'🤖 ML Model' if model_loaded else '📐 Smart Heuristic'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <div style="font-size:72px;margin-bottom:20px;">🍽️</div>
        <p style="font-family:'Syne',sans-serif;font-size:24px;font-weight:700;color:#fff;margin:0;">
            Ready to Forecast
        </p>
        <p style="color:rgba(255,255,255,0.4);font-size:15px;margin-top:10px;">
            Select a dish from the sidebar and click
            <strong style="color:#43e97b;">Generate Forecast</strong>
        </p>
        <div style="margin-top:32px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
            <span style="background:rgba(79,172,254,0.1);border:1px solid rgba(79,172,254,0.3);color:#4facfe;
            border-radius:20px;padding:6px 16px;font-size:12px;font-weight:600;">🍛 13 Main Courses</span>
            <span style="background:rgba(250,130,49,0.1);border:1px solid rgba(250,130,49,0.3);color:#fa8231;
            border-radius:20px;padding:6px 16px;font-size:12px;font-weight:600;">🍚 11 Biryanis</span>
            <span style="background:rgba(163,140,209,0.1);border:1px solid rgba(163,140,209,0.3);color:#a18cd1;
            border-radius:20px;padding:6px 16px;font-size:12px;font-weight:600;">🥙 6 Starters</span>
        </div>
    </div>
    """, unsafe_allow_html=True)