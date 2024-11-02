#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:09:23 2024

@author: james
"""
import random
import numpy as np

def get_random_update(time_end, possible_dst_ids, stay_keenness, last_end=None):
    # on function call, a bot player will randomly goto the library somewhere.
    # for this we will assume just a random time between 1000 and 20000 seconds
    # drawn from the poisson distribution with mean 7000 (just under 2 hours)
    # if the bot is keen, then we ramp this up by factor depending on stay_keenness
    time_spent = (0.5+stay_keenness/10)*np.random.poisson(7000)
    if last_end is None:
        time_start = max(time_end-time_spent, 1)
    else:
        time_start = max(time_end-time_spent, last_end)
    
    # the logic we choose for destination is random also
    dest_id = random.choice(possible_dst_ids)
    
    update_dic = {"destination_id": dest_id,
                  "time_start": time_start,
                  "time_end": time_end}
    return update_dic