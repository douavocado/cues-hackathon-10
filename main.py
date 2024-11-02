import streamlit as st
from components.library_selector import LibrarySelector
from components.location_verifier import verify_location
from components.checkin_handler import render as checkin_handler

st.set_option('client.showErrorDetails', False)

def main():
    # Set the title of the app
    st.title("Cambridge Library Monopoly")
    st.header("Select a Library and Check In/Out")

    library_selector = LibrarySelector()
    library_name = library_selector.render() # This should return the coordinates of the selected library
    #print(library_name)
    #st.write(library_name)
    try:
        location_verify = verify_location(library_name)
        if location_verify:
            st.success('Location successfully verified.')
        else:
            st.warning('Location verification unsuccessful.')
    except:
        st.error('An error has occured.')
        #pass#raise Exception("Please press the location button to verify.")
    
    if library_name:
        # If a library is selected, render the check-in/out handler
        checkin_handler(library_name)

    if library_name:
        checkin_handler.render(library_name)

if __name__ == "__main__":
    main()
