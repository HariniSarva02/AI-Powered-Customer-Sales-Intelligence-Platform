import streamlit as st
import plotly.express as px

from dashboard_utils import load_sales_data

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="👥",
    layout="wide",
)

st.title("Customer Intelligence")
st.caption(
    "Understand customer value, purchasing behavior, and exploratory segments."
)

try:
    df = load_sales_data()
except Exception as error:
    st.error(f"Unable to load sales data: {error}")
    st.stop()

st.sidebar.title("Customer Filters")

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    key="customer_region_filter",
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
    key="customer_category_filter",
)



min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

start_date = st.sidebar.date_input(
    "From Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="customer_start_date_filter",
    format="YYYY-MM-DD",
)

end_date = st.sidebar.date_input(
    "To Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="customer_end_date_filter",
    format="YYYY-MM-DD",
)

def reset_customer_filters():
    st.session_state["customer_region_filter"] = regions
    st.session_state["customer_category_filter"] = categories
    st.session_state["customer_start_date_filter"] = min_date
    st.session_state["customer_end_date_filter"] = max_date



st.sidebar.divider()

st.sidebar.button(
    "Reset Filters",
    use_container_width=True,
    on_click=reset_customer_filters,
)




if start_date > end_date:
    st.warning("From Date cannot be later than To Date.")
    st.stop()

filtered = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
].copy()




if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Aggregate sales and profit by customer
customer_summary = (
    filtered.groupby(["Customer ID", "Customer Name"], as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
    )
    .sort_values("Sales", ascending=False)
)


total_customers = customer_summary["Customer ID"].nunique()

average_sales = (
    customer_summary["Sales"].mean()
    if total_customers
    else 0
)

profitable_customers = int(
    (customer_summary["Profit"] > 0).sum()
)

repeat_customers = int(
    (customer_summary["Orders"] > 1).sum()
)

repeat_customer_rate = (
    repeat_customers / total_customers * 100
    if total_customers
    else 0
)



col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{total_customers:,}",
)

col2.metric(
    "Average Sales per Customer",
    f"${average_sales:,.2f}",
)

col3.metric(
    "Repeat Customers",
    f"{repeat_customers:,}",
)

col4.metric(
    "Repeat Customer Rate",
    f"{repeat_customer_rate:.2f}%",
)


st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Customers by Sales")
    top_customers = customer_summary.head(10).sort_values("Sales")
    fig = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Highest Sales Customers",
        color="Sales",
        color_continuous_scale=["#E6E1D8", "#78917B"],
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Customer Sales vs. Profit")
    fig = px.scatter(
        customer_summary,
        x="Sales",
        y="Profit",
        hover_name="Customer Name",
        size="Orders",
        title="Sales and Profit by Customer",
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#B87967")
    st.plotly_chart(fig, use_container_width=True)



# -------------------------
# CUSTOMER SEGMENTATION
# -------------------------

st.divider()

st.subheader("Customer Segmentation")

# Classify customers based on number of orders
customer_summary["Customer Segment"] = customer_summary[
    "Orders"
].apply(
    lambda orders: (
        "One-Time Customer"
        if orders == 1
        else "Repeat Customer"
        if orders <= 4
        else "Frequent Customer"
    )
)

# Count customers in each segment
segment_summary = (
    customer_summary["Customer Segment"]
    .value_counts()
    .reset_index()
)

segment_summary.columns = [
    "Customer Segment",
    "Number of Customers",
]

# Create segmentation chart
segment_chart = px.pie(
    segment_summary,
    names="Customer Segment",
    values="Number of Customers",
    title="Customer Distribution by Segment",
    hole=0.45,
)

st.plotly_chart(
    segment_chart,
    use_container_width=True,
)

# Display segment details
st.dataframe(
    segment_summary,
    use_container_width=True,
    hide_index=True,
)


# -------------------------
# CUSTOMER SEGMENT PERFORMANCE
# -------------------------

st.divider()

st.subheader("Customer Segment Performance")

# Aggregate sales and profit by customer segment
segment_performance = (
    customer_summary.groupby(
        "Customer Segment",
        as_index=False,
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Customers=("Customer ID", "nunique"),
    )
)

# Convert performance data into chart format
segment_performance_long = segment_performance.melt(
    id_vars=["Customer Segment"],
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount",
)

# Create comparison chart
segment_performance_chart = px.bar(
    segment_performance_long,
    x="Customer Segment",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Sales and Profit by Customer Segment",
    color_discrete_map={
        "Sales": "#78917B",
        "Profit": "#B87967",
    },
    hover_data={
        "Amount": ":,.2f",
    },
)

segment_performance_chart.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Amount ($)",
)

st.plotly_chart(
    segment_performance_chart,
    use_container_width=True,
)

# Display segment performance details
st.dataframe(
    segment_performance,
    use_container_width=True,
    hide_index=True,
)


st.subheader("Customer Performance Details")

st.dataframe(
    customer_summary,
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download Customer Data (CSV)",
    data=customer_summary.to_csv(index=False).encode("utf-8"),
    file_name="customer_performance.csv",
    mime="text/csv",
)






# -------------------------
# CUSTOMER SEGMENT SUMMARY
# -------------------------

st.divider()

st.subheader("Customer Segment Summary")

# Calculate customer and sales percentages
segment_summary_metrics = segment_performance.copy()

total_segment_customers = segment_summary_metrics[
    "Customers"
].sum()

total_segment_sales = segment_summary_metrics[
    "Sales"
].sum()

segment_summary_metrics["Customer Share (%)"] = (
    segment_summary_metrics["Customers"]
    / total_segment_customers
    * 100
)

segment_summary_metrics["Sales Share (%)"] = (
    segment_summary_metrics["Sales"]
    / total_segment_sales
    * 100
)

# Display summary table
st.dataframe(
    segment_summary_metrics[
        [
            "Customer Segment",
            "Customers",
            "Customer Share (%)",
            "Sales",
            "Sales Share (%)",
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Customer Share (%)": st.column_config.NumberColumn(
            "Customer Share (%)",
            format="%.2f%%",
        ),
        "Sales Share (%)": st.column_config.NumberColumn(
            "Sales Share (%)",
            format="%.2f%%",
        ),
        "Sales": st.column_config.NumberColumn(
            "Sales",
            format="$%.2f",
        ),
    },
)
