import pandas as pd
import mysql.connector

# -----------------------------
# MySQL connection
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mypassword",
    database="olist_ecommerce"
)

cursor = conn.cursor()

# Location of cleaned CSV files
base_path = r"D:\project1_GUVI\data\cleaned"


def load_table(file_name, table_name, columns, batch_size=5000):

    file_path = base_path + "\\" + file_name

    print(f"\nLoading {file_name}...")

    df = pd.read_csv(file_path)

    # Replace NaN with None
    df = df.where(pd.notna(df), None)

    column_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = f"""
        INSERT INTO {table_name} ({column_list})
        VALUES ({placeholders})
    """

    data = df[columns].itertuples(index=False, name=None)

    batch = []

    for row in data:
        batch.append(row)

        if len(batch) == batch_size:
            cursor.executemany(query, batch)
            conn.commit()
            batch = []

    # Insert remaining rows
    if batch:
        cursor.executemany(query, batch)
        conn.commit()

    print(f"{table_name} loaded: {len(df)} rows")


# ==========================================
# LOAD TABLES
# ==========================================

# 1. Customers
load_table(
    "customers.csv",
    "customers",
    [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]
)

# 2. Products
load_table(
    "products.csv",
    "products",
    [
        "product_id",
        "product_category_name",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]
)

# 3. Sellers
load_table(
    "sellers.csv",
    "sellers",
    [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ]
)

# 4. Category Translation
load_table(
    "category_translation.csv",
    "category_translation",
    [
        "product_category_name",
        "product_category_name_english"
    ]
)

# 5. Orders
load_table(
    "orders.csv",
    "orders",
    [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)

# 6. Order Items
load_table(
    "order_items.csv",
    "order_items",
    [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]
)

# 7. Order Payments
load_table(
    "order_payments.csv",
    "order_payments",
    [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]
)

# 8. Order Reviews
load_table(
    "order_reviews.csv",
    "order_reviews",
    [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]
)

# 9. Geolocation
load_table(
    "geolocation.csv",
    "geolocation",
    [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]
)

cursor.close()
conn.close()

print("\n================================")
print("ALL DATASETS LOADED SUCCESSFULLY")
print("================================")