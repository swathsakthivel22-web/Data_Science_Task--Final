import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("🤖 AI SQL Data Analyst Agent (No API)")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    st.dataframe(df.head())

    conn = sqlite3.connect("data.db")
    df.to_sql("employee", conn, if_exists="replace", index=False)

    def generate_sql(query):
        q = query.lower()

        if "attrition" in q and "department" in q:
            return "SELECT department, COUNT(*) FROM employee WHERE attrition='Yes' GROUP BY department"
        elif "average income" in q:
            return "SELECT AVG(monthly_income) FROM employee"
        elif "count" in q:
            return "SELECT COUNT(*) FROM employee"
        else:
            return "SELECT * FROM employee LIMIT 10"

    query = st.text_input("Ask your question")

    if query:
        sql = generate_sql(query)

        st.subheader("SQL Query")
        st.code(sql)

        result = pd.read_sql_query(sql, conn)

        st.subheader("Result")
        st.dataframe(result)

        if len(result.columns) >= 2:
            fig = px.bar(result, x=result.columns[0], y=result.columns[1])
            st.plotly_chart(fig)
