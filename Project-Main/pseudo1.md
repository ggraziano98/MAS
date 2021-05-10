General Notes:
## Ladley and Schenk-hopp [2007],  Farmer et al. [2005a]
Zero intelligence ABM Financial models implement trader behaviour as noise or with more sophistication as random-walks and/or poisson distributions. Even with a lack of elaborate strategies and learning capabilities, Zero Intelligence ABM Financial Models have been shown to reflect the spread-variance dynamics of real markets (data has been tested against the London Stock Exchange) implying that most(some??) of market emergent behaviour is coded in simple structural rules of the market itself rather than by elaborate trading strategies of agents.    
    MORALE DELLA STORIA: Potremmo iniziare a fare il modello concentrandoci solo sulla struttura di mercato, buttandoci poi degli agenti che si comportano (quasi) a caso e magari dargli un network di comunicazione random (quella roba di erdos-renyi) e poi vedere che ne viene fuori. In seguito continuiamo a scavare più a fondo con gli Agenti magari. 







# MODEL LEVEL: market_model
    Study of Stock Market Structure

    \\ __init__
        order_book: contains all the waiting orders waiting to be matched and fulfilled
        price_history: contains the price of assets for each time step

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
        Execution of market/limit orders of agents
        Market orders meet limit orders by the best available price. Execution time depends on price.

# AGENT LEVEL:
    Behavioural study of market participants 
    Agent type gets defined by the strategy method(s) of each agent class 

    \\ __init__: 
        Money (in their pocket)
        Assets (in their possession)
        S: (Strategy) Amount of stock to buy or to sell for each time step
        Time_Horizon

## Tecnical Strategies
    The technical trader calculates the moving averages and derivatives of the log of the price_history and buys/sells an S amount of stock

    # Moving Average
    \\ MA(price_history, N):
        MA = []
        Average = (somma degli ultimi N prezzi)/N 
        MA.Append(Average) per ogni time step 
    
    \\ MA_Cross(x,y,z(optional)):
        x > y > z
        The agent calculates three MAs for three different x, y and z time periods.
        The crossover between each of these MAs gives the Technical Agent a buy/sell signal 
        If MA(x)[-1] < MA(y)[-1] AND MA(x)[-2] > MA(y)[-2]:
            Buy Signal
            Send a Buy order of S assets proportional to the derivative difference between MA(x) and MA(y)
        If MA(x)[-1] > MA(y)[-1] AND MA(x)[-2] < MA(y)[-2]:
            Sell Signal
            Send a Sell order of S assets proportional to the derivative difference between MA(x) and MA(y)

        
        
## Funamentalist Strategies
    The fundamentalist trader sets an expectation price of the stock 'exp' and buys/sells if the stock price falls below or rises abote the exp price




## Shared Methods:
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
