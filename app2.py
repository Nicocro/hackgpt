import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import json

# Function to get random data
def get_random_data(page_number, user_input=None):
    # Get random image URL
    image_url = f"https://picsum.photos/800/600?random={page_number}"

    # Get random text
    text_api_url = "https://baconipsum.com/api/?type=all-meat&sentences=2&format=json"
    response = requests.get(text_api_url)
    text_output = json.loads(response.text)[0]

    return {"text_output": text_output, "image_url": image_url}

# Function to create the page navigation
def page_navigation(current_page):
    col1, col2, col3 = st.columns(3)

    if current_page > 0:
        with col1:
            if st.button('<< Previous'):
                current_page -= 1

    with col2:
        st.write(f'Step {current_page} of 10')

    if current_page < 10:
        with col3:
            if st.button('Next >>'):
                current_page += 1

    return current_page

# Main function to display the pages
def main():
    st.set_page_config(page_title="Narrative chat", layout="wide")
    st.title("Narrative Chat")

    # Initialize the current page
    current_page = st.session_state.get('current_page', 0)

    # Display content for each page
    if current_page == 0:
        st.header("Narrative Chat")
        st.write("Please enter a storyline:")
        user_input = st.text_area("")
        st.session_state.user_input = user_input

    else:
        # Retrieve data from random generators
        data = get_random_data(current_page, st.session_state.user_input)
        text_output = data.get('text_output', '')
        image_url = data.get('image_url', '')

        # Display text output
        st.header(f"Step {current_page}")
        st.write(text_output)

        # Display image output
        if image_url:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"Image for Page {current_page}", use_column_width=True)

    # Display page navigation
    current_page = page_navigation(current_page)

    st.write('current_page:', current_page)
    st.session_state.current_page = current_page

if __name__ == "__main__":
    main()
