#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:36:34 2024

@author: james
"""
import random
import time

from logic.classes import Environment, HumanPlayer, BotPlayer, Library

# create test libraries
libraries = [Library(0, position=(random.random(), random.random())),
             Library(1, position=(random.random(), random.random())),
             Library(2, position=(random.random(), random.random())),
             Library(3, position=(random.random(), random.random())),
             Library(4, position=(random.random(), random.random()))
             ]

# create test players
total_players = 100
players = []
for id_ in range(total_players):
    players.append(BotPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20))))
    
# create environment
env = Environment(destinations=libraries, players=players)

# now create fictitious updates
# updates = []
# for i in range(20000):
#     player_id = random.randint(0,999)
#     dest_id = random.randint(0,4)
#     time_start= time.time() - random.randint(10000,10000000)
#     time_end = time_start + random.randint(1000, 20000)
#     update_dic = {"player_id": player_id,
#                   "destination_id": dest_id,
#                   "time_start": time_start,
#                   "time_end": time_end}
#     updates.append(update_dic)

all_dest_ids = [0,1,2,3,4]
# simulating time
for time_step in range(1,1000000, 100):
    new_updates = []
    for player in players:
        prob = player.keenness/10000
        if random.random() < prob:
            # then player has update
            new_updates.append(player.get_update(time_step, all_dest_ids))
    
    env.on_update(new_updates)
    env.update_dest_worths()