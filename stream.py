import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ============================
# PAGE CONFIG + LIGHT THEME
# ============================
st.set_page_config(page_title="Food Demand Dashboard", layout="wide")

# Custom background (light color)
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# ============================
# LOAD FILES
# ============================
model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

# ============================
# CATEGORY MAPPING (IMPORTANT)
# ============================
category_map = {
    0: "Main Course",
    1: "Biryani",
    2: "Starter"
}

# Reverse map (for dropdown)
category_reverse = {v: k for k, v in category_map.items()}

# ============================
# TITLE
# ============================
st.title("🍽️ Food Demand Forecasting Dashboard")
st.caption("AI-powered prediction with insights 📊")

# ============================
# SIDEBAR INPUTS
# ============================
st.sidebar.header("⚙️ Enter Inputs")

item = st.sidebar.number_input("Item", min_value=0)

# 👇 Category as NAME
category_name = st.sidebar.selectbox("Category", list(category_map.values()))
category = category_reverse[category_name]

price = st.sidebar.number_input("Price", min_value=0.0)
revenue = st.sidebar.number_input("Revenue", min_value=0.0)

month = st.sidebar.selectbox("Month", list(range(1, 13)))
day_of_week = st.sidebar.selectbox("Day of Week", list(range(7)))
is_holiday = st.sidebar.selectbox("Holiday", [0, 1])

previous_day_sales = st.sidebar.number_input("Previous Day Sales", min_value=0.0)
previous_week_sales = st.sidebar.number_input("Previous Week Sales", min_value=0.0)
same_day_last_month = st.sidebar.number_input("Same Day Last Month", min_value=0.0)
avg_last_7_days = st.sidebar.number_input("Avg Last 7 Days", min_value=0.0)
item_avg_sales = st.sidebar.number_input("Item Avg Sales", min_value=0.0)

weather = st.sidebar.selectbox(
    "Weather", ["Normal", "Sunny", "Cloudy", "Rainy", "Hot", "Cold"]
)

buffer = st.sidebar.slider("Extra Preparation %", 0, 30, 10)

# ============================
# WEATHER EFFECT
# ============================
def apply_weather(pred, weather):
    effects = {
        "Sunny": 1.05,
        "Cloudy": 1.02,
        "Rainy": 0.92,
        "Hot": 0.95,
        "Cold": 1.03,
        "Normal": 1.0
    }
    return pred * effects.get(weather, 1)

# ============================
# PREDICTION
# ============================
if st.sidebar.button("🔮 Predict Demand"):

    input_dict = {
        "Item": item,
        "Category": category,
        "Price": price,
        "Revenue": revenue,
        "month": month,
        "day_of_week": day_of_week,
        "is_holiday": is_holiday,
        "previous_day_sales": previous_day_sales,
        "previous_week_sales": previous_week_sales,
        "same_day_last_month": same_day_last_month,
        "avg_last_7_days": avg_last_7_days,
        "item_avg_sales": item_avg_sales
    }

    input_df = pd.DataFrame([input_dict])[features]

    try:
        pred_log = model.predict(input_df)

        try:
            pred = np.expm1(pred_log)
        except:
            pred = np.exp(pred_log)

        pred = apply_weather(pred[0], weather)

        expected = int(max(0, pred))
        prepared = int(expected * (1 + buffer / 100))
        waste = prepared - expected

        # ============================
        # METRICS
        # ============================
        st.subheader("📊 Key Metrics")

        c1, c2, c3 = st.columns(3)
        c1.metric("Expected Sales", expected)
        c2.metric("Prepare Quantity", prepared)
        c3.metric("Estimated Waste", waste)

        # ============================
        # SMALL TREND CHART
        # ============================
        st.subheader("📈 Sales Trend")

        trend_df = pd.DataFrame({
            "Type": ["Prev Day", "Prev Week", "Last Month", "Avg 7 Days", "Item Avg"],
            "Sales": [
                previous_day_sales,
                previous_week_sales,
                same_day_last_month,
                avg_last_7_days,
                item_avg_sales
            ]
        })

        # 👇 SMALL SIZE CHART
        fig, ax = plt.subplots(figsize=(4,2))
        ax.plot(trend_df["Type"], trend_df["Sales"], marker='o')
        ax.set_title("Trend", fontsize=10)
        ax.tick_params(axis='x', rotation=30)

        st.pyplot(fig)

        # ============================
        # BAR CHART SMALL
        # ============================
        st.subheader("📊 Comparison")

        comp_df = pd.DataFrame({
            "Category": ["Expected", "Prepared", "Waste"],
            "Values": [expected, prepared, waste]
        })

        st.bar_chart(comp_df.set_index("Category"), height=250)

        # ============================
        # DETAILS
        # ============================
        st.subheader("📌 Summary")

        st.write(f"**Item ID:** {item}")
        st.write(f"**Category:** {category_name} ✅")
        st.write(f"**Weather:** {weather}")
        st.write(f"**Holiday:** {'Yes' if is_holiday else 'No'}")

    except Exception as e:
        st.error(f"❌ Error: {e}")