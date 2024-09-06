# -*- coding: utf-8 -*-
import numpy as np
# Trading with Zero Intelligence Agents Model without Marshallian Path
# Axel Szmulewiez, Blake LeBaron, Patrick Herb
# Brandeis University
# 04/14/2015


def doTrade(buyers, sellers, bookValues, numberTraders, predictedPrice, constrained, maxValue, maxCost):
    # This function operates the double auction order book. The function
    # determines with 50% probability whether the next trader to submit an
    # offer is a buyer or a seller. Then, it compares the new bid/ask and
    # executes a trade if it satisfies the counterposing best standing offer,
    # or it takes the place as best offer of its kind if it is better than the
    # currently standing one (for example, if a new bid is submitted and it is
    # higher than the best ask, a trade will occur, but if it's not higher than
    # the best ask but higher than the best standing bid it will take its
    # place. A similar process takes place if a seller submits an ask). The
    # function returns an updated state of the order book to update simulation.
    
    # Initialize return vector to current book values
    updatedValues = bookValues
    
    # Randomly choose between a buyer and a seller (belor 0.5 we select a
    # buyer, otherwise we select a seller).
    traderDeterminer = np.random.rand()
    
    # Process as buyer
    if traderDeterminer <0.5:
        
        # Initialize a new buyer ID (at first 0)
        newBuyer = -1
        
        #Choose a random buyer that has yet not traded. Lock selection of a
        # buyer in a while loop until it chooses a buyer that hasn't traded
        while newBuyer == -1:
            # Choose a random index in the buyers vector to select a buyer
            randomIndex = np.random.randint(0, numberTraders)
            if buyers[randomIndex].Traded == 0:
                newBuyer = randomIndex
    
        
        # Make buyer generate a random bid based on its reservation price and
        # simulation constraint
        newBid = buyers[newBuyer].formBidPrice(constrained, predictedPrice, maxValue)
        
        # Do a trade if there is currently a standing ask that the bid can
        # trade with. Check the logical variable and the value of the best
        # standing ask
        if (updatedValues[5] == 1) & (newBid > updatedValues[3]):
            # Set the transaction price to the best ask value
            updatedValues[6] = updatedValues[3]
            # Record surplus added by the trade
            updatedValues[7] = buyers[newBuyer].Value - sellers[updatedValues[4]].Cost
            # Update ID of buyer
            updatedValues[1] = newBuyer
        
        # If the there is no trade, set the bid as best bid if it is higher
        # than the currently standing best bid, even if it doesn't satisfy the
        # ask or if there currently is no ask
        else:
            if newBid > updatedValues[0]:
                # Set new bid as best bid, and update the ID of bidder
                updatedValues[0]= newBid
                updatedValues[1] = newBuyer
                # Set logical variable for standing bid to true
                updatedValues[2] = 1
                # If new bid is lower than best bid, do nothing
    # Process a seller
    else:
        # Initialize a new seller ID (at first 0)
        newSeller = -1
        # Choose a random seller that has yet not traded. Lock selection of a
        # seller in a while loop until it chooses a seller that hasn't traded
        while newSeller == -1:
            # Choose a random index in the sellers vector to select a seller
            randomIndex = np.random.randint(0, numberTraders)
            if sellers[randomIndex].Traded == 0:
                newSeller = randomIndex
        
        # Make seller generate a random ask based on its reservation cost and
        # simulation constraint
        newAsk = sellers[newSeller].formAskPrice(constrained, predictedPrice, maxValue, maxCost)
        
        # Do a trade if there is currently a standing bid that the ask can
        # trade with. Check the logical variable and the value of the best
        # standing bid
        if (updatedValues[2] == 1) & (updatedValues[0] > newAsk):
            # Set the transaction price to the best bid value
            updatedValues[6] = updatedValues[0]
            # Record surplus added by the trade
            updatedValues[7] = buyers[updatedValues[1]].Value - sellers[newSeller].Cost
            # Record ID of seller
            updatedValues[4] = newSeller
        # If the there is no trade, set the ask as best ask if it is lower
        # than the currently standing best ask, even if it doesn't satisfy the
        # bid or if there currently is no bid
        else:
            if newAsk < updatedValues[3]:
                # Set new ask as best ask, and update the ID of bidder
                updatedValues[3] = newAsk
                updatedValues[4] = newSeller
                # Set logical variable for standing ask to true
                updatedValues[5] = 1
                # If new ask is higher than best ask, do nothing
       
    return updatedValues

        
            
                
                