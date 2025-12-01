

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

###4

CREATE INDEX idx_daily_sales_order_date
ON daily_sales(order_date);


CREATE INDEX idx_customer_revenue_total
ON customer_revenue(total_revenue DESC);


### 5

INSERT INTO orders (order_id, customer_id, order_date, status)
VALUES (7, 2, DATE '2024-05-04', 'COMPLETED');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (8, 7, 3, 1, 89.00),
    (9, 7, 4, 1, 19.90);


SELECT *
FROM order_summary
WHERE order_id = 7;

SELECT *
FROM daily_sales
WHERE order_date = '2024-05-04';

REFRESH MATERIALIZED VIEW daily_sales;


SELECT *
FROM daily_sales
WHERE order_date = '2024-05-04';

