SELECT c.customer_id, c.customer_name,
       SUM(oi.quantity * oi.unit_price_cents) AS revenue_cents
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.order_status = 'completed'
GROUP BY c.customer_id, c.customer_name
ORDER BY revenue_cents DESC, c.customer_id;
