import streamlit as st
import mysql.connector


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            ssl_disabled=False
        )

        return conn

    except Exception as e:
        st.error(f"Database connection failed: {e}")
        raise