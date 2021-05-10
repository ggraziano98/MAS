General Notes:
## Ladley and Schenk-hopp [2007],  Farmer et al. [2005a]
Zero intelligence ABM Financial models implement trader behaviour as noise or with more sophistication as random-walks and/or poisson distributions. Even with a lack of elaborate strategies and learning capabilities, Zero Intelligence ABM Financial Models have been shown to reflect the spread-variance dynamics of real markets (data has been tested against the London Stock Exchange) implying that most(some??) of market emergent behaviour is coded in simple structural rules of the market itself rather than by elaborate trading strategies of agents.    
    MORALE DELLA STORIA: Potremmo iniziare a fare il modello concentrandoci solo sulla struttura di mercato, buttandoci poi degli agenti che si comportano (quasi) a caso e magari dargli un network di comunicazione random (quella roba di erdos-renyi) e poi vedere che ne viene fuori. In seguito continuiamo a scavare più a fondo con gli Agenti magari. 







# MODEL LEVEL: market_model
    Study of Stock Market Structure

    \\ __init__
        Order_Book: contains all the waiting orders waiting to be matched and fulfilled
        Price_History: contains the price of assets for each time step

    \\ Bid-Ask Method:
        Takes the highest buying price (BID) and the lowest selling price (ASK) and communicates this information to all agents in real time. 
        
        .. datacollector: computation of spread (ASK-BID) [can be useful for analysing if spread behavior has correlation with bubble-crashes behaviorLi]

    \\ Fulfill Method: 
        Fulfills an order each time a buy and a sell meet at a price 
        The exchangers (agents selling-buying to eachother) will receive money-assets on their respective variables 
        The order gets removed from the order book

    \\ Volume Method: 
        Calculates the total volume of exchange for each step of the market_model 
        .. datacollector: sum of all fulfills in terms of the number of assets


    \\ STEP Method:
        Time ordered execution of market/limit orders of agents   

# AGENT LEVEL:
    Behavioural study of market participants 

## Shared Methods:
    \\ __init__: 
        Money (in their pocket)
        Assets (in their possession)
        Strategy: Amount of stock to buy or to sell for each time step

    \\ (Limit) BUY Method:
        each category of agent can perform a buy action 
        the agent will communicate to the market_model its limit price 
    
    \\ (Limit) SELL Method: 
        each category of agent can perform a sell action 
        the agent will communicate to the market_model its limit price

    \\ (Market) BUY Method: 
        each category of agent can perform a sell action 
        the agent will buy the current ASK price

    \\ (Market) SELL Method: 
        each category of agent can perform a sell action 
        the agent will sell the current BID price 
    
    \\ Order_Cancel Method: 
        The agent can decide to cancel an unexecuted order












    
    \\ STEP Method:
        Decision making process and execution of the decision 

# NETWORK LEVEL: 
    Study of self-organising social interaction networks applied to financial actors 
