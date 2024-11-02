# handle user input for check ins and outs, calculate and accumulate points

import streamlit as st
from components.location_verifier import verify_location
import pandas as pd
import time
import datetime

class CheckInHandler:
    def __init__(self):
        if 'checked_in' not in st.session_state:
            st.session_state.checked_in = False
        return
    
    def render(self, library_name):
        check_in_button = st.button("Check In")
        check_out_button = st.button("Check Out")

        # Get user's location (mock for now)
        user_coords = (52.2053, 0.1218)  # Replace with actual GPS retrieval logic

        if not verify_location(user_coords, library_name):
            st.warning("You are too far from the library to check in or out.")
            return

        if check_in_button:
            print(st.session_state.checked_in)
            if st.session_state.checked_in == True:
                st.warning("You have already checked in. You need to check out first.")
                return

            st.session_state.start_time = time.time()
            st.session_state.dest_name = library_name
            st.session_state.checked_in = True
            st.success(f'Checked in to {library_name} at {time.ctime(st.session_state.start_time)}. You earned 1 point!')

        elif check_out_button:
            # add error handling if check_in_time is not initialised
            if st.session_state.checked_in == False:
                st.warning("You need to check in before checking out.")
                return

            elif library_name != st.session_state.dest_name:
                st.warning("You have selected a different library. Check out of your previous library before checking in to another one.")
                return

            check_out_data = {
                "user_id": 0,
                "dest_name": library_name,
                "start_time": st.session_state.start_time,
                "end_time": time.time()
            }
            # save_checkout(checkout_data)
            st.success(f"Checked out from {library_name} at {time.ctime(check_out_data['end_time'])}. You were there since {time.ctime(check_out_data['start_time'])}")
            st.session_state.checked_in = False
                    
                