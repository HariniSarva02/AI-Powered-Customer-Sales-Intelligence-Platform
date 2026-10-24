
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "cleaned"
    / "sales_powerbi_ready.csv"
)

RETURNS_FILE = (
    PROJECT_ROOT
    / "01_Data"
    / "cleaned"
    / "returns_orders.csv"
)


@st.cache_data
def load_sales_data():
    df = pd.read_csv(DATA_FILE)
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )
    df["Order ID"] = df["Order ID"].astype(str).str.strip()
    df["Customer ID"] = df["Customer ID"].astype(str).str.strip()
    return df


@st.cache_data
def load_returns_data():
    returns_df = pd.read_csv(RETURNS_FILE)
    return set(
        returns_df["Order ID"]
        .dropna()
        .astype(str)
        .str.strip()
    )
