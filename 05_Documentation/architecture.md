# Project Architecture — Customer Sales Intelligence Platform

## 1. Overview

The Customer Sales Intelligence Platform is an end-to-end analytics project designed to transform raw retail sales data into validated datasets, business intelligence metrics, customer segmentation, and interactive reporting.

## 2. Technology Stack

- **Python:** Data inspection, cleaning, validation, and analysis
- **Pandas and NumPy:** Data manipulation and numerical analysis
- **MySQL:** Structured storage and SQL-based business analysis
- **Power Query:** Data import and transformation for Power BI
- **Power BI:** Interactive dashboards, KPIs, and business reporting
- **Git and GitHub:** Version control and portfolio presentation

## 3. Data Pipeline

1. **Raw data:** Preserve the original source file in `01_Data/raw/`.
2. **Data preparation:** Split the source into sales, returns, and people datasets.
3. **Cleaning and validation:** Use Python scripts to inspect missing values, correct postal-code formatting, validate dates, and compare business totals.
4. **Supporting datasets:** Maintain the date dimension and create a unique returned-order list for safer modeling.
5. **SQL analysis:** Store sales data in MySQL and use SQL to analyze profitability, discounts, regions, trends, and customer purchasing behavior.
6. **Data modeling:** Define relationships between sales, dates, returns, and regional representatives without multiplying sales records.
7. **Business intelligence:** Build interactive Power BI reports with KPI cards, trend charts, profitability analysis, and customer insights.
8. **Documentation and delivery:** Record data definitions, analytical findings, screenshots, and project instructions.

## 4. Current Data Assets

| Asset | Purpose |
|---|---|
| `Superstore_21col.csv` | Original combined source file |
| `sales.csv` | Cleaned sales dataset |
| `sales_powerbi_ready.csv` | Sales dataset with postal-code formatting corrected |
| `returns.csv` | Original returns records |
| `returns_orders.csv` | Unique returned-order IDs for modeling |
| `people.csv` | Regional sales representative mapping |
| `date_dimension.csv` | Calendar attributes for time-based analysis |

## 5. Analytical Scope

The project includes:

- Overall sales, profit, order, and customer KPIs
- Category and subcategory profitability
- Discount-band analysis
- Regional performance
- Monthly and annual sales trends
- Repeat-customer analysis
- RFM-based customer segmentation
- Identification of high-value customers who may need re-engagement

## 6. Data Integrity Principles

- Preserve raw source data.
- Keep reproducible cleaning scripts.
- Validate row counts and business totals after transformations.
- Avoid joins that duplicate sales or profit.
- Distinguish observed relationships from proven causation.
- Document assumptions and limitations.

## 7. Delivery Status

Data preparation and initial SQL analysis are underway. Power BI modeling, dashboard development, and final portfolio documentation will be completed in subsequent project stages.