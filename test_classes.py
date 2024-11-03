#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:36:34 2024

@author: james
"""
import random
import time
import numpy as np

from logic.classes import Environment, HumanPlayer, BotPlayer, Library


prop_adaptive = 1
# create test libraries
libraries = [Library(0, position=(random.random(), random.random()), base_worth=random.randint(1000,10000)),
             Library(1, position=(random.random(), random.random()), base_worth=random.randint(1000,10000)),
             Library(2, position=(random.random(), random.random()), base_worth=random.randint(1000,10000)),
             Library(3, position=(random.random(), random.random()), base_worth=random.randint(1000,10000)),
             Library(4, position=(random.random(), random.random()), base_worth=random.randint(1000,10000))
             ]

# create test players
total_players = 100
players = []
for id_ in range(total_players):
    if id_ == 0:
        players.append(HumanPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20)), adaptive= True, keenness=random.randint(1,10), stay_keenness=random.randint(1,10)))
    elif np.random.random() < prop_adaptive:
        players.append(BotPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20)), adaptive= True, keenness=random.randint(1,10), stay_keenness=random.randint(1,10)))
    else:
        players.append(BotPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20)), adaptive= False, keenness=random.randint(1,10), stay_keenness=random.randint(1,10)))
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

# human id is id 0

all_dest_ids = [0,1,2,3,4]
# simulating time
base_weights = np.ones(len(all_dest_ids))/len(all_dest_ids)
probs = []
y = []
step = 10
keen_constant = 5000000/step
trained = False

DATA_STORE = []

for time_step in range(0,1000000000, step):
    data_dic = {}
    
    new_updates = []
    weights = base_weights + 0.2*np.random.random(size=(len(all_dest_ids))) # slight perturb
    weights = weights/np.sum(weights)
    for player in players:
        prob = player.keenness/keen_constant
        if random.random() < prob:
            # then player has update
            update = player.get_update(time_step, all_dest_ids, weights=weights)
            new_updates.append(update)
            if player.id == 0:
                duration = int((update["time_end"]-update["time_start"])/step)
                y[-duration:] = [1]*duration
                # now update model
                env.add_data(probs, y)
                if trained:
                    env.adapt_model()
                else:
                    env.train_full_model()
                probs = []
                y = []
                base_weights = env.model_class.get_weights(len(all_dest_ids))
    env.on_update(new_updates)
    env.update_dest_worths()
    # update human keenness
    players[0].update_keenness(env.get_dest_share_prices())
    # now capture data instances and train adapative model
    # if time_step % 10000 == 0:
    probs.append(weights)
    y.append(0)
    
    data_dic["time"] = time_step
    data_dic["player_score"] = players[0].total_score
    data_dic["player_dest_scores"] = players[0].dest_times
    data_dic["dest_share_prices"] = env.get_dest_share_prices()
    data_dic["adaptive_probs"] = {x : base_weights[x] for x in range(len(base_weights))}
    data_dic["leader_board"] = env.get_score_leader_dic()
    
    DATA_STORE.append(data_dic)
    