import streamlit as st
from streamlit_option_menu import option_menu
from DatabaseManager import DatabaseManager, make_hashes, check_hashes
import time

st.set_page_config(page_title="Profile")
st.title("Customer Details")
st.sidebar.header("Customer Details")
st.sidebar.write("Hello")

customer_type_map = {"C": "Corporate", "I": "Individual"}

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
def cached_customer_bookings(username):
    result = db_manager.get_customer_bookings(
        username
    )  # TODO Implement this method to return pandas DF
    return result


def profile():
    username = st.text_input("Enter Username")
    result = cached_customer_details(username)
    selected = option_menu(
        "",
        ["User Home", "Change Password", "View Bookings"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
    )
    if selected == "User Home":
        with st.container(border=True):
            st.write("**Customer Type**", customer_type_map[result["CUST_TYPE"]])

            if result["CUST_TYPE"] == "I":
                st.write("**Full Name**", f"{result['FNAME']} {result['LNAME']}")
                st.write("**License ID**", result["DRIVERS_LICENCE_NO"])
                st.write("**Insurance Company Name**", result["INSURANCE_CMP_NAME"])
                st.write("**Insurance Policy Number**", result["INSURANCE_POLICY_NO"])
            else:
                st.write("**Employee ID**", result["EMP_ID"])
                st.write("**Company Name**", result["COMPANY_NAME"])
                st.write("**Company Registration Number**", result["COMPANY_REGN_NO"])

            st.write("**Phone Number**", result["CUST_PHONE_NO"])
            st.write("**Email ID**", result["CUST_EMAIL"])
            st.write("**Address**")
            with st.container(border=True):
                st.write("Street details", result["CUST_ADDR_STREET"])
                st.write("City", result["CUST_ADDR_CITY"])
                st.write("Zipcode", result["CUST_ADDR_ZIPCODE"])
                st.write("State", result["CUST_ADDR_STATE"])

    elif selected == "Change Password":
        with st.container(border=True):
            curr_password = st.text_input("Enter Current Password", type="password")
            new_password = st.text_input("Enter New Password", type="password")
            new_password_2 = st.text_input("Re-enter New Password", type="password")
            if new_password:
                if new_password == curr_password:
                    st.write("New password cannot be same as Current password!")
                if new_password != new_password_2:
                    st.write("Password do not match!")

        pswd_flag = st.button("Change Password")
        if pswd_flag:
            result = db_manager.login_user(username, make_hashes(curr_password))
            if result:
                hashed_pswd = make_hashes(new_password)
                db_manager.update_userdata(username, hashed_pswd)
                st.success("Successfully Changed Password!")
            else:
                st.warning("Invalid Credentials!")
    else:
        with st.container(border=True):
            st.subheader("Your Bookings")
            result = cached_customer_bookings(username)
            if result:
                st.dataframe(result)
            else:
                st.info("You don't have any previous bookings!")


if __name__ == "__main__":
    profile()
