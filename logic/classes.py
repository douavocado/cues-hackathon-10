#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 13:42:06 2024

@author: james
"""
import time

class Player:
    def __init__(self, id_, player_type=None, total_score=0):
        self.id = id_
        self.player_type=player_type
        self.total_score = total_score
        self.dest_times = {}
        self.dest_times_history = {} # key is dest.id, value is a list of [time_start, time_added]
    
    def add_destination(self, dest):
        self.dest_times[dest.id] = 0
        self.dest_times_history[dest.id] = []
    
    def update_dest_time(self, dest, time_start, time_added, max_hist, max_hist_time):
        if dest.id not in self.dest_times:
            self.add_destination(dest)
        
        current_time = time.time()
        self.dest_times_history[dest.id].append([time_start, time_added])
        self.dest_times_history[dest.id] = [x for x in self.dest_times_history[dest.id] if current_time - x[0] < max_hist_time]
        self.dest_times_history[dest.id].sort(reverse=True, key=lambda x: x[1])
        self.dest_times_history[dest.id] = self.dest_times_history[dest.id][:max_hist] # only take top max_hist amount of added times
        added_times = [x[1] for x in self.dest_times_history[dest.id]]
        self.dest_times[dest.id] = sum(added_times)
    
    def update_total_score(self, score):
        self.total_score = score
        
class HumanPlayer(Player):
    def __init__(self, id_, total_score=0):
        super().__init__(id_, player_type="human", total_score=total_score)

class BotPlayer(Player):
    def __init__(self, id_, total_score=0):
        super().__init__(id_, player_type="bot", total_score=total_score)

class Destination:
    def __init__(self, id_, position=None, tolerance=0.0005, destype=None, worth=100000):
        self.worth=worth
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

class Library(Destination):
    def __init__(self, id_, position=None, tolerance=0.0005, worth=100000):
        super().__init__(id_, position=position, tolerance=tolerance, destype="library", worth=worth)
        
class Environment:
    def __init__(self, destinations = [], players = [], max_hist_time=4838400, max_hist=10):
        self.destination_dic = {destination.id: destination for destination in destinations}
        self.player_dic = {player.id: player for player in players}
        self.max_hist = max_hist
        self.max_hist_time = max_hist_time
    
    def add_player(self, player):
        self.player_dic[player.id] = player
    
    def add_destination(self, dest):
        self.destination_dic[dest.id] = dest
    
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
            self.player_dic[player_id].update_dest_time(self.destination_dic[dest_id], update_dic["time_start"], added_time, self.max_hist, self.max_hist_time)
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