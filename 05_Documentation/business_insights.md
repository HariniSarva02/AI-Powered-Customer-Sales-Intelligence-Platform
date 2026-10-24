# Business Insights — Customer Sales Intelligence Platform

## 1. Executive Summary

The Superstore dataset contains 9,994 sales line items covering January 2015 through December 2018. The analysis examines sales performance, profitability, discount patterns, regional results, and historical customer purchasing behavior.

### Overall Performance

- Total sales: $2,297,200.86
- Total profit: $286,397.02
- Total quantity sold: 37,873
- Distinct orders: 5,009
- Distinct customers: 793
- Overall profit margin: approximately 12.47%

These values are based on the locally validated sales dataset.

## 2. Category Performance

Technology generated the highest category sales at approximately $836,154.10 and profit of $145,455.66.

Office Supplies generated approximately $122,490.88 in profit from $719,046.99 in sales.

Furniture generated approximately $741,999.98 in sales but only $18,451.25 in profit, producing a margin of approximately 2.49%.

**Business implication:** Investigate Furniture's product mix, discounting, and cost structure to identify opportunities to improve profitability. The category-level results alone do not establish the cause of its low margin.

## 3. Discount and Profitability Patterns

The SQL analysis found the following results:

- Orders with no discount generated approximately $320,987.88 in profit.
- The 21–30% discount band generated a loss of approximately $10,369.34.
- The above-30% discount band generated a loss of approximately $125,007.10.
- Combined losses in the two bands above 20% discount were approximately $135,376.44.

**Business implication:** Review heavily discounted transactions, especially those associated with negative profit. These findings show an association between discount bands and profitability, not proof that discounts alone caused the losses.

## 4. Subcategory Opportunities

### Areas requiring investigation

- Tables: approximately $17,725.59 in losses, with an average discount of 26.13%.
- Bookcases: approximately $3,472.56 in losses, with an average discount of 21.11%.
- Supplies: approximately $1,188.99 in losses, with an average discount of 7.68%.
- Machines: approximately 1.79% profit margin and 30.61% average discount.

### Stronger profitability examples

- Copiers: approximately $55,617.90 in profit and a 37.20% margin.
- Accessories: approximately $41,936.78 in profit and a 25.05% margin.
- Paper: approximately $34,053.34 in profit and a 43.39% margin.

**Business implication:** Investigate loss-making subcategories and compare pricing, discounts, shipping, and product costs before recommending changes. Use profitable subcategories as comparison points, while accounting for differences in product mix.

## 5. Regional Performance

- West: approximately $725,457.93 in sales and $108,418.79 in profit.
- East: approximately $678,781.36 in sales and $91,522.84 in profit.
- Central: approximately $501,239.88 in sales and $39,706.45 in profit.
- South: approximately $391,721.90 in sales and $46,749.71 in profit.

**Business implication:** West leads the regions in sales and profit. Central has the lowest regional profit margin among the four regions, at approximately 7.92%, making it a useful area for further investigation.

## 6. Sales Trends

Annual sales were approximately:

| Year | Sales | Year-over-year sales growth |
|---|---:|---:|
| 2015 | $484,247.56 | — |
| 2016 | $470,532.46 | -2.83% |
| 2017 | $609,205.86 | 29.47% |
| 2018 | $733,215.19 | 20.36% |

Sales declined slightly in 2016 and increased substantially in 2017 and 2018.

November 2018 was the strongest month by sales in the monthly analysis, at approximately $118,447.81.

**Business implication:** Examine monthly trends and year-end performance to support planning. More years of data would be needed to establish a reliable long-term seasonal pattern.

## 7. Customer Analysis and RFM Segmentation

Across the four-year dataset:

- 793 distinct customers were identified.
- 781 customers had more than one order.
- The historical repeat-customer rate was approximately 98.49%.

RFM segmentation produced these groups:

| Segment | Customers |
|---|---:|
| At-Risk | 258 |
| Potential | 219 |
| Loyal | 207 |
| High-Value | 109 |

The At-Risk group contains customers with relatively low recency scores under the project's RFM rules. This is a historical segmentation, not a validated churn prediction.

**Business implication:** Review high-value customers in the At-Risk segment for targeted re-engagement. Validate segment definitions and customer behavior before deploying marketing campaigns.

## 8. Customer Profitability

The highest-sales customer in the top-customer analysis generated approximately $25,043.07 in sales but had a historical loss of approximately $1,980.75.

**Business implication:** Evaluate customer value using both sales and profit. High revenue does not necessarily mean high profitability.

## 9. Recommended Next Actions

1. Investigate loss-making product subcategories and heavily discounted transactions.
2. Review Furniture's low overall margin and Central's regional profitability.
3. Evaluate customer-level profit alongside customer sales.
4. Use RFM segments to prioritize further customer analysis and possible re-engagement.
5. Build interactive reports that allow users to explore performance by date, region, category, subcategory, and customer segment.

## 10. Analytical Limitations

- The dataset covers historical transactions from 2015 to 2018, not current retail performance.
- Observational patterns do not establish causation.
- RFM segments are rule-based and have not been validated as churn predictions.
- Business recommendations should be tested against costs, operational context, and additional data before implementation.