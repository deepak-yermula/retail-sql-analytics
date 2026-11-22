WITH customer_revenue AS (
 SELECT c.customer_id, c.customer_name, c.country,
        SUM(oi.quantity * oi.unit_price_cents) AS revenue_cents
 FROM customers c
 JOIN orders o ON o.customer_id = c.customer_id
 JOIN order_items oi ON oi.order_id = o.order_id
 WHERE o.order_status = 'completed'
 GROUP BY c.customer_id, c.customer_name, c.country
)
SELECT country, customer_name, revenue_cents,
       DENSE_RANK() OVER (PARTITION BY country ORDER BY revenue_cents DESC) AS country_revenue_rank
FROM customer_revenue
ORDER BY country, country_revenue_rank, customer_name;
