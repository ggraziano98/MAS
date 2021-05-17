\\GENERAL NOTES:
## Ladley and Schenk-hopp [2007],  Farmer et al. [2005a]
Zero intelligence ABM Financial models implement trader behaviour as noise or (with more sophistication) as random-walks and/or poisson distributions. Even with a lack of elaborate strategies and learning capabilities, Zero Intelligence ABM Financial Models have been shown to reflect the spread-variance dynamics of real markets (data has been tested against the London Stock Exchange) implying that most(some??) of market emergent behaviour is coded in simple structural rules of the market itself rather than by elaborate trading strategies of agents.    
    MORALE DELLA STORIA: Potremmo iniziare a fare il modello concentrandoci solo sulla struttura di mercato, buttandoci poi degli agenti che si comportano (quasi) a caso e magari dargli un network di comunicazione random (quella roba di erdos-renyi) e poi vedere che ne viene fuori. In seguito continuiamo a scavare più a fondo con gli Agenti magari. 

Successione degli eventi: 
Trading giornaliero a tick di m minuti (quindi 60*8/m tick giornalieri per 8 ore di trading)
Attività di network durante la "notte" (cioè da un giorno all'altro di trading gli agenti comunicano tra di loro le proprie opinioni e si aggiorna il network di interazione per il giorno di trading seguente)



# MODEL LEVEL: market_model
    Study of Stock Market Structure

    \\ __init__
        order_book: contains all the waiting orders waiting to be matched and fulfilled
        price_history: contains the price of assets for each time step
        nf = number of fundamentalist traders
        nt = number of technical traders
        N = nf + nt (total number of agents to be kept constant, a switching mechanism between being an nf or a nt trader can be implemented)
        
    

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
            gets initialised as a random wealth distribution
        Assets (in their possession)
            gets initialised in a random way
        S: (Strategy) Amount of stock to buy or to sell for each time step
        Time_Horizon (Needed for fundamentalist traders)
        Opinion_Index: OI€[-1,1] with 1 being optimistic and -1 being pessimistic 

### Tecnical Strategies
General Behaviour Implementation: 
We don't account for the exact strategies used by technical traders but instead try to mimic their general behaviour by assuming they can be either optimistic or pessimistic about the future value of the stock. 

nt = total number of technical traders (tts)
n+ = number of optimistic tts
n- = number of pessimistic tts 
opinion index: x = (n+ + n-)/nt --- x € [-1,1]
        -1: everyone's pessimist
        +1: everyone's optimist
         0: balanced overall sentiment

tech_perc = nt/N --- #percentuale di technicals su N traders, it is needed for the implementation of transition capabilities between being technical and fundamental (see lux-marchesi-2000)
k = frequency of revaluation of opinion 

opinion change coefficient U
U = alpha*x + beta*(time_derivative of price)/k


transition_pn = k*np.exp(U) #transition from being optimist (positive=p) to being pessimist (negative=n)

transition_np = k*np.exp(-U) #transition to being optimist (positive=p) from being pessimist (negative=n)

{tech_perc should be multiplied to transition_ if transition between being t or f is to be implemented in the model}









###### I GOT TOO DEEP WITH THIS: Chartist Implementation
The technical trader calculates the moving averages and derivatives of the log of the price_history and buys/sells an S amount of stock.
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
            ---Send a Buy order of S assets proportional to the derivative difference between MA(x) and MA(y)
        If MA(x)[-1] > MA(y)[-1] AND MA(x)[-2] < MA(y)[-2]:
            Sell Signal
            ---Send a Sell order of S assets proportional to the derivative difference between MA(x) and MA(y)

        
        
### Funamentalist Strategies
    The fundamentalist trader sets an expectation price of the stock 'exp' and buys/sells if the stock price falls below or rises abote the exp price. It will buy/sell only if the ratio between exp and the actual price is higher/lower than the risk free return: 
    exp(i)/p ≥ 1 + (r + π(i))(h(i) − t)
    exp(i)/p ≤ 1 + r(h(i) − t)
    Con: 
    p - prezzo corrente 
    r - risk free return (eg. 2%)
    π - risk premium (se rischio di perdere soldi è perchè voglio guadagnarne di più)
    h - time horizon of the investment

### Market Maker
    It is more an object than an agent. It fulfills all the 


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


# DATACOLLECTORS & VISUALIZATION
Average value of fair value of fundamentalists
Chartist's opinion index time series 

Price Time series 
