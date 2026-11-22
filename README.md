# Retail Sales SQL Analytics

**Category:** SQL analytics and relational data modeling  
**Tech:** Python 3.10+, SQLite (SQL uses SQLite dialect; some functions differ in PostgreSQL/Snowflake)

## Business question

How can a retail business identify its top customers, best-selling products, monthly revenue, and order performance from normalized sales data?

## Data model

- `customers(customer_id, customer_name, country)`
- `products(product_id, category, product_name, unit_price_cents)`
- `orders(order_id, customer_id, order_date, order_status)`
- `order_items(order_id, product_id, quantity, unit_price_cents)`

All data is synthetic. Money is represented using **integer cents** to avoid floating-point rounding errors.

## Run locally

```bash
python src/setup_db.py
python src/run_queries.py
python -m unittest discover -s tests -v
```

No pip dependencies. The scripts generate `retail.db` and print the analysis results.

## Queries included

1. Revenue by month, excluding cancelled orders (`sql/01_monthly_revenue.sql`).
2. Top spending customers (`sql/02_top_customers.sql`).
3. Top-selling products by revenue (`sql/03_top_products.sql`).
4. Customers ranked by revenue within country using a window function (`sql/04_country_rank.sql`).
5. Customer lifetime value via a common table expression (`sql/05_customer_ltv.sql`).

## Expected results from the synthetic sample

- Completed order revenue: **$725.00** (72,500 cents).
- Cancelled orders do not contribute revenue.
- The top revenue product should be **Laptop** ($500.00).

These assertions are verified in the unit tests.

## Interview discussion prompts

- Why is the data split into four tables?
- How do you avoid double-counting when joining orders and order items?
- What changes would be needed for millions of rows, indexes, and a columnar cloud warehouse?
- Why should cancelled orders be excluded from recognized sales revenue?

## Next improvements

Add slowly changing product dimensions, indexes for frequently filtered attributes, and a separate refund model.
