import streamlit as st
from components.library_selector import LibrarySelector
from components.checkin_handler import CheckInHandler


def main():
    # Set the title of the app
    st.title("Cambridge Library Monopoly")
    st.header("Select a Library and Check In/Out")

    library_selector = LibrarySelector()
    checkin_handler = CheckInHandler()
    library_name = library_selector.render()

    if library_name:
        checkin_handler.render(library_name)

if __name__ == "__main__":
    main()
