SELECT p.product_name,
       SUM(oi.quantity) AS units_sold,
       SUM(oi.quantity * oi.unit_price_cents) AS revenue_cents
FROM products AS p
JOIN order_items AS oi ON oi.product_id = p.product_id
JOIN orders AS o ON o.order_id = oi.order_id
WHERE o.order_status = 'completed'
GROUP BY p.product_id, p.product_name
ORDER BY revenue_cents DESC, p.product_name;
