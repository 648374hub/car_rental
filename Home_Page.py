import streamlit as st

st.set_page_config(page_title="WOW Car Rental Service", layout="wide")


def main():
    st.write("# Welcome to WOW Car Rental Service! 👋")

    page_bg_img = """
        <style>
        .stApp {
            background-image: url("https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_13/2798361/190325-rental-cars-cs-229p.jpg");
            background-size: cover;
        }
        </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
