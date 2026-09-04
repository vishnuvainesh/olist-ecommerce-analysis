# ============================================================
# OLIST MARKETPLACE INTELLIGENCE
# SQL QUERIES
# ============================================================


# ============================================================
# OVERVIEW / KPI QUERIES
# ============================================================

TOTAL_REVENUE = """
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM order_payments
"""


TOTAL_ORDERS = """
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
"""


TOTAL_CUSTOMERS = """
SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers
"""


TOTAL_SELLERS = """
SELECT
    COUNT(DISTINCT seller_id) AS total_sellers
FROM sellers
"""


AVERAGE_ORDER_VALUE = """
SELECT
    ROUND(
        SUM(payment_value) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM order_payments
"""


AVERAGE_REVIEW_SCORE = """
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews
"""


# ============================================================
# REVENUE
# ============================================================

MONTHLY_REVENUE = """
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
WHERE o.order_status <> 'canceled'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY month
"""


REVENUE_BY_CATEGORY = """
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    )
ORDER BY revenue DESC
"""


CATEGORY_PERFORMANCE = """
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,
    COUNT(*) AS units_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    )
ORDER BY revenue DESC
"""


# ============================================================
# GEOGRAPHIC SALES
# ============================================================

SALES_BY_LOCATION = """
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC
"""


# ============================================================
# REVIEWS
# ============================================================

REVIEW_SCORE_DISTRIBUTION = """
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score
"""


REVIEWS_BY_CATEGORY = """
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,
    ROUND(AVG(r.review_score), 2) AS average_review_score,
    COUNT(*) AS total_reviews
FROM order_reviews r
JOIN orders o
    ON r.order_id = o.order_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    )
ORDER BY average_review_score DESC
"""


RATING_VS_DELIVERY = """
SELECT
    r.review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_estimated_delivery_date
            )
        ),
        2
    ) AS average_delivery_delay
FROM order_reviews r
JOIN orders o
    ON r.order_id = o.order_id
WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score
"""


# ============================================================
# CUSTOMERS
# ============================================================

CUSTOMER_DISTRIBUTION = """
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT c.customer_unique_id) AS customers
FROM customers c
GROUP BY c.customer_state
ORDER BY customers DESC
"""


REPEAT_VS_NEW_CUSTOMERS = """
SELECT
    CASE
        WHEN order_count > 1 THEN 'Repeat Customers'
        ELSE 'New Customers'
    END AS customer_type,
    COUNT(*) AS customers
FROM
(
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) customer_orders
GROUP BY
    CASE
        WHEN order_count > 1 THEN 'Repeat Customers'
        ELSE 'New Customers'
    END
ORDER BY customers DESC
"""


CUSTOMER_SPENDING = """
SELECT
    c.customer_unique_id,
    ROUND(SUM(p.payment_value), 2) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC
"""


TOP_CUSTOMERS = """
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC
LIMIT 50
"""


# ============================================================
# SELLERS
# ============================================================

TOP_SELLERS = """
SELECT
    oi.seller_id,
    COUNT(*) AS units_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.seller_id
ORDER BY revenue DESC
LIMIT 50
"""


# ============================================================
# PRODUCTS
# ============================================================

TOP_SELLING_PRODUCTS = """
SELECT
    oi.product_id,
    COUNT(*) AS units_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY units_sold DESC
LIMIT 50
"""


# ============================================================
# DELIVERY
# ============================================================

AVERAGE_DELIVERY_TIME = """
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
    AND order_purchase_timestamp IS NOT NULL
"""


ON_TIME_VS_DELAYED = """
SELECT
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
            THEN 'On Time'
        ELSE 'Delayed'
    END AS delivery_status,
    COUNT(*) AS orders
FROM orders
WHERE
    order_delivered_customer_date IS NOT NULL
    AND order_estimated_delivery_date IS NOT NULL
GROUP BY
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
            THEN 'On Time'
        ELSE 'Delayed'
    END
ORDER BY orders DESC
"""


DELIVERY_BY_LOCATION = """
SELECT
    c.customer_state AS state,
    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_time
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL
GROUP BY c.customer_state
ORDER BY average_delivery_time DESC
"""


DELIVERY_DELAY_VS_REVIEW = """
SELECT
    r.review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_estimated_delivery_date
            )
        ),
        2
    ) AS average_delivery_delay
FROM order_reviews r
JOIN orders o
    ON r.order_id = o.order_id
WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score
"""


# ============================================================
# END
# ============================================================