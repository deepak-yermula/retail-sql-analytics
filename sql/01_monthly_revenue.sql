SELECT substr(o.order_date, 1, 7) AS sales_month,
       SUM(oi.quantity * oi.unit_price_cents) AS revenue_cents,
       COUNT(DISTINCT o.order_id) AS completed_orders
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.order_status = 'completed'
GROUP BY substr(o.order_date, 1, 7)
ORDER BY sales_month;
