import streamlit as st
import datetime
from uuid import uuid4

st.set_page_config(page_title="Create Booking", layout="wide")
st.title("Book a Car")
st.sidebar.header("Book a Car")
st.sidebar.write("Hello")


def create_booking():
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Vehicle Details")
                vehicle_type = st.selectbox(
                    "Select Vehicle type",
                    options=("Hatchback", "Sedan", "SUV", "Premium"),
                )
                col3, col4 = st.columns(2)
                with col3:
                    checkin = st.date_input(
                        "Pick-up Date", min_value=datetime.datetime.today()
                    )
                with col4:
                    checkout = st.date_input(
                        "Drop-off Date", min_value=datetime.datetime.today()
                    )
                with st.expander("**Enter Pick-up Address**"):
                    pick_street = st.text_input("Street details", key=uuid4())
                    pick_city = st.text_input("City", key=uuid4())
                    pick_zipcode = st.text_input("Zipcode", key=uuid4())
                    pick_state = st.text_input("State", key=uuid4())
                with st.expander("**Enter Drop-off Address**"):
                    drop_street = st.text_input("Street details", key=uuid4())
                    drop_city = st.text_input("City", key=uuid4())
                    drop_zipcode = st.text_input("Zipcode", key=uuid4())
                    drop_state = st.text_input("State", key=uuid4())
        with col2:
            with st.container(border=True):
                st.subheader("Customer Details")
                customer_type = st.selectbox(
                    "Select Customer type", options=("Individual", "Corporate")
                )
                if customer_type == "Corporate":
                    with st.container():
                        emp_id = st.text_input("Employee ID")
                        corp_id = st.text_input("Corporate ID")

                customer_name = st.text_input("Full Name")
                customer_age = int(st.number_input("Age", step=1))
                licene = st.text_input("License ID")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email ID")

                with st.expander("**Enter Address**"):
                    street = st.text_input("Street details", key=uuid4())
                    city = st.text_input("City", key=uuid4())
                    zipcode = st.text_input("Zipcode", key=uuid4())
                    state = st.text_input("State", key=uuid4())

        book_flag = st.button("Book now")

    if book_flag:
        if checkout >= checkin:
            with st.container(border=True):
                st.subheader("Verify Details and Make Payment")
                col5, col6 = st.columns([0.5, 0.5])
                with col5:
                    st.write("**Customer Name:** ", customer_name)
                    st.write("**Customer Type:** ", customer_type)
                    st.write("**Vehicle Type:** ", vehicle_type)
                    st.write("**Pick-up Date:** ", checkin)
                    st.write("**Drop-off Date** ", checkout)
                    st.write("**No. of Days:** ", (checkout - checkin).days)
                    # TODO: Generate invoice by fetching charges from DB
                    st.write("**Base Charges:** ")
                    st.write("**Discount Amount:** ")
                    st.write("---")
                    st.write("**Total Amount:** ")

                with col6:
                    st.write("**Enter Payment Details**")
                    card_name = st.text_input("Name on Card")
                    card_num = st.text_input("Card Number")
                    pay_flag = st.button("Pay Now")
                    if pay_flag:
                        pass
                    # TODO: Update DB
        else:
            st.warning("Wrong drop-off and pick-up date entered!")


if __name__ == "__main__":
    create_booking()
