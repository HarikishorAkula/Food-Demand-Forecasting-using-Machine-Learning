import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ============================
# PAGE CONFIG + GREEN UI
# ============================
st.set_page_config(page_title="Food Demand Dashboard", layout="wide")

st.markdown("""
<style>
body {
    background-color: #e8f5e9;
}
[data-testid="stSidebar"] {
    background-color: #c8e6c9;
}
.stMetric {
    background-color: #ffffff;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# LOAD FILES
# ============================
model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

# ============================
# CATEGORY MAPPING
# ============================
category_map = {0:"Main Course",1:"Biryani",2:"Starter"}
category_reverse = {v:k for k,v in category_map.items()}

# ============================
# TITLE
# ============================
st.title("🍽️ Smart Food Demand AI Dashboard")
st.caption("Forecast • Revenue • Profit • Smart Stock 🚀")

# ============================
# SIDEBAR INPUTS
# ============================
st.sidebar.header("⚙️ Inputs")

item = st.sidebar.number_input("Item", min_value=0)
category_name = st.sidebar.selectbox("Category", list(category_map.values()))
category = category_reverse[category_name]

price = st.sidebar.number_input("Price (₹)", min_value=0.0)

# 🔥 COST (NEW for profit)
cost_price = st.sidebar.number_input("Cost Price (₹)", min_value=0.0)

month = st.sidebar.selectbox("Month", list(range(1, 13)))
day_of_week = st.sidebar.selectbox("Day", list(range(7)))
is_holiday = st.sidebar.selectbox("Holiday", [0, 1])

previous_day_sales = st.sidebar.number_input("Prev Day Sales", min_value=0.0)
previous_week_sales = st.sidebar.number_input("Prev Week Sales", min_value=0.0)
same_day_last_month = st.sidebar.number_input("Last Month", min_value=0.0)
avg_last_7_days = st.sidebar.number_input("Avg 7 Days", min_value=0.0)
item_avg_sales = st.sidebar.number_input("Item Avg", min_value=0.0)

weather = st.sidebar.selectbox("Weather", ["Normal","Sunny","Cloudy","Rainy","Hot","Cold"])
buffer = st.sidebar.slider("Buffer %", 0, 30, 10)

# ============================
# WEATHER EFFECT
# ============================
def apply_weather(pred, weather):
    effects = {
        "Sunny":1.05,"Cloudy":1.02,"Rainy":0.92,
        "Hot":0.95,"Cold":1.03,"Normal":1
    }
    return pred * effects.get(weather,1)

# ============================
# PREDICTION
# ============================
if st.sidebar.button("🔮 Predict"):

    input_dict = {
        "Item":item,"Category":category,"Price":price,
        "Revenue":price*previous_day_sales,  # 🔥 auto revenue
        "month":month,"day_of_week":day_of_week,"is_holiday":is_holiday,
        "previous_day_sales":previous_day_sales,
        "previous_week_sales":previous_week_sales,
        "same_day_last_month":same_day_last_month,
        "avg_last_7_days":avg_last_7_days,
        "item_avg_sales":item_avg_sales
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
        prepared = int(expected * (1 + buffer/100))
        waste = prepared - expected

        # ============================
        # 💰 REVENUE + PROFIT
        # ============================
        revenue = expected * price
        cost = prepared * cost_price
        profit = revenue - cost

        # ============================
        # 🧠 STOCK RECOMMENDATION
        # ============================
        if waste > 30:
            suggestion = "⚠️ Reduce preparation (High waste)"
        elif expected > 200:
            suggestion = "🚀 Increase stock (High demand)"
        else:
            suggestion = "✅ Optimal stock level"

        # ============================
        # METRICS
        # ============================
        st.subheader("📊 Dashboard")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Expected Sales", expected)
        c2.metric("Prepare Qty", prepared)
        c3.metric("Waste", waste)
        c4.metric("Profit (₹)", profit)

        # ============================
        # CHART
        # ============================
        st.subheader("📈 Sales Trend")

        trend_df = pd.DataFrame({
            "Type":["Prev Day","Prev Week","Last Month","Avg 7","Item Avg"],
            "Sales":[previous_day_sales,previous_week_sales,
                     same_day_last_month,avg_last_7_days,item_avg_sales]
        })

        fig, ax = plt.subplots(figsize=(4,2))
        ax.plot(trend_df["Type"], trend_df["Sales"], marker='o')
        st.pyplot(fig)

        # ============================
        # BAR CHART
        # ============================
        comp_df = pd.DataFrame({
            "Type":["Expected","Prepared","Waste"],
            "Values":[expected,prepared,waste]
        })

        st.bar_chart(comp_df.set_index("Type"), height=250)

        # ============================
        # INSIGHTS
        # ============================
        st.subheader("🧠 AI Insights")

        st.success(f"💡 Recommendation: {suggestion}")
        st.info(f"💰 Revenue: ₹{revenue}")
        st.info(f"📉 Cost: ₹{cost}")
        st.info(f"📊 Profit: ₹{profit}")

        # ============================
        # SUMMARY
        # ============================
        st.subheader("📌 Summary")
        st.write(f"**Category:** {category_name}")
        st.write(f"**Weather:** {weather}")
        st.write(f"**Holiday:** {'Yes' if is_holiday else 'No'}")

    except Exception as e:
        st.error(f"❌ Error: {e}")