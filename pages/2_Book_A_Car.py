import streamlit as st
import datetime
from uuid import uuid4
from DatabaseManager import DatabaseManager

st.set_page_config(page_title="Create Booking", layout="wide")
st.title("Book a Car")
st.sidebar.header("Book a Car")
st.sidebar.write("Hello")

db_manager = DatabaseManager(
    db_user="root",
    db_password="648374@Mysql",
    host="localhost",
    database="car_rental",
)


@st.cache_data
def cached_customer_details(username):
    result = db_manager.get_customer_details(username)  # TODO Implement this method
    return result


@st.cache_data
def cached_rent_details(vehicle_class):
    result = db_manager.get_rental_details(vehicle_class)  # TODO Implement this method
    return result


@st.cache_data
def cached_discount(username, discount_id):
    result = db_manager.verify_and_get_discount(
        username, discount_id
    )  # TODO Implement this method
    return result


def create_booking():
    user_inputs = {}
    with st.container(border=True):
        st.subheader("Vehicle Details")
        user_inputs["VEH_CLASS_TYPE"] = st.selectbox(
            "**Select Vehicle type**",
            options=("Hatchback", "Sedan", "SUV", "Premium"),
        )
        user_inputs["VEH_VIN"] = st.text_input("**Enter Vehicle VIN**")
        col3, col4 = st.columns(2)
        with col3:
            user_inputs["PICKUP_DATE"] = st.date_input(
                "**Pick-up Date**", min_value=datetime.datetime.today()
            )
        with col4:
            user_inputs["PLANNED_DROPOFF_DATE"] = st.date_input(
                "**Drop-off Date**", min_value=datetime.datetime.today()
            )
        if user_inputs["PLANNED_DROPOFF_DATE"] < user_inputs["PICKUP_DATE"]:
            st.warning("Wrong drop-off and pick-up date entered!")

        with st.expander("**Enter Pick-up Address**"):
            pickup_addr = {}
            pickup_addr["LOC_ADDR_STREET"] = st.text_input(
                "Street details", key=uuid4()
            )
            pickup_addr["LOC_ADDR_CITY"] = st.text_input("City", key=uuid4())
            pickup_addr["LOC_ADDR_ZIPCODE"] = st.text_input("Zipcode", key=uuid4())
            pickup_addr["LOC_ADDR_STATE"] = st.text_input("State", key=uuid4())
        with st.expander("**Enter Drop-off Address**"):
            drop_addr = {}
            drop_addr["LOC_ADDR_STREET"] = st.text_input("Street details", key=uuid4())
            drop_addr["LOC_ADDR_CITY"] = st.text_input("City", key=uuid4())
            drop_addr["LOC_ADDR_ZIPCODE"] = st.text_input("Zipcode", key=uuid4())
            drop_addr["LOC_ADDR_STATE"] = st.text_input("State", key=uuid4())

        user_inputs["pickup_addr"] = pickup_addr
        user_inputs["drop_addr"] = drop_addr

        user_inputs["DISCOUNT_ID"] = st.text_input("**Enter Discount Coupon**")
        book_flag = st.button("**Book now**")

    if book_flag:
        discount = cached_discount(
            st.session_state["username"], user_inputs["DISCOUNT_ID"]
        )
        if discount == 0:
            st.warning("Invalid Discount Coupon!")
            user_inputs["DISCOUNT_ID"] = None

        user_details = cached_customer_details(st.session_state["username"])
        rent_details = cached_rent_details(user_inputs["VEH_CLASS_TYPE"])

        n_days = (user_inputs["PLANNED_DROPOFF_DATE"] - user_inputs["PICKUP_DATE"]).days
        discount_amt = (discount / 100) * (rent_details["VEH_RENTAL_RATE"] * n_days)
        user_inputs["AMOUNT"] = (
            rent_details["VEH_RENTAL_RATE"] * n_days
        ) - discount_amt
        with st.container(border=True):
            st.subheader("Verify Details and Make Payment")
            col7, col8 = st.columns([0.5, 0.5])
            with col7:
                st.write(f"**Customer Type:** {user_details['CUST_TYPE']}")

                if user_details["CUST_TYPE"] == "I":
                    st.write(
                        f"**Customer Name:** {user_details['FNAME']}_{user_details['LNAME']}"
                    )
                    st.write(f"**License ID:** {user_details['DRIVERS_LICENCE_NO']}")
                else:
                    st.write(f"**Employee ID:** {user_details['EMP_ID']}")
                    st.write(f"**Company Name:** {user_details['COMPANY_NAME']}")

                st.write(f"**Vehicle Type:** {user_inputs['VEH_CLASS_TYPE']}")
                st.write(f"**Pick-up Date:** {user_inputs['PICKUP_DATE']}")
                st.write(f"**Drop-off Date** {user_inputs['PLANNED_DROPOFF_DATE']}")
                st.write(f"**No. of Days:** {n_days}")
                st.write(f"**Base Charges per day:** {rent_details['VEH_RENTAL_RATE']}")
                st.write(f"**Discount Amount:** {discount_amt}")
                st.write("---")
                st.write(f"**Total Amount:** {user_inputs['AMOUNT']}")

            with col8:
                st.write("**Enter Payment Details**")
                user_inputs["PAYMENT_CARD_NO"] = st.text_input("Card Number")
                pay_flag = st.button("Pay Now")
                if pay_flag:
                    booking_id = db_manager.update_booking(
                        user_inputs
                    )  # TODO: Implement this method as it accepts dictionary of inputs
                    st.success(
                        f"Your Booking is Successful! Booking reference ID - {booking_id}"
                    )


if __name__ == "__main__":
    create_booking()
