from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import BarChartModule, PieChartModule, ChartModule

from model.Market import Mercato

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
    Line Graph with ask/bid/close or open/close/high/low/volume                 (cambiare l'api per avere solo gli ultimi N)
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
    def __init__(self, model_cls, visualization_elements, name="Mesa Model", model_params=...):
        self.settings["debug"] = False
        self.settings["autoreload"] = True
        self.verbose = False

        super().__init__(model_cls, visualization_elements, name, model_params)

    def reset_model(self):
        super().reset_model()
        self.model.start()

ask_bid_chart = ChartModule(
    [
        {"Label": "ask", "Color": GREEN},
        {"Label": "bid", "Color": RED},
    ]
)

price_chart = ChartModule(
    [
        {"Label": "price", "Color": GREEN},
    ]
)

tech_fraction_chart = ChartModule(
    [
        {"Label": "technical_fraction", "Color": GREEN},
    ]
)

tech_pie_chart = PieChartModule(
    [
        {"Label": "tech_optimists", "Color": GREEN},
        {"Label": "tech_pessimists", "Color": RED},
        {"Label": "nf", "Color": BLUE}
    ]
)

model_params = {
    "nt": UserSettableParameter("slider", "Numero Technical", 10, 0, 500, 1),
    "nf": UserSettableParameter("slider", "Numero Fundamentalists", 490, 0, 500, 1),
}

server = CustomServer(
    Mercato,
    [ask_bid_chart, tech_pie_chart, price_chart, tech_fraction_chart],
    "Mercato prova 1",
    model_params=model_params,
)


