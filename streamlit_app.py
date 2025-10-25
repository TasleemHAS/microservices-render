import streamlit as st
import requests
import os
from datetime import datetime

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

# Helper function to display data as table without pandas
def display_users_table(users):
    if not users:
        st.info("No users found")
        return
    
    # Create a simple table using Streamlit's native functions
    st.write("### Users List")
    for user in users:
        with st.expander(f"👤 {user.get('name', 'Unknown')} (ID: {user.get('id', 'N/A')})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Email:** {user.get('email', 'N/A')}")
            with col2:
                st.write(f"**ID:** {user.get('id', 'N/A')}")
            with col3:
                st.write(f"**Created:** {user.get('created_at', 'N/A')}")
    
    st.metric("Total Users", len(users))

def display_orders_table(orders):
    if not orders:
        st.info("No orders found")
        return
    
    # Create a simple table using Streamlit's native functions
    st.write("### Orders List")
    for order in orders:
        with st.expander(f"📦 {order.get('product', 'Unknown')} (ID: {order.get('id', 'N/A')})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Product:** {order.get('product', 'N/A')}")
                st.write(f"**User ID:** {order.get('user_id', 'N/A')}")
                st.write(f"**Status:** {order.get('status', 'N/A')}")
            with col2:
                st.write(f"**Quantity:** {order.get('quantity', 'N/A')}")
                st.write(f"**Amount:** ${order.get('amount', 'N/A')}")
                st.write(f"**Created:** {order.get('created_at', 'N/A')}")
    
    st.metric("Total Orders", len(orders))

# Main tabs
tab1, tab2, tab3 = st.tabs(["Users", "Orders", "Create New"])

with tab1:
    st.header("Users Management")
    users = fetch_users()
    display_users_table(users)
    
    # User actions
    st.subheader("User Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Find User**")
        find_user_id = st.number_input("User ID to find", min_value=1, value=1, key="find_user_id")
        if st.button("Find User", key="find_user_btn"):
            try:
                response = requests.get(f"{USER_SERVICE_URL}/api/users/{int(find_user_id)}", timeout=5)
                if response.status_code == 200:
                    user = response.json()
                    st.success("✅ User found!")
                    st.json(user)
                else:
                    st.error("❌ User not found")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.write("**Delete User**")
        delete_user_id = st.number_input("User ID to delete", min_value=1, value=1, key="delete_user_id")
        if st.button("Delete User", key="delete_user_btn"):
            try:
                response = requests.delete(f"{USER_SERVICE_URL}/api/users/{int(delete_user_id)}", timeout=5)
                if response.status_code == 200:
                    st.success("✅ User deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete user")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("Orders Management")
    orders = fetch_orders()
    display_orders_table(orders)
    
    # Order actions
    st.subheader("Order Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Find Order**")
        find_order_id = st.number_input("Order ID to find", min_value=1, value=1, key="find_order_id")
        if st.button("Find Order", key="find_order_btn"):
            try:
                response = requests.get(f"{ORDER_SERVICE_URL}/api/orders/{int(find_order_id)}", timeout=5)
                if response.status_code == 200:
                    order = response.json()
                    st.success("✅ Order found!")
                    st.json(order)
                else:
                    st.error("❌ Order not found")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.write("**User Orders**")
        user_id_for_orders = st.number_input("User ID", min_value=1, value=1, key="user_orders")
        if st.button("Get User Orders"):
            try:
                response = requests.get(f"{ORDER_SERVICE_URL}/api/orders/user/{int(user_id_for_orders)}", timeout=5)
                if response.status_code == 200:
                    user_orders_data = response.json()
                    user_orders = user_orders_data.get('orders', [])
                    if user_orders:
                        st.success(f"✅ Found {len(user_orders)} orders for user {user_id_for_orders}")
                        display_orders_table(user_orders)
                    else:
                        st.info("No orders found for this user")
                else:
                    st.error("Failed to fetch user orders")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

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
                else:
                    st.error("Please fill in both name and email")
    
    with col2:
        st.subheader("Create Order")
        with st.form("order_form", clear_on_submit=True):
            user_id = st.number_input("User ID", min_value=1, value=1)
            product = st.text_input("Product")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.01)
            status = st.selectbox("Status", ["pending", "completed", "shipped", "cancelled"])
            if st.form_submit_button("Create Order"):
                if product and amount:
                    try:
                        response = requests.post(
                            f"{ORDER_SERVICE_URL}/api/orders",
                            json={
                                "user_id": int(user_id),
                                "product": product,
                                "quantity": int(quantity),
                                "amount": float(amount),
                                "status": status
                            },
                            timeout=5
                        )
                        if response.status_code == 201:
                            st.success("✅ Order created!")
                        else:
                            st.error("Failed to create order")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please fill in all fields")

if st.sidebar.button("Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("Deployed on Render.com")
st.sidebar.info("No pandas dependency - faster deployment!")
