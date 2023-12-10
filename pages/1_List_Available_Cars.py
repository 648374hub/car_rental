import os
import random
from uuid import uuid4
import streamlit as st
from PIL import Image
from DatabaseManager import DatabaseManager

st.set_page_config(page_title="Cars List", layout="wide")
st.title("Available Cars")
st.sidebar.header("Available Cars")

images = os.listdir("images")

db_manager = DatabaseManager(
    db_user="root",
    db_password="648374@Mysql",
    host="localhost",
    database="car_rental",
)


@st.cache_data
def cached_vehicle_details(limit):
    result = db_manager.list_avail_cars(limit)
    return result


def list_cars():
    st.sidebar.write(f"Hello {st.session_state.username}")

    st.write("---")
    car_details = cached_vehicle_details(len(images))  # list of records
    for details_obj, image_path in zip(car_details, images):
        with st.container():
            col1, col2, col3 = st.columns([0.5, 1, 0.3])
            with col1:
                image1 = Image.open(f"images/{image_path}")
                st.image(image1)
            with col2:
                st.write("Vehicle VIN: ", details_obj["VEH_VIN"])
                st.write("Make: ", details_obj["VEH_MAKE"])
                st.write("Model: ", details_obj["VEH_MODEL"])
                st.write("Type: ", details_obj["VEH_CLASS_TYPE"])
                st.write("Rental Rate: ", details_obj["VEH_RENTAL_RATE"])
                st.write("Over Mileage Fees: ", details_obj["VEH_OVER_MILEAGE_FEES"])
                st.write("Registration Year: ", details_obj["VEH_YEAR"])
            with col3:
                st.write(f"Status : {random.choice(['Available','Unavailable'])}")
        st.write("---")


if __name__ == "__main__":
    try:
        list_cars()
    except AttributeError as e:
        st.warning("Please LogIn to access this page")
