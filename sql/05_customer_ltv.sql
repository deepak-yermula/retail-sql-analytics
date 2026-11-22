WITH paid_orders AS (
 SELECT o.customer_id, o.order_id,
        SUM(oi.quantity * oi.unit_price_cents) AS order_total_cents
 FROM orders o
 JOIN order_items oi ON oi.order_id = o.order_id
 WHERE o.order_status = 'completed'
 GROUP BY o.customer_id, o.order_id
)
SELECT c.customer_name, COUNT(po.order_id) AS total_orders,
       COALESCE(SUM(po.order_total_cents), 0) AS lifetime_value_cents
FROM customers c
LEFT JOIN paid_orders po ON po.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY lifetime_value_cents DESC, c.customer_name;
