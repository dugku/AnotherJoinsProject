import streamlit as st
import pyodbc

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
        +";TrustServerCertificate=yes;"
    )

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

quety = ("""
SELECT TOP 2000 *
FROM CONTRIBUTING_FACTOR
WHERE FACTOR_DESCRIPTION != 'Unspecified'
""")
rows = run_query(quety)

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
