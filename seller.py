# -*- coding: utf-8 -*-

# Trading with Zero Intelligence Agents Model without Marshallian Path
# Axel Szmulewiez, Blake LeBaron, Patrick Herb
# Brandeis University
# 04/14/2015
import numpy as np

class Seller:
    # This class defines a seller. A seller has a reservation cost below
    # which he will not trade. Since each seller can only trade once, we
    # record whether a seller traded or not. A seller generates a bid price
    # (which varies depending if the simulation runs with or without
    # constraint)
    
    def __init__(self, maxCost):
        self.Cost = 0
        self.Traded = 0
    
    # Generate ask offer
    def formAskPrice(self, constrained, predictedPrice, maxValue, maxCost):
        if constrained == 1:
            potentialAsk = self.Cost + ((np.random.rand() * np.absolute(maxValue - self.Cost)))
            ask = potentialAsk
        else:
            potentialAsk = np.random.rand() * (maxCost - 1)
            ask = potentialAsk
        return ask
    