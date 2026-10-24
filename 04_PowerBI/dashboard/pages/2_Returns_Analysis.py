import streamlit as st
import plotly.express as px
import pandas as pd

from dashboard_utils import load_sales_data, load_returns_data

st.set_page_config(
    page_title="Returns Analysis",
    page_icon="↩️",
    layout="wide",
)

st.title("Returns Analysis")
st.caption("Explore returned orders and their impact on sales.")

try:
    df = load_sales_data()
    returned_order_ids = load_returns_data()
except Exception as error:
    st.error(f"Unable to load data: {error}")
    st.stop()

st.sidebar.title("Returns Filters")

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    key="returns_region_filter",
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
    key="returns_category_filter",
)


min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()



start_date = st.sidebar.date_input(
    "From Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="returns_start_date_filter",
    format="YYYY-MM-DD",
)

end_date = st.sidebar.date_input(
    "To Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="returns_end_date_filter",
    format="YYYY-MM-DD",
)


def reset_returns_filters():
    st.session_state["returns_region_filter"] = regions
    st.session_state["returns_category_filter"] = categories
    st.session_state["returns_start_date_filter"] = min_date
    st.session_state["returns_end_date_filter"] = max_date

st.sidebar.divider()

st.sidebar.button(
    "Reset Filters",
    use_container_width=True,
    on_click=reset_returns_filters,
)

df["Is Returned"] = df["Order ID"].isin(returned_order_ids)




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

returned_orders = filtered.loc[
    filtered["Is Returned"], "Order ID"
].nunique()

total_orders = filtered["Order ID"].nunique()
return_rate = (
    returned_orders / total_orders * 100 if total_orders else 0
)

returned_sales = filtered.loc[
    filtered["Is Returned"], "Sales"
].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Returned Orders", f"{returned_orders:,}")
col2.metric("Return Rate", f"{return_rate:.2f}%")
col3.metric("Sales on Returned Orders", f"${returned_sales:,.2f}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Returned Orders by Category")
    category_returns = (
        filtered.loc[filtered["Is Returned"]]
        .groupby("Category", as_index=False)["Order ID"]
        .nunique()
        .rename(columns={"Order ID": "Returned Orders"})
    )

    if category_returns.empty:
        st.info("No returned orders for the selected filters.")
    else:
        fig = px.bar(
            category_returns,
            x="Category",
            y="Returned Orders",
            color="Category",
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Returned Orders by Region")
    region_returns = (
        filtered.loc[filtered["Is Returned"]]
        .groupby("Region", as_index=False)["Order ID"]
        .nunique()
        .rename(columns={"Order ID": "Returned Orders"})
    )

    if region_returns.empty:
        st.info("No returned orders for the selected filters.")
    else:
        fig = px.bar(
            region_returns,
            x="Region",
            y="Returned Orders",
            color="Region",
        )
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Return Rate by Category")

category_summary = (
    filtered.groupby("Category")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Returned_Orders=(
            "Is Returned",
            lambda values: filtered.loc[values.index]
            .loc[values, "Order ID"]
            .nunique(),
        ),
    )
    .reset_index()
)

category_summary["Return Rate (%)"] = (
    category_summary["Returned_Orders"]
    / category_summary["Total_Orders"]
    * 100
)

st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True,
)




# -------------------------
# RETURN RATE BY REGION
# -------------------------

st.divider()

st.subheader("Return Rate by Region")

# Total unique orders by region
region_total_orders = (
    filtered.groupby("Region")["Order ID"]
    .nunique()
    .reset_index(name="Total Orders")
)

# Unique returned orders by region
region_returned_orders = (
    filtered.loc[filtered["Is Returned"]]
    .groupby("Region")["Order ID"]
    .nunique()
    .reset_index(name="Returned Orders")
)

# Combine regional order counts
region_summary = region_total_orders.merge(
    region_returned_orders,
    on="Region",
    how="left",
)

region_summary["Returned Orders"] = (
    region_summary["Returned Orders"]
    .fillna(0)
    .astype(int)
)

# Calculate return rate
region_summary["Return Rate (%)"] = (
    region_summary["Returned Orders"]
    / region_summary["Total Orders"]
    * 100
)

# Create chart
region_return_chart = px.bar(
    region_summary.sort_values(
        "Return Rate (%)",
        ascending=False,
    ),
    x="Region",
    y="Return Rate (%)",
    color="Return Rate (%)",
    title="Return Rate by Region",
    color_continuous_scale=[
        "#E6E1D8",
        "#78917B",
    ],
    hover_data=[
        "Total Orders",
        "Returned Orders",
    ],
)

region_return_chart.update_layout(
    xaxis_title="Region",
    yaxis_title="Return Rate (%)",
)

st.plotly_chart(
    region_return_chart,
    use_container_width=True,
)
