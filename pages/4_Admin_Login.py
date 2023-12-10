import streamlit as st
from streamlit_option_menu import option_menu
from DatabaseManager import DatabaseManager, make_hashes, check_hashes
import time
import datetime
from uuid import uuid4

st.set_page_config(page_title="Admin")
st.title("Admin Login")
st.sidebar.header("Admin Login")
st.sidebar.write("Hello Admin")

customer_type_map = {"Corporate": "C", "Individual": "I"}

db_manager = DatabaseManager(
    db_user="root",
    db_password="648374@Mysql",
    host="localhost",
    database="car_rental",
)


@st.cache_data
def cached_booking_details(invoice_id):
    result = db_manager.get_booking_details(invoice_id)

    return result


def login_admin():
    with st.container(border=True):
        username = st.text_input("**Enter Username**")
        password = st.text_input("**Enter Password**")

        login = st.button("**Login**")
        if login:
            hashed_pswd = make_hashes(password)
            result = db_manager.login_admin(username, hashed_pswd)
            if "admin" in result:
                st.success("Logged In as {} !".format(username))
                return True
            else:
                st.warning("Invalid Credentials!")
                return False


def checkout(invoice_id):
    result = cached_booking_details(invoice_id)

    for key, value in result.items():
        st.write(f"**{key}:** {value}")

    end_odometer = st.number_input("**End Odometer Reading**")
    actual_dropoff = st.date_input("**Actual Drop-off Date**")
    odometer_flag = False
    if actual_dropoff > result["planned_dropoff_date"]:
        n_days = (actual_dropoff - result["pickup_date"]).days
        daily_miles = (end_odometer - result["start_odometer"]) / n_days
        if daily_miles > result["daily_odometer_limit"]:
            odometer_flag = True
        if odometer_flag:
            total = ((result["veh_rental_rate"] * n_days)) + (
                result["veh_over_mileage_fees"] * n_days
            )
            balance = total - result["inv_amount"]
        else:
            total = result["veh_rental_rate"] * n_days
            balance = total - result["inv_amount"]

        st.write("**Amount Paid: **", result["inv_amount"])
        st.write("**Is Daily Odometer Limit Exceeded: **", odometer_flag)
        st.write("**Total Amount: **", total)
        st.write("**Balance Amount: **", balance)

        update = st.button("**Update Booking**")
        if update:
            db_manager.update_drop_off(
                invoice_id, end_odometer, actual_dropoff, odometer_flag, total
            )

    st.success("**Thankyou for Booking with us!**")


def main():
    option = option_menu(
        "",
        ["Check Out", "Register New Car", "Activate Coupon", "Change Fare"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
    )

    if option == "Check Out":
        invoice_id = st.number_input("**Enter Invoice ID**")
        with st.container(border=True):
            checkout(invoice_id)
    elif option == "Activate Coupon":
        with st.container(border=True):
            discount_type = st.selectbox(
                "**Select Discount Type**", options=["Individual", "Corporate"]
            )
            if discount_type == "Individual":
                discount_id = st.number_input("**Enter Discount ID**")
                percent = st.number_input("**Enter Discount Percent**")
                from_date = st.date_input(
                    "**Valid From**", min_value=datetime.datetime.today()
                )
                to_date = st.date_input(
                    "**Valid Upto**", min_value=datetime.datetime.today()
                )
                update = st.button("**Activate**")
                if update:
                    db_manager.add_discount_ind(
                        discount_id, percent, from_date, to_date
                    )
                    st.success("Successfully added Discount Coupon!")
            else:
                discount_id = st.number_input("**Enter Discount ID**")
                percent = st.number_input("**Enter Discount Percent**")
                company = st.text_input("**Enter Affiliated Company**")
                update = st.button("**Activate**")
                if update:
                    db_manager.add_discount_corp(discount_id, percent, company)
                    st.success("Successfully added Discount Coupon!")

    elif option == "Change Fare":
        admin_inputs = {}
        with st.container(border=True):
            admin_inputs["VEH_CLASS_TYPE"] = st.selectbox(
                "**Select Vehicle type**",
                options=("Hatchback", "Sedan", "SUV", "Premium"),
            )
            admin_inputs["VEH_RENTAL_RATE"] = st.number_input("**New Rental Rate**")
            admin_inputs["VEH_OVER_MILEAGE_FEES"] = st.number_input(
                "**New Over Mileage Fees**"
            )
            update = st.button("**Update Fare**")
            if update:
                db_manager.update_rent(
                    admin_inputs["VEH_CLASS_TYPE"], admin_inputs["VEH_RENTAL_RATE"]
                )
                db_manager.update_over_mil(
                    admin_inputs["VEH_CLASS_TYPE"],
                    admin_inputs["VEH_OVER_MILEAGE_FEES"],
                )

    else:
        admin_inputs = {}
        with st.container(border=True):
            admin_inputs["VEH_MAKE"] = st.text_input("**Make**")
            admin_inputs["VEH_MODEL"] = st.text_input("**Model**")
            admin_inputs["VEH_YEAR"] = st.number_input("**Year of Registration**")
            admin_inputs["VEH_LICENSE_PLATE_NO"] = st.text_input(
                "**License Plate Number**"
            )
            admin_inputs["VEH_CLASS_TYPE"] = st.selectbox(
                "**Select Vehicle type**",
                options=("Hatchback", "Sedan", "SUV", "Premium"),
            )
            with st.expander("**Enter Address**"):
                vehicle_addr = {}
                vehicle_addr["LOC_ADDR_STREET"] = st.text_input(
                    "Street details", key=uuid4()
                )
                vehicle_addr["LOC_ADDR_CITY"] = st.text_input("City", key=uuid4())
                vehicle_addr["LOC_ADDR_ZIPCODE"] = st.text_input("Zipcode", key=uuid4())
                vehicle_addr["LOC_ADDR_STATE"] = st.text_input("State", key=uuid4())
                vehicle_addr["LOC_ADDR_COUNTRY"] = st.text_input("Country", key=uuid4())

            admin_inputs["vehicle_address"] = vehicle_addr

            _ = st.file_uploader("**Upload Image**")

            update = st.button("**Register Vehicle**")
            if update:
                db_manager.register_car(admin_inputs)


if __name__ == "__main__":
    login = login_admin()
    if login:
        main()
