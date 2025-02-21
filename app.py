import streamlit as st
from auth import authenticate
from orders import place_order, manage_orders, admin_dashboard

def main():
    st.title("Laundry Service Management App")
    
    # User authentication
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = authenticate(username, password)

    if role:
        st.sidebar.success(f"Logged in as {role.capitalize()}")

        if role == "customer":
            place_order(username)
        elif role == "laundryman":
            manage_orders()
        elif role == "admin":
            admin_dashboard()
    else:
        st.sidebar.error("Invalid username or password")

if __name__ == "__main__":
    main()
