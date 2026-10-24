# Data Dictionary — Customer Sales Intelligence Platform

## 1. Sales Dataset

**File:** `01_Data/cleaned/sales_powerbi_ready.csv`

**Grain:** One row per sales line item.

| Column | Description |
|---|---|
| Row ID | Unique identifier for a sales row |
| Order ID | Identifier for the customer order |
| Order Date | Date the order was placed |
| Ship Date | Date the order was shipped |
| Ship Mode | Shipping method |
| Customer ID | Unique customer identifier |
| Customer Name | Customer's name |
| Segment | Customer segment |
| Country | Country of the sale |
| City | Customer's city |
| State | Customer's state |
| Postal Code | Postal code; 11 records are missing |
| Region | Sales region |
| Product ID | Product identifier |
| Category | Product category |
| Sub-Category | Product subcategory |
| Product Name | Product description |
| Sales | Sales amount |
| Quantity | Units sold |
| Discount | Discount rate |
| Profit | Profit amount |

**Validated row count:** 9,994

## 2. Returns Dataset

**Original file:** `01_Data/cleaned/returns.csv`

**Power BI relationship file:** `01_Data/cleaned/returns_orders.csv`

The original file contains 800 rows and 296 unique returned order IDs. The relationship file retains one row per unique returned order ID to avoid duplicating sales records through repeated order IDs.

## 3. People Dataset

**File:** `01_Data/cleaned/people.csv`

| Column | Description |
|---|---|
| Person | Regional sales representative |
| Region | Region assigned to the representative |

**Validated row count:** 4

## 4. Date Dimension

**File:** `01_Data/cleaned/date_dimension.csv`

Contains 1,458 unique dates and date attributes, including year, quarter, month, week number, day, and day name. It covers all order dates in the sales dataset.

## 5. Data Quality Checks

- Sales dataset contains 9,994 rows.
- No duplicate sales rows were detected.
- Key business columns contain no missing values.
- Eleven postal codes are missing and remain unfilled.
- Postal codes were cleaned to remove trailing `.0` formatting.
- No invalid order or ship dates were detected.
- All unique returned order IDs exist in the sales dataset.
- The date dimension contains no duplicate dates and covers all order dates.
- Sales and profit totals match between `sales.csv` and `sales_powerbi_ready.csv`.

## 6. Important Modeling Notes

- Use `sales_powerbi_ready.csv` for the cleaned sales table.
- Use `returns_orders.csv` for a unique returned-order list.
- Avoid joining the original repeated return records directly to sales in a way that multiplies sales or profit.
- Treat sales, profit, quantity, and discount as separate business measures.
- Investigate relationships and filter directions before finalizing the BI model.