# -*- coding: utf-8 -*-

# Trading with Zero Intelligence Agents Model without Marshallian Path
# Axel Szmulewiez, Blake LeBaron, Patrick Herb
# Brandeis University
# 04/14/2015
import numpy as np

class Buyer:
    # This class defines a buyer. A buyer has a reservation value above
    # which he will not trade. Since each buyer can only trade once, we
    # record whether a buyer traded or not. A buyer generates a bid price
    # (which varies depending if the simulation runs with or without
    # constraint)
    
    def __init__(self, maxValue):
        self.Value = 0
        self.Traded = 0
    
    # Generate a bid offer
    def formBidPrice(self,constrained, predictedPrice, maxValue):
        if constrained == 1:
            potentialBid = self.Value - (np.random.rand() * (self.Value -1))
            bid = potentialBid
        else:
            potentialBid = np.random.rand() * (maxValue - 1)
            bid = potentialBid
        return bid
        
    