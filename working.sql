USE olist_ecommerce;

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2)
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

CREATE TABLE category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(30),
    payment_installments INT,
    payment_value DECIMAL(10,2),
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat DECIMAL(10,7),
    geolocation_lng DECIMAL(10,7),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);

SHOW TABLES;

USE olist_ecommerce;
SHOW TABLES;

USE olist_ecommerce;

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'category_translation', COUNT(*) FROM category_translation
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL
SELECT 'geolocation', COUNT(*) FROM geolocation;

DESCRIBE customers;
DESCRIBE products;
DESCRIBE sellers;
DESCRIBE orders;
DESCRIBE order_items;
DESCRIBE order_payments;
DESCRIBE order_reviews;
DESCRIBE geolocation;
DESCRIBE category_translation;

SELECT *
FROM orders
LIMIT 5;

SELECT *
FROM customers
LIMIT 5;

SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'olist_ecommerce'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;


SELECT
    order_id,
    ROUND(SUM(price), 2) AS total_order_value
FROM order_items
GROUP BY order_id;

-- ============================================
-- 7.2 Delivery Days
-- ============================================

SELECT
    order_id,
    DATEDIFF(
        order_delivered_customer_date,
        order_purchase_timestamp
    ) AS delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- ============================================
-- 7.3 Delivery Delay
--- Negative → Early
--- zero     → On time
--- Positive → Late

SELECT
    order_id,
    DATEDIFF(
        order_delivered_customer_date,
        order_estimated_delivery_date
    ) AS delivery_delay
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- ============================================
-- 7.4 Customer Order Count

SELECT
    customer_id,
    COUNT(order_id) AS customer_order_count
FROM orders
GROUP BY customer_id;

-- ============================================
-- 7.5 Customer Total Spending

SELECT
    o.customer_id,
    ROUND(SUM(oi.price), 2) AS customer_total_spending
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.customer_id;

-- ============================================
-- 7.6 Average Order Value

SELECT
    o.customer_id,
    ROUND(
        SUM(oi.price) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.customer_id;

-- ============================================
-- 7.7 Seller Revenue

SELECT
    seller_id,
    ROUND(SUM(price), 2) AS seller_revenue
FROM order_items
GROUP BY seller_id
ORDER BY seller_revenue DESC;

-- ============================================
-- 7.8 Seller Order Count

SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS seller_order_count
FROM order_items
GROUP BY seller_id
ORDER BY seller_order_count DESC;

-- ============================================
-- 7.9 Repeat Customer Indicator
-- 1 → Repeat customer (more than 1 order)
-- 0 → One-time customer (only 1 order)

SELECT
    customer_id,
    COUNT(order_id) AS customer_order_count,
    CASE
        WHEN COUNT(order_id) > 1 THEN 1
        ELSE 0
    END AS repeat_customer
FROM orders
GROUP BY customer_id;

SELECT 
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;


SHOW DATABASES;
USE olist_ecommerce;
SHOW TABLES;

SELECT
    COUNT(*) AS delivered_orders,
    MIN(order_purchase_timestamp) AS first_purchase,
    MAX(order_purchase_timestamp) AS last_purchase,
    MIN(order_delivered_customer_date) AS first_delivery,
    MAX(order_delivered_customer_date) AS last_delivery
FROM orders
WHERE
    order_delivered_customer_date IS NOT NULL
    AND order_purchase_timestamp IS NOT NULL;
    
    
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_time
FROM orders
WHERE
    order_delivered_customer_date IS NOT NULL
    AND order_purchase_timestamp IS NOT NULL;