# -*- coding: utf-8 -*-
# Trading with Zero Intelligence Agents Model without Marshallian Path
# Python version: David Ritzwoller, Blake LeBaron
# based on original matlab code by,
# Axel Szmulewiez, Blake LeBaron, Patrick Herb
# Brandeis University
# 04/14/2015
# 07/22/2016

# We implement a dynamic model of zero intelligence traders developed by
# Gode & Sunder (1993). We evaluate the role of the market as a natural
# allocator of resources in the economy. By having near Zero Intelligence
# agents who don't maximize profits or utility functions, we exclude the
# human factor in trade and isolate the roles of demand and supply. 

# The market is structured as a double aucion order book. When a trade takes
# places, it reinitializes the order book. The price of the transaction is 
# that of the bid/ask that is submitted to match the current best standing 
# offer. Each trade is for one unit. There are 100 buyers and 100 sellers
# that submit offers for 8000 iterations. Each trader is allowed to trade
# only once. The program compares the simulation's performance with the 
# theoretical economically efficient outcome.

# Sources: 
#           Allocative Efficiency of Markets with Zero-Intelligence
#           Traders: Market as a Partial Substitute for Individual
#           Rationality, Gode & Sunder (1993)
#
#           On the Behavioral Foundations of the Law of Supply and Demand:
#           Human Convergence and Robot Randomness, Brewer, Huang, Nelson &
#           Plott (2002)
#
#           Mark E. McBride, Department of Economics, Miami University, on
#           the development of the model in NetLogo and particular
#          contribution to this program in the design of order book
#           mechanics.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Buyer import Buyer
from Seller import Seller
from initializeBook import initializeBook
from doTrade import doTrade
# Get parameters from user

# Simulation runs with 100 buyers and 100 sellers (a market big enough to 
# consider it perfectly competitive

numberTraders = 500
# refresh demands 
#  This option if set to true will draw new values/costs for all agents who 
#  have not traded.  This is like a continuous refresh and this eliminates
#  the Marshallian path (see )
refresh = False

# Get input for maximum buyer value and seller cost (shape the demand and
# supply curves). Make sure inputs are positive
maxValue = 0 
while maxValue <= 0:
    maxValue = float(input('Please enter the desired maximum buyer value(demand curve upper bound, > 10 suggested): '))

maxCost = 0
while maxCost <= 0:
    maxCost = float(input('Please enter the desired maximum seller cost (supply curve upper bound, > 10 suggested): '))

# Run simulation with 50000 iteration
iterations = 50000

# Determine whether simulation will be constrained or unconstrained. Lock
# in while loop until valid input is given
constrained = -1
while (constrained != 0) & (constrained != 1):
    constrained = int(input('Please enter ''1'' for constrained simulation , ''0'' for unconstrained:  '))

# Determine whether simulation will have a price ceiling 5% above
# theoretical equilibrium price. Lock in while loop until valid input is
# given
ceiling = -1
# while (ceiling != 0) & (ceiling != 1):
#    ceiling = int(input('Please enter ''1'' to include a price ceiling in the simulation, ''0'' otherwise: '))

# Create vector holding all buyers
buyers = []    
for i in range(numberTraders):
    buyers.append(Buyer(maxValue))
    
# Initialize all buyers to not traded state and give them a reservation
# price (random variable bounded above)
valueVec = maxValue*np.random.rand(numberTraders)
for i in range(numberTraders):
    buyers[i].Value = valueVec[i]
    buyers[i].Traded = 0


    
# Create vector holding all sellers
sellers = []
for i in range(numberTraders):
    sellers.append(Seller(maxCost))
    
# Initialize all sellers to not traded state and give them a reservation
# cost (random variable bounded below)
costVec = maxCost*np.random.rand(numberTraders)
for i in range(numberTraders):
    sellers[i].Cost = costVec[i]
    sellers[i].Traded = 0

    
# Sort buyer and seller vectors to calculate equilibrium values and to 
# later plot demand and supply curves
buyerValues = []
for i in range(numberTraders):
    buyerValues.append(buyers[i].Value)
buyerValues.sort(reverse = True)

sellerCosts = []
for i in range(numberTraders):
    sellerCosts.append(sellers[i].Cost)
sellerCosts.sort()
    
# Compute theoretical equilibrium and surplus
predictedPrice = 0
predictedQuantity = 0
maximumSurplus = 0
for i in range(numberTraders):
    # If value of buyer is greater than cost of seller, there is a trade.
    # Then, quantity increases by one, there are gains for trade (surplus)
    # and the price is updated
    if(buyerValues[i] - sellerCosts[i]) > 0:
        predictedPrice = (buyerValues[i] + sellerCosts[i]) /2
        predictedQuantity = predictedQuantity + 1
        maximumSurplus = maximumSurplus + (buyerValues[i] - sellerCosts[i])
        
# Initialize the order book vector. Please see function description for the
# values held in each index
orderBookValues = initializeBook(maxCost)

# Initialize vector with transaction prices (update as iterations execute).
# Let the length of the vector be the maximum number of iterations, then
# discard leftover indexes initialized to zero for efficiency
transactionPrices = []

# Initial surplus is 0
surplus = 0

# Initial quantity traded is 0
quantity = 0

tradedValues = []
tradedCosts  = []

for i in range(iterations):
    # Stop the loop if all buyers and sellers have already traded. Note
    # that if all buyers have traded, all sellers have traded, since each
    # trader is allowed to trade only once
    if sum(buyers.Traded for buyers in buyers) == numberTraders:
        break
    
    # Attempt a trade or a new bid/ask (report update if trade occurs). 
    # Pass vectors of buyers and sellers to manipulate, the order book 
    # values to update trade information, number of traders to give upper 
    # bound for random generation of index that determines chosen trader, 
    # and constraing choice along with predicted price and max value for 
    # trader to generate bid/offer
    orderBookValues = doTrade(buyers, sellers, orderBookValues, numberTraders, predictedPrice, constrained, maxValue, maxCost)
    
    # Record transaction price, update surplus and quantity, mark traders 
    # to record that they have traded, and reinitialize the order book
    # if a trade occured
    if orderBookValues[6] > 0:
        transactionPrices.append(orderBookValues[6])
        surplus = surplus + orderBookValues[7]
        buyers[orderBookValues[1]].Traded = 1
        sellers[orderBookValues[4]].Traded = 1
        tradedValues.append(buyers[orderBookValues[1]].Value)
        tradedCosts.append(sellers[orderBookValues[4]].Cost)
        orderBookValues = initializeBook(maxCost)
        quantity = quantity +1
        # if refresh is True, then redraw values for all buyers and sellers
        #   this makes this as if at start with a complete refresh
        if refresh:
            for checkBuyer in buyers:
                if(checkBuyer.Traded == 0):
                    checkBuyer.Value = valueVec[np.random.randint(numberTraders)]
            for checkSeller in sellers:
                if(checkSeller.Traded == 0):
                    checkSeller.Cost = costVec[np.random.randint(numberTraders)]

# Calculate simulation surplus as percentage of total possible surplus
# This is a prototype area for the refresh option
# This should probably be eliminated in production
# no great way to estimate theoretical surplus under refresh
if refresh:
    tradedValnp = np.array(tradedValues)
    tradedCostnp = np.array(tradedCosts)
    tradedValnp = np.sort(tradedValnp)[::-1]
    tradedCostnp.sort()
    infraMarginal = (tradedValnp>tradedCostnp)
    maximumSurplus = np.sum(tradedValnp[infraMarginal]-tradedCostnp[infraMarginal])


surplusPercentage = surplus / maximumSurplus * 100.
SimulationPrice = np.mean(transactionPrices[-50:])

# Generate rolling means and variances with Panda (needs version 0.18)
priceTS = pd.Series(transactionPrices,index=range(len(transactionPrices)))
priceRoll = priceTS.rolling(window=50,min_periods=10)
priceVar = priceRoll.var()
priceMean = priceRoll.mean()

################################
#   REPORT RESULTS AND GRAPH   #
################################

# Plot demand and supply curves and price pattern
# Plot Supply and Demand using sorted values and costs vectors initialized
# to calculate equlibrium values. Also plot price path

xPrice = [1*x for x in range(len(transactionPrices))]
x = [1*x for x in range(numberTraders)]
fig,ax = plt.subplots()
ax.plot(x, buyerValues, 'r')
ax.plot(x, sellerCosts, 'g')
ax.plot(xPrice, transactionPrices, 'k')
ax.plot(xPrice, priceMean.values, 'b')

    
# Adjust and label axes and title
ax.set_xlabel('Quantity')
ax.set_ylabel('Price')
ax.set_title('Market For Traded Asset')
ax.grid()


# ax
fig2, a2 = plt.subplots()
a2.plot(priceVar)
# a2.plot(priceMean)
a2.set_xlabel('Period')
a2.set_ylabel('Price variance')
a2.grid()
plt.show()



# Report statistics results
print('Simulation Results:')
print('The predicted quantity was '+str(predictedQuantity)+', and the predicted price was '+ str(predictedPrice)[0:5])
print('The simulation quantity is '+str(quantity)+' ,and the simulation price is '+ str(SimulationPrice)[0:5])    
print('The simulation achieved '+str(surplusPercentage)[0:5]+' ,of the total available surplus')



    




    
    
    
    

