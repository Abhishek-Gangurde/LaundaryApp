import streamlit as st
from datetime import datetime
from database import get_db_connection
from email_service import send_email
from auth import users

def place_order(username):
    conn = get_db_connection()
    c = conn.cursor()
    st.header("Place a New Laundry Order")
    service = st.selectbox("Select Service", ["Wash", "Dry", "Iron", "Full Service"])
    pickup_date = st.date_input("Select Pickup Date")
    pickup_time = st.time_input("Select Pickup Time")
    notes = st.text_area("Special Instructions")

    if st.button("Place Order"):
        pickup_datetime = f"{pickup_date} {pickup_time}"
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO orders (customer, service, status, pickup_datetime, notes, order_time) VALUES (?, ?, ?, ?, ?, ?)',
                  (username, service, "Pending", pickup_datetime, notes, order_time))
        conn.commit()
        st.success("Order placed successfully!")
        
        customer_email = users[username].get("email")
        if customer_email:
            subject = "Order Confirmation"
            body = f"Dear {username},\n\nYour order for '{service}' has been placed successfully.\n\nDetails:\n- Pickup Date & Time: {pickup_datetime}\n- Notes: {notes}\n\nThank you for using our service!"
            send_email(customer_email, subject, body)

    st.subheader("Your Current Orders")
    c.execute("SELECT * FROM orders WHERE customer = ?", (username,))
    orders = c.fetchall()
    for order in orders:
        with st.expander(f"Order #{order[0]} - {order[2]} (Status: {order[3]})"):
            st.write(f"Pickup Date & Time: {order[4]}")
            st.write(f"Notes: {order[5]}")
            st.write(f"Order Time: {order[6]}")


def manage_orders():
    conn = get_db_connection()
    c = conn.cursor()
    st.header("Manage Orders")
    filter_status = st.selectbox("Filter Orders by Status", ["All", "Pending", "Picked Up", "In Process", "Completed"])
    c.execute("SELECT * FROM orders" if filter_status == "All" else "SELECT * FROM orders WHERE status = ?", (filter_status,))
    orders = c.fetchall()
    for order in orders:
        with st.expander(f"Order #{order[0]} - {order[1]}"):
            st.write(f"Service: {order[2]}")
            st.write(f"Status: {order[3]}")
            st.write(f"Pickup Date & Time: {order[4]}")
            st.write(f"Notes: {order[5]}")
            new_status = st.selectbox(f"Update Status for Order #{order[0]}", ["Pending", "Picked Up", "In Process", "Completed"], index=["Pending", "Picked Up", "In Process", "Completed"].index(order[3]))
            if st.button(f"Update Status for Order #{order[0]}"):
                c.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order[0]))
                conn.commit()
                st.success(f"Order #{order[0]} status updated to {new_status}")
