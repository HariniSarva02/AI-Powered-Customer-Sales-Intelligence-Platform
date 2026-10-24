import streamlit as st
import plotly.express as px

from dashboard_utils import load_sales_data


st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📈",
    layout="wide",
)

# Minimal & Elegant styling
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

st.title("Sales Analysis")
st.caption(
    "Explore sales trends, categories, regions, and product performance."
)

# Load sales data
try:
    df = load_sales_data()
except Exception as error:
    st.error(f"Unable to load sales data: {error}")
    st.stop()

# Sidebar filters
st.sidebar.title("Sales Filters")

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()


def reset_sales_filters():
    st.session_state["sales_region_filter"] = regions
    st.session_state["sales_category_filter"] = categories
    st.session_state["sales_start_date_filter"] = min_date
    st.session_state["sales_end_date_filter"] = max_date



selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    key="sales_region_filter",
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
    key="sales_category_filter",
)



start_date = st.sidebar.date_input(
    "From Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="sales_start_date_filter",
    format="YYYY-MM-DD",
)

end_date = st.sidebar.date_input(
    "To Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="sales_end_date_filter",
    format="YYYY-MM-DD",
)


st.sidebar.divider()

st.sidebar.button(
    "Reset Filters",
    use_container_width=True,
    on_click=reset_sales_filters,
)


filtered = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
].copy()

if start_date > end_date:
    st.warning("From Date cannot be later than To Date.")
    st.stop()

filtered = filtered[
    filtered["Order Date"].dt.date.between(start_date, end_date)
]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# KPI cards
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique()
total_customers = filtered["Customer ID"].nunique()
profit_margin = total_profit / total_sales * 100 if total_sales else 0

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Customers", f"{total_customers:,}")
col5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.caption(f"Showing {len(filtered):,} of {len(df):,} sales records")
st.divider()

# Monthly sales trend
st.subheader("Sales Performance Over Time")

monthly_sales = (
    filtered.assign(Month=filtered["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

monthly_chart = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
)
monthly_chart.update_traces(line_color="#78917B")
st.plotly_chart(monthly_chart, use_container_width=True)




# Monthly profit trend
st.subheader("Monthly Profit Trend")

monthly_profit = (
    filtered.assign(
        Month=filtered["Order Date"].dt.to_period("M").astype(str)
    )
    .groupby("Month", as_index=False)["Profit"]
    .sum()
)

profit_chart = px.line(
    monthly_profit,
    x="Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend",
)

profit_chart.update_traces(
    line_color="#78917B"
)

profit_chart.add_hline(
    y=0,
    line_dash="dash",
    line_color="gray",
)

st.plotly_chart(
    profit_chart,
    use_container_width=True,
)




# Sales by category and profit by region
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    category_sales = (
        filtered.groupby("Category", as_index=False)["Sales"].sum()
    )
    category_chart = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category",
    )
    st.plotly_chart(category_chart, use_container_width=True)

with col2:
    st.subheader("Profit by Region")
    region_profit = (
        filtered.groupby("Region", as_index=False)["Profit"].sum()
    )
    region_chart = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region",
    )
    region_chart.update_traces(marker_color="#78917B")
    st.plotly_chart(region_chart, use_container_width=True)




# Profit by category
st.subheader("Profit by Category")

category_profit = (
    filtered.groupby("Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

category_profit_chart = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Profit",
    title="Profit by Product Category",
    color_continuous_scale=[
        "#B87967",
        "#E6E1D8",
        "#78917B",
    ],
)

category_profit_chart.add_hline(
    y=0,
    line_dash="dash",
    line_color="gray",
)

st.plotly_chart(
    category_profit_chart,
    use_container_width=True,
)


# Product subcategory performance
st.subheader("Product Subcategory Performance")

subcategory = (
    filtered.groupby("Sub-Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

subcategory_chart = px.bar(
    subcategory,
    x="Sub-Category",
    y="Profit",
    color="Profit",
    title="Profit by Product Subcategory",
    color_continuous_scale=["#B87967", "#E6E1D8", "#78917B"],
)
st.plotly_chart(subcategory_chart, use_container_width=True)



# -------------------------
# TOP 10 PRODUCTS BY SALES
# -------------------------

st.divider()

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
    .sort_values("Sales", ascending=True)
)

top_products_chart = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    color="Sales",
    color_continuous_scale=[
        "#E6E1D8",
        "#78917B",
    ],
)

top_products_chart.update_layout(
    yaxis_title="Product",
    xaxis_title="Sales",
)

st.plotly_chart(
    top_products_chart,
    use_container_width=True,
)



# -------------------------
# DISCOUNT VS PROFIT ANALYSIS
# -------------------------

st.divider()

st.subheader("💰 Discount vs Profit Analysis")

discount_profit_chart = px.scatter(
    filtered,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=[
        "Product Name",
        "Sales",
        "Quantity",
    ],
    title="Relationship Between Discount and Profit",
)

discount_profit_chart.add_hline(
    y=0,
    line_dash="dash",
    line_color="gray",
)

discount_profit_chart.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit",
)

st.plotly_chart(
    discount_profit_chart,
    use_container_width=True,
)
