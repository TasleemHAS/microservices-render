import streamlit as st
import datetime
import json

# Initialize session state for data storage
if 'users' not in st.session_state:
    st.session_state.users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": "2024-01-02"}
    ]

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"id": 1, "user_id": 1, "product": "Laptop", "quantity": 1, "amount": 999.99, "status": "completed", "created_at": "2024-01-01"},
        {"id": 2, "user_id": 2, "product": "Mouse", "quantity": 2, "amount": 49.99, "status": "pending", "created_at": "2024-01-02"}
    ]

st.set_page_config(
    page_title="Microservices Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Microservices Dashboard - Pure Streamlit!")
st.success("✅ All services running in single Streamlit app")

# Sidebar
st.sidebar.header("Service Status")
st.sidebar.success("✅ User Service (Integrated)")
st.sidebar.success("✅ Order Service (Integrated)")

# Helper functions
def display_users_table(users):
    if not users:
        st.info("No users found")
        return
    
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
    display_users_table(st.session_state.users)
    
    # User actions
    st.subheader("User Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Find User**")
        find_user_id = st.number_input("User ID to find", min_value=1, value=1, key="find_user_id")
        if st.button("Find User", key="find_user_btn"):
            user = next((u for u in st.session_state.users if u['id'] == find_user_id), None)
            if user:
                st.success("✅ User found!")
                st.json(user)
            else:
                st.error("❌ User not found")
    
    with col2:
        st.write("**Delete User**")
        delete_user_id = st.number_input("User ID to delete", min_value=1, value=1, key="delete_user_id")
        if st.button("Delete User", key="delete_user_btn"):
            st.session_state.users = [u for u in st.session_state.users if u['id'] != delete_user_id]
            st.success("✅ User deleted successfully!")
            st.rerun()

with tab2:
    st.header("Orders Management")
    display_orders_table(st.session_state.orders)
    
    # Order actions
    st.subheader("Order Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Find Order**")
        find_order_id = st.number_input("Order ID to find", min_value=1, value=1, key="find_order_id")
        if st.button("Find Order", key="find_order_btn"):
            order = next((o for o in st.session_state.orders if o['id'] == find_order_id), None)
            if order:
                st.success("✅ Order found!")
                st.json(order)
            else:
                st.error("❌ Order not found")
    
    with col2:
        st.write("**User Orders**")
        user_id_for_orders = st.number_input("User ID", min_value=1, value=1, key="user_orders")
        if st.button("Get User Orders"):
            user_orders = [o for o in st.session_state.orders if o['user_id'] == user_id_for_orders]
            if user_orders:
                st.success(f"✅ Found {len(user_orders)} orders for user {user_id_for_orders}")
                display_orders_table(user_orders)
            else:
                st.info("No orders found for this user")

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
                    new_user = {
                        "id": max([u['id'] for u in st.session_state.users], default=0) + 1,
                        "name": name,
                        "email": email,
                        "created_at": datetime.datetime.now().isoformat()
                    }
                    st.session_state.users.append(new_user)
                    st.success("✅ User created!")
                    st.rerun()
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
                    new_order = {
                        "id": max([o['id'] for o in st.session_state.orders], default=0) + 1,
                        "user_id": int(user_id),
                        "product": product,
                        "quantity": int(quantity),
                        "amount": float(amount),
                        "status": status,
                        "created_at": datetime.datetime.now().isoformat()
                    }
                    st.session_state.orders.append(new_order)
                    st.success("✅ Order created!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

if st.sidebar.button("Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("Deployed on Render.com - Single App Solution")
