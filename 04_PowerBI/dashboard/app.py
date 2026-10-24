import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="Customer & Sales Intelligence Platform",
    page_icon="📊",
    layout="wide",
)

# -------------------------
# CUSTOM STYLING
# -------------------------

st.markdown(
    """
    <style>
        .stApp {
            background-color: #FAF9F6;
        }

        h1, h2, h3 {
            color: #3F493F;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E6E1D8;
            padding: 16px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# LOAD DATA
# -------------------------

project_root = Path(__file__).resolve().parents[2]

data_path = (
    project_root
    / "01_Data"
    / "cleaned"
    / "sales_powerbi_ready.csv"
)

df = pd.read_csv(data_path)


# -------------------------
# CALCULATE KPIs
# -------------------------

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

total_orders = df["Order ID"].nunique()

total_customers = df["Customer ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales
    else 0
)


# -------------------------
# HOME PAGE
# -------------------------

st.title("📊 Customer & Sales Intelligence Platform")

st.caption(
    "An interactive platform for sales performance, "
    "profitability, product analysis, and customer insights."
)

st.divider()

st.subheader("Welcome")

st.write(
    "Explore your business performance and customer "
    "insights using the analysis pages below."
)

# -------------------------
# KPI CARDS
# -------------------------

st.subheader("Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Sales",
        value=f"${total_sales:,.2f}",
    )

with col2:
    st.metric(
        label="Total Profit",
        value=f"${total_profit:,.2f}",
    )

with col3:
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}",
    )

with col4:
    st.metric(
        label="Total Customers",
        value=f"{total_customers:,}",
    )

with col5:
    st.metric(
        label="Profit Margin",
        value=f"{profit_margin:.2f}%",
    )


# -------------------------
# MONTHLY SALES TREND
# -------------------------

st.divider()

st.subheader("📈 Monthly Sales Trend")

# Convert Order Date into datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Create monthly sales data
monthly_sales = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

# Convert monthly dates into readable format
monthly_sales["Order Date"] = (
    monthly_sales["Order Date"]
    .dt.to_timestamp()
)

# Display sales trend chart
st.line_chart(
    monthly_sales,
    x="Order Date",
    y="Sales",
)


# -------------------------
# MONTHLY PROFIT TREND
# -------------------------

st.divider()

st.subheader("📉 Monthly Profit Trend")

# Create monthly profit data
monthly_profit = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Profit"]
    .sum()
    .reset_index()
)

# Convert monthly dates into readable format
monthly_profit["Order Date"] = (
    monthly_profit["Order Date"]
    .dt.to_timestamp()
)

# Display profit trend chart
st.line_chart(
    monthly_profit,
    x="Order Date",
    y="Profit",
)




# -------------------------
# SALES BY CATEGORY
# -------------------------

st.divider()

st.subheader("📊 Sales by Category")

# Calculate total sales for each category
category_sales = (
    df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

# Create category sales chart
category_sales_chart = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Total Sales by Category",
    color_discrete_sequence=[
        "#78917B",
        "#B87967",
        "#D9B98F",
    ],
)

category_sales_chart.update_layout(
    xaxis_title="Category",
    yaxis_title="Sales ($)",
)

# Display chart
st.plotly_chart(
    category_sales_chart,
    use_container_width=True,
)



# -------------------------
# ANALYSIS NAVIGATION
# -------------------------

st.subheader("Explore Analytics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Sales Analysis")

    st.write(
        "Explore sales trends, category performance, "
        "regional profitability, and product subcategories."
    )

    st.page_link(
        "pages/1_Sales_Analysis.py",
        label="Explore Sales Analysis",
        icon="📈",
        use_container_width=True,
    )

with col2:
    st.markdown("### ↩️ Returns Analysis")

    st.write(
        "Review returned orders, return rates, "
        "and sales associated with returned orders."
    )

    st.page_link(
        "pages/2_Returns_Analysis.py",
        label="Explore Returns Analysis",
        icon="↩️",
        use_container_width=True,
    )

with col3:
    st.markdown("### 👥 Customer Intelligence")

    st.write(
        "Explore customer sales, profitability, "
        "top customers, and customer performance."
    )

    st.page_link(
        "pages/3_Customer_Intelligence.py",
        label="Explore Customer Intelligence",
        icon="👥",
        use_container_width=True,
    )

st.divider()

st.info(
    "Select an analysis above or use the left sidebar "
    "to navigate between dashboard pages."
)

st.caption(
    "Customer & Sales Intelligence Platform | "
    "Python • Streamlit • Pandas • Plotly"
)
