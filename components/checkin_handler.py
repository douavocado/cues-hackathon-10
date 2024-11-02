# handle user input for check ins and outs, calculate and accumulate points

import streamlit as st
from components.location_verifier import verify_location
import time
import datetime

class CheckInHandler:
    def __init__(self):
        self.checked_in = False
        return
    
    def render(self, library_name):
        check_in_button = st.button("Check In")
        check_out_button = st.button("Check Out")

        if verify_location(library_name):
            st.success('Location successfully verified.')
        else:
            st.warning("You are too far from the library to check in or out.")
            return

        if check_in_button:
            if self.checked_in == True:
                st.warning("You have already checked in. You need to check out first.")
                return

            self.start_time = time.time()
            self.dest_name = library_name
            self.checked_in = True
            st.success(f'Checked in to {library_name} at {time.ctime(self.start_time)}. You earned 1 point!')

        elif check_out_button:
            if self.checked_in == False:
                st.warning("You need to check in before checking out.")
                return
            elif library_name != self.dest_name:
                st.warning("You have selected a different library. Check out of your previous library before checking in to another one.")
                return

            check_out_data = {
                "player_id": 0,
                "destination_id": library_name,
                "time_start": self.start_time,
                "time_end": time.time()
            }

           # st.session_state.env.on_update([check_out_data])

            st.success(f"Checked out from {library_name} at {time.ctime(check_out_data['time_end'])}. You were there since {time.ctime(check_out_data['time_start'])}")
            self.checked_in = False
                    
                