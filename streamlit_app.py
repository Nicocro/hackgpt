import streamlit as st

# Function to create the page navigation
def page_navigation(current_page):
    col1, col2, col3 = st.columns(3)

    if current_page > 1:
        with col1:
            if st.button('<< Previous'):
                current_page -= 1

    with col2:
        st.write(f'Page {current_page} of 10')

    if current_page < 10:
        with col3:
            if st.button('Next >>'):
                current_page += 1

    return current_page

# Main function to display the pages
def main():
    st.set_page_config(page_title="Streamlit 10 Page App", layout="wide")
    st.title("Streamlit 10 Page App")

    with st.form("my_form"):
        st.write("Tell me a story")
        st.text_area("story")
        submitted = st.form_submit_button("Submit")

    if submitted:
        current_page = st.session_state.get('current_page', 1)

        data = get_data()

        st.write(data[current_page][0])
        st.image(data[current_page][1])

        current_page = page_navigation(current_page)
        st.session_state.current_page = current_page



def get_data():
    data = list()
    for i in range(10):
        data.append((f'This is prompt {i}', f'https://picsum.photos/200/300?random={i}'))

    return data

if __name__ == "__main__":
    main()

