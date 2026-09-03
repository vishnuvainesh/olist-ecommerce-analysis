import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mypassword",
    database="olist_ecommerce"
)

print("MySQL connection successful!")

conn.close()