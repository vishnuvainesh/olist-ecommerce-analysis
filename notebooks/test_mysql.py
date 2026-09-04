import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Vishnu2005v",
    database="olist_ecommerce"
)

print("MySQL connection successful!")

conn.close()
