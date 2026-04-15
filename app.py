import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(page_title="Food Demand Dashboard", layout="wide")
st.markdown("""


<style>

/* 🌿 Main background */
.stApp {
    background: linear-gradient(to right, #e8f5e9, #f1f8e9);
}

/* 🌿 Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #c8e6c9, #a5d6a7);
}

/* 🏷️ Labels */
label {
    color: #1b5e20 !important;
    font-weight: 600;
}

/* ✅ INPUT BOXES (SAFE) */
input, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #a5d6a7 !important;
    border-radius: 10px;
    padding: 8px;
}

/* 🔴 SELECTBOX MAIN */
div[data-baseweb="select"] {
    background-color: #ff5252 !important;
    border-radius: 10px !important;
    border: 2px solid #d32f2f !important;
}

/* 🔥 SELECTED TEXT (IMPORTANT FIX) */
div[data-baseweb="select"] span {
    color: #ffffff !important;
    font-weight: bold;
}

/* 🔽 DROPDOWN MENU */
ul[role="listbox"] {
    background-color: #ffffff !important;
}

/* 🔽 DROPDOWN ITEMS */
li {
    color: #000000 !important;
    font-weight: 500;
}

/* 🔥 HOVER ITEM */
li:hover {
    background-color: #ffcdd2 !important;
    color: #000000 !important;
}

/* 📊 Metric cards */
[data-testid="metric-container"] {
    background-color: #ffffff !important;
    border-radius: 12px;
    padding: 15px;
}

/* Metric text */
[data-testid="metric-container"] div {
    color: #000000 !important;
}

/* 🧾 General text */
p, span, div {
    color: #000000 !important;
}

</style>


""", unsafe_allow_html=True)



# ============================
# LOAD FILES
# ============================
model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

# ============================
# CATEGORY
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
cost_price = st.sidebar.number_input("Cost Price (₹)", min_value=0.0)
# ============================
# MONTH SELECTBOX
# ============================
months = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

month_name = st.sidebar.selectbox("Month", list(months.keys()))
month = months[month_name]

day_of_week = st.sidebar.selectbox("Day", list(range(7)))

# 👇 Holiday text clearly visible now
is_holiday = st.sidebar.selectbox("Holiday", ["No", "Yes"])
is_holiday_val = 1 if is_holiday == "Yes" else 0

previous_day_sales = st.sidebar.number_input("Prev Day Sales", min_value=0.0)
previous_week_sales = st.sidebar.number_input("Prev Week Sales", min_value=0.0)
same_day_last_month = st.sidebar.number_input("Last Month", min_value=0.0)
avg_last_7_days = st.sidebar.number_input("Avg 7 Days", min_value=0.0)
item_avg_sales = st.sidebar.number_input("Item Avg", min_value=0.0)

weather = st.sidebar.selectbox("Weather", ["Normal","Sunny","Cloudy","Rainy","Hot","Cold"])
buffer = st.sidebar.slider("Buffer %", 0, 30, 10)

# ============================
# WEATHER
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
        "Item":item,
        "Category":category,
        "Price":price,
        "Revenue":price*previous_day_sales,
        "month":month,
        "day_of_week":day_of_week,
        "is_holiday":is_holiday_val,
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

        # 💰 BUSINESS
        revenue = expected * price
        cost = prepared * cost_price
        profit = revenue - cost

        # 🧠 SUGGESTION
        if waste > 30:
            suggestion = "⚠️ Reduce preparation"
        elif expected > 200:
            suggestion = "🚀 Increase stock"
        else:
            suggestion = "✅ Optimal stock"

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

        st.success(f"{suggestion}")
        st.info(f"💰 Revenue: ₹{revenue}")
        st.info(f"📉 Cost: ₹{cost}")
        st.info(f"📊 Profit: ₹{profit}")

        # ============================
        # SUMMARY
        # ============================
        st.subheader("📌 Summary")
        st.write(f"Category: {category_name}")
        st.write(f"Weather: {weather}")
        st.write(f"Holiday: {is_holiday}")

    except Exception as e:
        st.error(f"❌ Error: {e}")