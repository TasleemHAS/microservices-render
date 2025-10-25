import streamlit as st
import requests
import pandas as pd
import os

# Configuration - for Docker deployment
USER_SERVICE_URL = "http://localhost:5001"
ORDER_SERVICE_URL = "http://localhost:5002"

st.set_page_config(
    page_title="Microservices Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Microservices Dashboard - Deployed!")
st.markdown("**Successfully deployed on Render.com** 🚀")

# Add a small delay for services to start
import time

def fetch_users():
    try:
        response = requests.get(f"{USER_SERVICE_URL}/api/users", timeout=10)
        if response.status_code == 200:
            return response.json().get('users', [])
        return []
    except:
        return []

def fetch_orders():
    try:
        response = requests.get(f"{ORDER_SERVICE_URL}/api/orders", timeout=10)
        if response.status_code == 200:
            return response.json().get('orders', [])
        return []
    except:
        return []

# Sidebar
st.sidebar.header("Service Status")
st.sidebar.info("All services running in single container")

# Check services with retry
def check_service(url, service_name):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            st.sidebar.success(f"✅ {service_name}")
            return True
        else:
            st.sidebar.error(f"❌ {service_name}")
            return False
    except:
        st.sidebar.error(f"❌ {service_name}")
        return False

# Wait a bit for services to start
time.sleep(2)

check_service(f"{USER_SERVICE_URL}/health", "User Service")
check_service(f"{ORDER_SERVICE_URL}/health", "Order Service")

# Main tabs
tab1, tab2, tab3 = st.tabs(["Users", "Orders", "Create New"])

with tab1:
    st.header("Users")
    users = fetch_users()
    if users:
        st.dataframe(pd.DataFrame(users), use_container_width=True)
        st.metric("Total Users", len(users))
    else:
        st.info("No users found or services starting...")

with tab2:
    st.header("Orders")
    orders = fetch_orders()
    if orders:
        st.dataframe(pd.DataFrame(orders), use_container_width=True)
        st.metric("Total Orders", len(orders))
    else:
        st.info("No orders found or services starting...")

with tab3:
    st.header("Create New")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Create User")
        with st.form("user_form", clear_on_submit=True):
            name = st.text_input("Name")
            email = st.text_input("Email")
            if st.form_submit_button("Create User"):
                if name and email:
                    try:
                        response = requests.post(
                            f"{USER_SERVICE_URL}/api/users",
                            json={"name": name, "email": email},
                            timeout=5
                        )
                        if response.status_code == 201:
                            st.success("✅ User created!")
                        else:
                            st.error("Failed to create user")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("Create Order")
        with st.form("order_form", clear_on_submit=True):
            user_id = st.number_input("User ID", min_value=1, value=1)
            product = st.text_input("Product")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.01)
            if st.form_submit_button("Create Order"):
                if product and amount:
                    try:
                        response = requests.post(
                            f"{ORDER_SERVICE_URL}/api/orders",
                            json={
                                "user_id": int(user_id),
                                "product": product,
                                "quantity": int(quantity),
                                "amount": float(amount)
                            },
                            timeout=5
                        )
                        if response.status_code == 201:
                            st.success("✅ Order created!")
                        else:
                            st.error("Failed to create order")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

if st.sidebar.button("Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("Deployed on Render.com")