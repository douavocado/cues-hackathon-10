#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 13:42:06 2024

@author: james
"""
import time
import numpy as np

from sklearn.linear_model import SGDClassifier

from logic.bot_logic import get_random_update, get_adaptive_update
from adaptive_model.model import Model

class Player:
    def __init__(self, id_, player_type=None, total_score=0):
        self.id = id_
        self.player_type=player_type
        self.total_score = total_score
        self.dest_times = {}
        self.dest_times_history = {} # key is dest.id, value is a list of [time_start, time_added]
        self.last_end = 0 # last time we were at a library
    
    def add_destination(self, dest):
        self.dest_times[dest.id] = 0
        self.dest_times_history[dest.id] = []
    
    def update_dest_time(self, dest, time_start, time_added, max_hist, max_hist_time, current_time=None):
        if dest.id not in self.dest_times:
            self.add_destination(dest)
        
        if current_time is None:
            current_time = time.time()
        
        self.last_end = max(self.last_end, time_start+time_added) # setting last end to be accurate
            
        self.dest_times_history[dest.id].append([time_start, time_added])
        self.dest_times_history[dest.id] = [x for x in self.dest_times_history[dest.id] if current_time - x[0] < max_hist_time]
        self.dest_times_history[dest.id].sort(reverse=True, key=lambda x: x[1])
        self.dest_times_history[dest.id] = self.dest_times_history[dest.id][:max_hist] # only take top max_hist amount of added times
        added_times = [x[1] for x in self.dest_times_history[dest.id]]
        # clean up empty lists
        if len(self.dest_times_history[dest.id]) == 0:
            del self.dest_times_history[dest.id]
        
        self.dest_times[dest.id] = sum(added_times)
    
    def update_total_score(self, score):
        self.total_score = score
        
    def get_type(self):
        if self.player_type is None:
            raise NotImplementedError()
        return self.player_type
    
    def __repr__(self):
        return "Player{}(type:{}, total_score:{})".format(self.id, self.get_type(), self.total_score)
        
class HumanPlayer(Player):
    def __init__(self, id_, total_score=0):
        super().__init__(id_, player_type="human", total_score=total_score)

class BotPlayer(Player):
    def __init__(self, id_, base_location, adaptive=False, total_score=0, keenness=5, stay_keenness=5):
        super().__init__(id_, player_type="bot", total_score=total_score)
        self.base_location = base_location
        self.keenness = keenness # how frequently we goto library
        self.stay_keenness = stay_keenness # once we are at library how long we stay
        self.adaptive = adaptive
    
    def get_update(self, time_end, possible_dst_ids, weights=None):
        # get random update
        if weights is None or self.adaptive == False:
            update_dic = get_random_update(time_end, possible_dst_ids, self.stay_keenness, last_end=self.last_end)
        else:            
            update_dic = get_adaptive_update(time_end, possible_dst_ids, self.stay_keenness, weights, last_end=self.last_end)
        
        
        # add our id to the dictionary
        update_dic["player_id"] = self.id
        return update_dic

class Destination:
    def __init__(self, id_, position=None, tolerance=0.0005, destype=None, base_worth=3600):
        self.worth=base_worth
        self.base_worth = base_worth
        self.id = id_
        self.tolerance=tolerance
        self.position = position
        self.destype = destype
        self.player_ids = []
        self.time_stores = {}
        self.share_worth = None
    
    def add_player(self, id_):
        self.player_ids.append(id_)
        self.time_stores[id_] = 0
    
    def update_player(self, player):
        self.time_stores[player.id] = player.dest_times[self.id]
    
    def calculated_total_time(self):
        return sum(self.time_stores.values())
    
    def calculate_worth_per_time(self):
        total_shares = max(self.calculated_total_time(),1)
        self.share_worth = self.worth/total_shares
    
    def update_worth(self):
        raise NotImplementedError()

class Library(Destination):
    def __init__(self, id_, position=None, tolerance=0.0005, base_worth=3600):
        super().__init__(id_, position=position, tolerance=tolerance, destype="library", base_worth=base_worth)
    
    def update_worth(self):
        # based on total time spent in the last max_hist_time , square rooted
        no_users = len(self.time_stores)
        self.worth = self.base_worth*(no_users+1) + (self.calculated_total_time())**0.5
        
class Environment:
    def __init__(self, destinations = [], players = [], max_hist_time=4838400, max_hist=10):
        self.destination_dic = {destination.id: destination for destination in destinations}
        self.player_dic = {player.id: player for player in players}
        self.max_hist = max_hist
        self.max_hist_time = max_hist_time
        # Initialize the model
        model = SGDClassifier(loss="log_loss", learning_rate="adaptive", eta0=0.005) 
        self.model_class = Model(model)
        
        self.prob_history = [] # running track of previous probabilities used
        self.active_history = [] # running track of binary 0-1 whether human player was active
    
    def add_player(self, player):
        self.player_dic[player.id] = player
    
    def add_destination(self, dest):
        self.destination_dic[dest.id] = dest
    
    def update_dest_worths(self):
        for dest_id in self.destination_dic.keys():
            self.destination_dic[dest_id].update_worth()
    
    def on_update(self, update_dics):
        """ 
            Update Dictionary of the form
            {"player_id": int,
             "destination_id": str,
             "time_start": int,
             "time_end": int}
            
            update_dics is a list of update dictionaries
        """
        
        # first update the player stats
        for update_dic in update_dics:
            player_id = update_dic["player_id"]
            dest_id = update_dic["destination_id"]
            added_time = update_dic["time_end"] - update_dic["time_start"]
            self.player_dic[player_id].update_dest_time(self.destination_dic[dest_id], update_dic["time_start"], added_time, self.max_hist, self.max_hist_time, current_time=update_dic["time_end"])
            self.destination_dic[dest_id].update_player(self.player_dic[player_id])
        
        # now calculate share worths for each library
        for dest_id in self.destination_dic.keys():
            self.destination_dic[dest_id].calculate_worth_per_time()
            
        # now update all player total_scores
        for player_id in self.player_dic.keys():
            total_score = 0
            for dest_id in self.player_dic[player_id].dest_times.keys():
                total_score += self.destination_dic[dest_id].share_worth * self.player_dic[player_id].dest_times[dest_id]
            self.player_dic[player_id].update_total_score(total_score)
    
    def add_data(self, probs, active):
        self.prob_history.extend(probs)
        self.prob_history = self.prob_history[-self.max_hist_time:]
        self.active_history.extend(active)
        self.active_history = self.active_history[-self.max_hist_time:]
    
    def train_full_model(self):
        X = np.array(self.prob_history)
        y = np.array(self.active_history)
        # now adapt model
        self.model_class.train_full(X,y)
        
    def adapt_model(self):
        # first get data ready
        X = np.array(self.prob_history)
        y = np.array(self.active_history)
        # now adapt model
        self.model_class.train_partial(X,y)
    
    def get_dest_share_prices(self):
        # returns a dictionary with key the destination id, value is the share price for the destination
        return {dest.id: dest.share_worth for dest in self.destination_dic.values()}
    
    def get_player_scores(self):
        # returns a dictionary with key player id, values is the player's total score
        return {player.id: player.total_score for player in self.player_dic.values()}
    
    def get_player_score(self, player_id):
        return self.get_player_scores()[player_id]
    
    def get_dest_share_price(self, dest_id):
        return self.get_dest_share_prices()[dest_id]
    
    def get_player(self, player_id):
        return self.player_dic[player_id]
    
    def get_destination(self, dest_id):
        return self.destination_dic[dest_id]
    
    def get_players(self, player_ids):
        return [self.get_player(id_) for id_ in player_ids]
    
    def get_destination_players(self, dest_id):
        # get all the players that have been at a certain destination
        ids =  list(self.destination_dic[dest_id].time_stores.keys())
        return self.get_players(ids)
    
    def get_score_leaders(self, leaders=10):
        # return ids of score leaders
        ordered_player_ids = sorted(self.player_dic.keys(), key=lambda x:self.player_dic[x].total_score, reverse=True)
        top = ordered_player_ids[:leaders]
        return top
    
    def get_score_leader_dic(self, leaders=10):
        # return ids of score leaders
        leader_ids = self.get_score_leaders(leaders=leaders)
        return {id_:self.player_dic[id_].total_score for id_ in leader_ids}
    