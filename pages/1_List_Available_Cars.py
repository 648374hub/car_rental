import os
import random
from uuid import uuid4
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Cars List", layout="wide")
st.title("Available Cars")
st.sidebar.header("Available Cars")
st.sidebar.write("Hello")

images = os.listdir("images")


def list_cars():
    st.write("---")
    for idx, image_path in enumerate(images):
        with st.container():
            col1, col2, col3 = st.columns([0.5, 1, 0.3])
            # TODO: Fetch details from DB
            with col1:
                image1 = Image.open(f"images/{image_path}")
                st.image(image1)
            with col2:
                st.write(f"Make: ")
                st.write(f"Model: ")
                st.write(f"Type: ")
                st.write(f"Daily Odometer Limit: ")
                st.write(f"Rental Rate: ")
                st.write(f"Over Mileage Fees: ")
                st.write(f"Registration Year: ")
            with col3:
                st.write(f"Status : {random.choice(['Available','Unavailable'])}")
        st.write("---")


if __name__ == "__main__":
    list_cars()
