import streamlit as st
import sqlite3
from datetime import datetime

def get_conn():
    return sqlite3.connect("my_insurance.db", check_same_thread=False)

conn = get_conn()
cursor = conn.cursor()

st.title(" xyz Bank : Health Insurance ")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Customer", "📜 Add Policy", "📝 Assign Policy", "📂 View Database"])

# Add Customer
with tab1:
    st.subheader("Add New Customer")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=20)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    bmi = st.number_input("BMI", min_value=100)

    if st.button("Add Customer"):
        cursor.execute("INSERT INTO Customer (name, age, gender, bmi) VALUES (?, ?, ?, ?)", 
                       (name, age, gender, bmi))
        conn.commit()
        st.success("Customer added!")

# Add Policy
with tab2:
    st.subheader("Add New Insurance Policy")
    policy_name = st.text_input("Policy Name")
    premium = st.number_input("Premium", min_value=1)
    coverage = st.number_input("Coverage Amount", min_value=1)
    duration = st.text_input("Duration (e.g. 1 Year)")

    if st.button("Add Policy"):
        cursor.execute("INSERT INTO InsurancePolicy (policy_name, premium, coverage, duration) VALUES (?, ?, ?, ?)", 
                       (policy_name, premium, coverage, duration))
        conn.commit()
        st.success("Policy added sucessfully!")

# Assign Policy to Customer
with tab3:
    st.subheader("Assign Policy to Customer")

    customers = cursor.execute("SELECT id, name FROM Customer").fetchall()
    policies = cursor.execute("SELECT id, policy_name FROM InsurancePolicy").fetchall()

    customer_options = {f"{c[1]} (ID: {c[1]})": c[1] for c in customers}
    policy_options = {f"{p[1]} (ID: {p[1]})": p[1] for p in policies}

    selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
    selected_policy = st.selectbox("Select Policy", list(policy_options.keys()))
    start_date = st.date_input("Policy Start Date", datetime.today())

    if st.button("Assign Policy"):
        cursor.execute("INSERT INTO CustomerPolicy (customer_id, policy_id, start_date) VALUES (?, ?, ?)",
                       (customer_options[selected_customer], policy_options[selected_policy], str(start_date)))
        conn.commit()
        st.success(" sucessfully Policy assigned to customer!")

# View Database
with tab4:
    st.subheader("📊 View Tables")

    if st.checkbox("Show Customers"):
        customers = cursor.execute("SELECT * FROM Customer").fetchall()
        st.table(customers)

    if st.checkbox("Show Policies"):
        policies = cursor.execute("SELECT * FROM InsurancePolicy").fetchall()
        st.table(policies)

    if st.checkbox("Show Customer Policies"):
        cpolicies = cursor.execute("SELECT * FROM CustomerPolicy").fetchall()
        st.table(cpolicies)

    if st.checkbox("Show Claims"):
        claims = cursor.execute("SELECT * FROM Claims").fetchall()
        st.table(claims)
