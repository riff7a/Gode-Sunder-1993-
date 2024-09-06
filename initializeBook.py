# -*- coding: utf-8 -*-
# Trading with Zero Intelligence Agents Model without Marshallian Path
# Axel Szmulewiez, Blake LeBaron, Patrick Herb
# Brandeis University
# 04/14/2015

def initializeBook(maxCost):
    # Initialize order book variables. Record the best standing bid and ask,
    # the ID of the best bidders (index number in buyer/seller vectors), 
    # transaction price (initialized to 0) and logical variables to determine
    # if there currently is a standing bid or ask. Initially there are no best 
    # bidders, so index of each is 0. The order book vector also records the
    # added value of a given trade (initialized to 0)

    # First index is the best bid (initialized to 0)
    # Second index is the best bid ID (initialized to 0, nobody)
    # Third index is the logical variable for current bid (1 for true, initialized to 0)
    # Fourth index is the best ask (initialized to the max cost for sellers)
    # Fifth index is the best ask ID (initialized to 0, nobody)
    # Sixth index is the logical variable for current ask (1 for true, initialized to 0).
    # Seventh index is the transaction price (initialized to 0)
    # Eight index is surplus added from a given trade (initially 0, no trade)   
    
    orderBookValues = [0 ,0 , 0, maxCost,0, 0, 0, 0]   
    return orderBookValues
