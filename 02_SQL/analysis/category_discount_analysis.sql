-- Customer Sales Intelligence Project
-- Analysis: Category Profitability and Discount Impact

-- 1. Overall business metrics
SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    SUM(Quantity) AS units_sold,
    COUNT(DISTINCT `Order ID`) AS total_orders,
    COUNT(DISTINCT `Customer ID`) AS total_customers
FROM sales;

-- 2. Category performance
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    SUM(Quantity) AS units_sold
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;

-- 3. Subcategory profitability
SELECT
    Category,
    `Sub-Category`,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(Discount) * 100, 2) AS avg_discount_pct
FROM sales
GROUP BY Category, `Sub-Category`
ORDER BY total_profit ASC;

-- 4. Profitability by discount band
SELECT
    CASE
        WHEN Discount = 0 THEN '0% discount'
        WHEN Discount <= 0.10 THEN '1-10% discount'
        WHEN Discount <= 0.20 THEN '11-20% discount'
        WHEN Discount <= 0.30 THEN '21-30% discount'
        ELSE 'Above 30% discount'
    END AS discount_band,
    COUNT(*) AS sales_records,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct
FROM sales
GROUP BY discount_band
ORDER BY MIN(Discount);

-- 5. Regional Sales and Profitability Analysis

SELECT
    Region,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT `Order ID`) AS total_orders,
    COUNT(DISTINCT `Customer ID`) AS total_customers
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;

-- 6. Monthly Sales Trends

SELECT
    DATE_FORMAT(`Order Date`, '%Y-%m') AS month_label,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT `Order ID`) AS total_orders
FROM sales
GROUP BY DATE_FORMAT(`Order Date`, '%Y-%m')
ORDER BY DATE_FORMAT(`Order Date`, '%Y-%m');

-- 7. Annual Sales Performance

SELECT
    YEAR(`Order Date`) AS sales_year,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT `Order ID`) AS total_orders,
    COUNT(DISTINCT `Customer ID`) AS total_customers
FROM sales
GROUP BY YEAR(`Order Date`)
ORDER BY YEAR(`Order Date`);

-- 8. Year-over-Year Sales Growth

SELECT
    current_year.sales_year,
    ROUND(current_year.total_sales, 2) AS total_sales,
    ROUND(previous_year.total_sales, 2) AS previous_year_sales,
    ROUND(
        (current_year.total_sales - previous_year.total_sales)
        / previous_year.total_sales * 100,
        2
    ) AS yoy_growth_pct
FROM (
    SELECT
        YEAR(`Order Date`) AS sales_year,
        SUM(Sales) AS total_sales
    FROM sales
    GROUP BY YEAR(`Order Date`)
) AS current_year
LEFT JOIN (
    SELECT
        YEAR(`Order Date`) AS sales_year,
        SUM(Sales) AS total_sales
    FROM sales
    GROUP BY YEAR(`Order Date`)
) AS previous_year
    ON current_year.sales_year = previous_year.sales_year + 1
ORDER BY current_year.sales_year;

-- 9. Repeat Customer Analysis

SELECT
    COUNT(*) AS total_customers,
    SUM(customer_orders.order_count > 1) AS repeat_customers,
    SUM(customer_orders.order_count = 1) AS one_time_customers,
    ROUND(
        SUM(customer_orders.order_count > 1) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_rate_pct
FROM (
    SELECT
        `Customer ID`,
        COUNT(DISTINCT `Order ID`) AS order_count
    FROM sales
    GROUP BY `Customer ID`
) AS customer_orders;


-- 10. Top Customers by Sales

SELECT
    `Customer ID`,
    `Customer Name`,
    COUNT(DISTINCT `Order ID`) AS total_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    MAX(`Order Date`) AS last_order_date
FROM sales
GROUP BY `Customer ID`, `Customer Name`
ORDER BY total_sales DESC
LIMIT 10;

-- =====================================================
-- SECTION 11: RFM CUSTOMER SCORING
-- Purpose: Rank customers by recency, frequency, and monetary value
-- Recency: 5 = most recent purchase
-- Frequency: 5 = highest order frequency
-- Monetary: 5 = highest total sales
-- =====================================================

SELECT
    scored.`Customer ID`,
    scored.`Customer Name`,
    scored.recency_days,
    scored.frequency,
    scored.monetary_value,
    scored.recency_score,
    scored.frequency_score,
    scored.monetary_score,
    CONCAT(
        scored.recency_score,
        scored.frequency_score,
        scored.monetary_score
    ) AS rfm_score
FROM (
    SELECT
        rfm.*,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS monetary_score
    FROM (
        SELECT
            `Customer ID`,
            `Customer Name`,
            DATEDIFF(
                (SELECT MAX(`Order Date`) FROM sales),
                MAX(`Order Date`)
            ) AS recency_days,
            COUNT(DISTINCT `Order ID`) AS frequency,
            ROUND(SUM(Sales), 2) AS monetary_value
        FROM sales
        GROUP BY `Customer ID`, `Customer Name`
    ) AS rfm
) AS scored
ORDER BY
    scored.recency_score DESC,
    scored.frequency_score DESC,
    scored.monetary_score DESC;


-- =====================================================
-- SECTION 12: RFM CUSTOMER SEGMENTATION
-- Purpose: Classify customers using RFM scores
-- Note: These are exploratory business rules, not a
-- validated churn prediction model.
-- =====================================================

SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM (
    SELECT
        scored.`Customer ID`,
        CASE
            WHEN scored.recency_score >= 4
             AND scored.frequency_score >= 4
             AND scored.monetary_score >= 4
                THEN 'High-Value'
            WHEN scored.frequency_score >= 4
                THEN 'Loyal'
            WHEN scored.recency_score <= 2
                THEN 'At-Risk'
            ELSE 'Potential'
        END AS customer_segment
    FROM (
        SELECT
            rfm.*,
            NTILE(5) OVER (ORDER BY recency_days DESC) AS recency_score,
            NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
            NTILE(5) OVER (ORDER BY monetary_value ASC) AS monetary_score
        FROM (
            SELECT
                `Customer ID`,
                DATEDIFF(
                    (SELECT MAX(`Order Date`) FROM sales),
                    MAX(`Order Date`)
                ) AS recency_days,
                COUNT(DISTINCT `Order ID`) AS frequency,
                SUM(Sales) AS monetary_value
            FROM sales
            GROUP BY `Customer ID`
        ) AS rfm
    ) AS scored
) AS segmented
GROUP BY customer_segment
ORDER BY customer_count DESC;

-- =====================================================
-- SECTION 13: HIGHEST-VALUE AT-RISK CUSTOMERS
-- Purpose: Identify customers for re-engagement review
-- Ranking: Historical sales, highest first
-- Reference date: Maximum Order Date in the dataset
-- =====================================================

WITH customer_rfm AS (
    SELECT
        `Customer ID`,
        `Customer Name`,
        DATEDIFF(
            (SELECT MAX(`Order Date`) FROM sales),
            MAX(`Order Date`)
        ) AS recency_days,
        COUNT(DISTINCT `Order ID`) AS frequency,
        SUM(Sales) AS monetary_value,
        SUM(Profit) AS total_profit,
        MAX(`Order Date`) AS last_order_date
    FROM sales
    GROUP BY `Customer ID`, `Customer Name`
),
scored AS (
    SELECT
        customer_rfm.*,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS monetary_score
    FROM customer_rfm
),
segmented AS (
    SELECT
        *,
        CASE
            WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
                THEN 'High-Value'
            WHEN frequency_score >= 4
                THEN 'Loyal'
            WHEN recency_score <= 2
                THEN 'At-Risk'
            ELSE 'Potential'
        END AS customer_segment
    FROM scored
)
SELECT
    `Customer ID`,
    `Customer Name`,
    last_order_date,
    recency_days,
    frequency,
    ROUND(monetary_value, 2) AS historical_sales,
    ROUND(total_profit, 2) AS historical_profit
FROM segmented
WHERE customer_segment = 'At-Risk'
ORDER BY monetary_value DESC
LIMIT 10;

-- =====================================================
-- SECTION 14: SUBCATEGORY DISCOUNT AND PROFITABILITY
-- Purpose: Compare sales, profit, discounts, and margins
-- Note: Association does not establish causation.
-- =====================================================

SELECT
    Category,
    `Sub-Category`,
    COUNT(*) AS sales_records,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Discount) * 100, 2) AS avg_discount_pct,
    ROUND(
        SUM(Profit) / NULLIF(SUM(Sales), 0) * 100,
        2
    ) AS profit_margin_pct
FROM sales
GROUP BY Category, `Sub-Category`
ORDER BY total_profit ASC;
