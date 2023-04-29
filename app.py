import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS

from img_gen_v2 import generate_story
from prompt_generation import pipeline


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
                if current_page == 0:
                    user_input = st.session_state.user_input
                    prompt_response = pipeline(user_input, 10)
                    steps = prompt_response.get("steps")
                    init_prompt = prompt_response.get("story")

                    init_img, img_dict = generate_story(init_prompt, steps)

                    st.session_state.pipeline_response = prompt_response
                    st.session_state.init_img = init_img
                    st.session_state.img_dict = img_dict

                current_page += 1

    return current_page


# Main function to display the pages
def get_pipeline_data(page_number):
    pipeline_response = st.session_state.pipeline_response
    text_output = pipeline_response.get("steps")[page_number - 1]
    img_dict = st.session_state.img_dict
    img = img_dict[page_number-1].get("image")

    return {"text_output": text_output, "image_obj": img}


def main():
    st.set_page_config(page_title="Narrative chat", layout="wide")
    st.title("DreamBot")

    # Initialize the current page
    current_page = st.session_state.get('current_page', 0)

    # Display content for each page
    if current_page == 0:
        st.write("Tell me what story you would like me to tell:")
        user_input = st.text_area("")
        st.session_state.user_input = user_input

    else:
        # Retrieve data from random generators
        data = get_pipeline_data(current_page)
        text_output = data.get('text_output', '')
        image = data.get('image_obj', '')

        # Display text output
        st.write(text_output)

        tts = gTTS(text_output)
        tts.save('audio.mp3')
        st.audio('audio.mp3')

        # Display image output
        if image:
            st.image(image, use_column_width=False, width=400)

    # Display page navigation
    current_page = page_navigation(current_page)

    st.write('current_page:', current_page)
    st.session_state.current_page = current_page


if __name__ == "__main__":
    main()
