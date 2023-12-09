import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from uuid import uuid4
from DatabaseManager import DatabaseManager, make_hashes, check_hashes
import time

st.set_page_config(page_title="SignUp")
st.title("Login and Registration")
st.sidebar.header("Login and Registration")
st.sidebar.write("Hello")

db_manager = DatabaseManager(
    db_user="root",
    db_password="648374@Mysql",
    host="localhost",
    database="car_rental",
)


def sign_up():
    selected = option_menu(
        "",
        ["Login", "Register"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
    )

    if selected == "Login":
        with st.container(border=True):
            username = st.text_input("**Enter Username**", key=uuid4())
            password = st.text_input("**Enter Password**", key=uuid4())

            login = st.button("**Login**")
            if login:
                # hashed_pswd = make_hashes(password)
                # result = db_manager.login_user(username, hashed_pswd)
                # if result:
                #     st.success("Logged In as {} !".format(username))
                #     time.sleep(2)
                #     switch_page("List Available Cars")
                # else:
                #     st.warning("Invalid Credentials!")
                pass
    else:
        with st.container(border=True):
            st.subheader("Enter Customer Details")
            customer_type = option_menu(
                "Select Customer Type",
                ["Individual", "Corporate"],
                menu_icon="cast",
                default_index=1,
                orientation="horizontal",
            )
            if customer_type == "Corporate":
                with st.container():
                    corp_emp_id = st.text_input("**Employee ID**")
                    corp_comp_name = st.text_input("**Company Name**")
                    corp_regd_num = st.text_input("**Company Registration Number**")
            else:
                with st.container():
                    indi_license = st.text_input("**Drivers License ID**")
                    indi_insr_comp = st.text_input("**Insurance Company Name**")
                    indi_insr_pol_num = st.text_input("**Insurance Policy Number**")
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("**First Name**")
                    with col2:
                        last_name = st.text_input("**Last Name**")

            phone = st.text_input("**Phone Number**")
            email = st.text_input("**Email ID**")
            username_flag = st.checkbox("Use Email-id as Username")
            if username_flag:
                username = email
            else:
                username = st.text_input("**Enter Username**", key=uuid4())

            with st.expander("Enter Address", expanded=True):
                street = st.text_input("**Street details**")
                city = st.text_input("**City**")
                zipcode = st.text_input("**Zipcode**")
                state = st.text_input("**State**")

            password = st.text_input("**Enter Password**", key=uuid4())
            password_2 = st.text_input("**Confirm Password**")

            if password != password_2:
                st.warning("Passwords do not match!")

            register = st.button("**Register**")
            if register:
                # if customer_type == "Corporate":
                #     db_manager.add_corporate_user(
                #         username,
                #         make_hashes(password),
                #         corp_emp_id,
                #         corp_comp_name,
                #         corp_regd_num,
                #         phone,
                #         email,
                #         street,
                #         city,
                #         zipcode,
                #         state,
                #     )
                # else:
                #     db_manager.add_individual_user(
                #         username,
                #         make_hashes(password),
                #         indi_license,
                #         indi_insr_comp,
                #         indi_insr_pol_num,
                #         first_name,
                #         last_name,
                #         phone,
                #         email,
                #         street,
                #         city,
                #         zipcode,
                #         state,
                #     )
                st.success("You have successfully created an Account!")
                st.info("Go to Login Menu to login")


if __name__ == "__main__":
    sign_up()
