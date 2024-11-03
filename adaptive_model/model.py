#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:43:49 2024

@author: james
"""
import numpy as np
from scipy.optimize import minimize


class Model:
    def __init__(self, model):
        self.model = model
        
    def train_full(self, X, y):
        # X is just the weight_probabilities for each destination
        # y is an indicator for whether the human player is active or not
        self.model.fit(X,y)
        
    def train_partial(self, X,y):
        self.model.partial_fit(X,y)
        
    def get_weights(self, input_dim):
        def objective_function(weights, model):
            """
            Calculates the negative of the predicted probability of y=1 
            (since we'll use a minimization function).
            """
            # Ensure weights sum to 1 (constraint)
            weights = weights / np.sum(weights) 
            probability_y1 = model.predict_proba(weights.reshape(1, -1))[0][1]
            return -probability_y1  
        
        # Initial guess for probability weights
        initial_weights = np.ones(input_dim)/input_dim
        
        # Constraints (e.g., weights must sum to 1)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds (e.g., weights must be between 0 and 1)
        bounds = [(0, 1) for _ in range(len(initial_weights))]
        
        # Perform optimization
        result = minimize(
            objective_function, 
            initial_weights, 
            args=(self.model,),  # Pass the trained model
            method='SLSQP',  # Suitable for constrained optimization
            bounds=bounds,
            constraints=constraints
        )
        
        # Get the optimized weights
        optimized_weights = result.x / np.sum(result.x)  # Normalize to ensure sum to 1
        print("Optimized Weights:", optimized_weights)
        return optimized_weights