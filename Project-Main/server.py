from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import BarChartModule, PieChartModule, ChartModule

from Market import Mercato

GREEN   = '#0cb325'
RED     = '#cc0808'
BLUE    = '#2655c9'
BLACK   = '#232833'
MID     = "#8b8c94"

AGENT_COL = {
    'tech'  : '#9c0261',
    'noise' : MID,
    'fund'  : '#dba204'
}

'''
Portrayals:
    Line Graph with ask/bid/close or open/close/high/low/volume                 (with hover?)
    Pie Chart with optimists/pessimists/neutral                                 (with filters for dedicated views for technical/fundamentalist/noise?)
    Bar Chart with agent wealth changing each tick                              (again, filter? or show assets/money/all)

On Startup:
    Generate Market
    Generate Agents 
    Generate some noise data to have a reference
'''


class CustomServer(ModularServer):
    '''
    just a wrapper to call a function after initialization
    '''
    def reset_model(self):
        super().reset_model()
        self.model.start()

price_chart = ChartModule(
    [
        {"Label": "ask", "Color": BLACK},
        {"Label": "bid", "Color": BLACK},
        {"Label": "close", "Color": BLUE},
    ]
)

pie_chart = PieChartModule(
    [
        {"Label": "optimists", "Color": GREEN},
        {"Label": "pessimists", "Color": RED},
        {"Label": "neutral", "Color": MID},
    ]
)

wealth_bar = BarChartModule(
    [{"Label": "wealth", "Color": MID}],
    scope="agent",
    sorting="ascending",
    sort_by="wealth",
)

model_params = {
    "nf": UserSettableParameter("slider", "Numero fundamentalists", 10, 1, 20, 1),
    "nt": UserSettableParameter("slider", "Numero technical", 10, 1, 20, 1),
    "nn": UserSettableParameter("slider", "Numero noise", 10, 1, 20, 1),
    "ask0": UserSettableParameter("number", "Ask iniziale", value=101),
    "bid0": UserSettableParameter("number", "Bid iniziale", value=99),
}

server = CustomServer(
    Mercato,
    [price_chart, pie_chart, wealth_bar],
    "Mercato prova 1",
    model_params=model_params,
)

