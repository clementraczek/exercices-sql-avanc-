

### 1. Synthèse des commandes



```sql
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.order_id,
    o.customer_id,
    c.full_name,
    o.order_date,
    o.status,
    SUM(oi.quantity * oi.unit_price) AS total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, c.full_name, o.order_date, o.status;

SELECT *
FROM order_summary
WHERE status = 'COMPLETED'
ORDER BY order_date, order_id;
---

### 2. Statistiques de ventes par jour

DROP MATERIALIZED VIEW IF EXISTS daily_sales;

CREATE MATERIALIZED VIEW daily_sales AS
SELECT
    o.order_date,
    COUNT(*) AS completed_orders,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'COMPLETED'
GROUP BY o.order_date;

SELECT *
FROM daily_sales
ORDER BY order_date;

SELECT *
FROM daily_sales
WHERE total_revenue >= 200
ORDER BY order_date;


---

### 3. Clients les plus rentables



DROP MATERIALIZED VIEW IF EXISTS customer_revenue;

CREATE MATERIALIZED VIEW customer_revenue AS
SELECT
    c.customer_id,
    c.full_name,
    COUNT(*) AS completed_orders,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id, c.full_name;

SELECT *
FROM customer_revenue
ORDER BY total_revenue DESC;

SELECT *
FROM customer_revenue
WHERE completed_orders >= 2;
---
