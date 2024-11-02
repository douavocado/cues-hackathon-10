# handle user input for check ins and outs, calculate and accumulate points

import streamlit as st
# from utils.database import save_checkin, save_checkout, update_user_points
from components.location_verifier import verify_location
import pandas as pd

def render(library_coords):
    user_name = st.text_input("Enter your name:")
    check_in_button = st.button("Check In")
    check_out_button = st.button("Check Out")

    # Get user's location (mock for now)
    user_coords = (52.2053, 0.1218)  # Replace with actual GPS retrieval logic

    if verify_location(user_coords, library_coords):
        if check_in_button:
            if user_name:
                checkin_data = {
                    "Name": user_name,
                    "Library": "Library Name Here",  # Replace with actual library name
                    "Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Checked In"
                }
                # save_checkin(checkin_data)
                # update_user_points(user_name, 1)  # Update points
                st.success(f"Checked in to the library at {checkin_data['Time']}. You earned 1 point!")
            else:
                st.error("Please enter your name to check in.")
        
        elif check_out_button:
            if user_name:
                checkout_data = {
                    "Name": user_name,
                    "Library": "Library Name Here",  # Replace with actual library name
                    "Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Checked Out"
                }
                # save_checkout(checkout_data)
                st.success(f"Checked out from the library at {checkout_data['Time']}.")
            else:
                st.error("Please enter your name to check out.")
    else:
        st.warning("You are too far from the library to check in or out.")
