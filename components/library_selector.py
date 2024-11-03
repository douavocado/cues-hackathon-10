# handle library selection and recommend new libraries?

import streamlit as st
from components.library_coordinates import department_libraries_coordinates


class LibrarySelector:
    def __init__(self):
        pass

    def render(self):
        library_name = st.selectbox("Select a library:", list(department_libraries_coordinates.keys()))#
        return library_name