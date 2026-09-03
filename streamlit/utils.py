import pandas as pd
from database import get_connection


def run_query(query):
    conn = get_connection()

    try:
        return pd.read_sql(query, con=conn)
    finally:
        conn.close()


def get_value(query, column):
    result = run_query(query)
    return result.iloc[0][column]


def format_currency(value):
    return f"₹{value:,.2f}"


def format_number(value):
    return f"{value:,}"