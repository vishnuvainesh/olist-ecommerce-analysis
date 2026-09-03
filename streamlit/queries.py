# ============================================================
# OLIST E-COMMERCE ANALYTICS
# queries.py
# ============================================================


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

TOTAL_REVENUE = """
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items
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
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_items
"""


AVERAGE_REVIEW_SCORE = """
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews
"""


# ============================================================
# SALES ANALYSIS
# ============================================================

MONTHLY_REVENUE = """
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS month,

    ROUND(
        SUM(oi.price),
        2
    ) AS monthly_revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    )

ORDER BY month
"""


REVENUE_BY_CATEGORY = """
SELECT
    p.product_category_name AS category,

    ROUND(
        SUM(oi.price),
        2
    ) AS revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

WHERE p.product_category_name IS NOT NULL

GROUP BY
    p.product_category_name

ORDER BY revenue DESC
"""


CATEGORY_PERFORMANCE = """
SELECT
    p.product_category_name AS category,

    COUNT(*) AS units_sold,

    ROUND(
        SUM(oi.price),
        2
    ) AS revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

WHERE p.product_category_name IS NOT NULL

GROUP BY
    p.product_category_name

ORDER BY revenue DESC
"""


TOP_SELLING_PRODUCTS = """
SELECT
    oi.product_id,

    COUNT(*) AS units_sold,

    ROUND(
        SUM(oi.price),
        2
    ) AS revenue

FROM order_items oi

GROUP BY
    oi.product_id

ORDER BY
    units_sold DESC

LIMIT 10
"""


SALES_BY_LOCATION = """
SELECT
    c.customer_state AS state,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(oi.price),
        2
    ) AS revenue

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_state

ORDER BY
    revenue DESC
"""


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

CUSTOMER_DISTRIBUTION = """
SELECT
    customer_state AS state,

    COUNT(
        DISTINCT customer_unique_id
    ) AS customers

FROM customers

GROUP BY
    customer_state

ORDER BY
    customers DESC
"""


CUSTOMER_SPENDING = """
SELECT
    c.customer_unique_id,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_unique_id

ORDER BY
    total_spending DESC
"""


REPEAT_VS_NEW_CUSTOMERS = """
SELECT
    CASE
        WHEN order_count = 1
            THEN 'New Customer'

        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS customers

FROM
(
    SELECT
        c.customer_unique_id,

        COUNT(
            DISTINCT o.order_id
        ) AS order_count

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    GROUP BY
        c.customer_unique_id

) AS customer_orders

GROUP BY
    customer_type

ORDER BY
    customers DESC
"""


TOP_CUSTOMERS = """
SELECT
    c.customer_unique_id,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_unique_id

ORDER BY
    total_spending DESC

LIMIT 5
"""


# ============================================================
# SELLER & PRODUCT ANALYSIS
# ============================================================

TOP_SELLERS = """
SELECT
    seller_id,

    COUNT(*) AS units_sold,

    ROUND(
        SUM(price),
        2
    ) AS revenue

FROM order_items

GROUP BY
    seller_id

ORDER BY
    units_sold DESC

LIMIT 10
"""


SELLER_REVENUE = """
SELECT
    seller_id,

    ROUND(
        SUM(price),
        2
    ) AS seller_revenue

FROM order_items

GROUP BY
    seller_id

ORDER BY
    seller_revenue DESC

LIMIT 10
"""


SELLER_RATINGS = """
SELECT
    oi.seller_id,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_rating

FROM order_items oi

JOIN order_reviews r
    ON oi.order_id = r.order_id

GROUP BY
    oi.seller_id

HAVING COUNT(r.review_score) >= 5

ORDER BY
    average_rating DESC

LIMIT 10
"""


# ============================================================
# DELIVERY ANALYSIS
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

        WHEN order_delivered_customer_date
             <= order_estimated_delivery_date
            THEN 'On Time'

        ELSE 'Delayed'

    END AS delivery_status,

    COUNT(*) AS total_orders

FROM orders

WHERE
    order_delivered_customer_date IS NOT NULL

    AND order_estimated_delivery_date IS NOT NULL

GROUP BY
    delivery_status

ORDER BY
    total_orders DESC
"""


DELIVERY_BY_LOCATION = """
SELECT
    c.customer_state AS state,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders,

    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_days

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE
    o.order_delivered_customer_date IS NOT NULL

GROUP BY
    c.customer_state

ORDER BY
    average_delivery_days DESC
"""


# ============================================================
# DELIVERY VS REVIEW
# ============================================================

DELIVERY_DELAY_VS_REVIEW = """
SELECT
    r.review_score AS review_score,

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

FROM orders o

JOIN order_reviews r
    ON o.order_id = r.order_id

WHERE
    o.order_delivered_customer_date IS NOT NULL

    AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY
    r.review_score

ORDER BY
    r.review_score
"""


# ============================================================
# CUSTOMER EXPERIENCE
# ============================================================

REVIEW_SCORE_DISTRIBUTION = """
SELECT
    review_score,

    COUNT(*) AS total_reviews

FROM order_reviews

GROUP BY
    review_score

ORDER BY
    review_score
"""


REVIEWS_BY_CATEGORY = """
SELECT
    p.product_category_name AS category,

    COUNT(*) AS total_reviews,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_rating

FROM order_reviews r

JOIN orders o
    ON r.order_id = o.order_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

WHERE
    p.product_category_name IS NOT NULL

GROUP BY
    p.product_category_name

ORDER BY
    total_reviews DESC

LIMIT 10
"""


# Same analysis as DELIVERY_DELAY_VS_REVIEW.
# Kept as a separate query because the dashboard
# uses it specifically on the Reviews page.

RATING_VS_DELIVERY = """
SELECT
    r.review_score AS review_score,

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

GROUP BY
    r.review_score

ORDER BY
    r.review_score
"""