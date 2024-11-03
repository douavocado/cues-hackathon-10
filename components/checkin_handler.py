# handle user input for check ins and outs, calculate and accumulate points

import streamlit as st
from components.location_verifier import verify_location

import time
import numpy as np
import random
import threading

class CheckInHandler:
    def __init__(self):
        self.checked_in = False
        self.dest_ids = list(st.session_state.env.destination_dic.keys())
        self.base_weights = np.ones(len(self.dest_ids))/len(self.dest_ids)
        self.trained_env = False
        self.probs = []
        self.y = np.array([])
        self.update_interval = 10
        self.lock = threading.Lock()
        return
    
    def render(self, library_name):
        col1, col2 = st.columns([1, 1])

        with col1:
            check_in_button = st.button("Check In", use_container_width=True)
        with col2:
            check_out_button = st.button("Check Out", use_container_width=True)

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
            st.success(f'Checked in to {library_name} at {time.ctime(self.start_time)}.')

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

            self.update_env(check_out_data)
            # st.session_state.env.on_update([check_out_data])
            st.success(f"Checked out from {library_name} at {time.ctime(check_out_data['time_end'])}. You were there since {time.ctime(check_out_data['time_start'])}")
            self.checked_in = False


    def update_env(self, check_out_data):
        with self.lock:
            new_updates = []
            
            weights = self.base_weights + 0.2*np.random.random(size=len(self.dest_ids)) # slight perturb
            weights = weights/np.sum(weights)
            self.probs.append(weights)
            self.y = np.append(self.y, [0])
            players = st.session_state.env.player_dic.values()
            for player in players:
                if player.id == 0:
                    continue
                prob = player.keenness/100
                if random.random() < prob:
                    # then player has update
                    update = player.get_update(time.time(), self.dest_ids, weights=weights)
                    new_updates.append(update)

            # human player has update
            if len(check_out_data) > 0:
                new_updates.append(check_out_data)
                # duration = int((check_out_data["time_end"]-check_out_data["time_start"])/self.update_interval)
                self.y[-1] = 1

                # now update model
                st.session_state.env.add_data(self.probs, self.y)
                if self.trained_env:
                    st.session_state.env.adapt_model()
                else:
                    st.session_state.env.train_full_model()
                    self.trained_env = True

            if self.trained_env:
                st.session_state.env.on_update(new_updates)
                st.session_state.env.update_dest_worths()

                # prepare for next update
                self.base_weights = st.session_state.env.model_class.get_weights(len(self.dest_ids))     
                