from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Mercato import Mercato

COLORS = {"Vucumpra": "#00AA00", "Umarell": "#880000"}


def market_portrayal(cell):
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[type(cell)]
    return portrayal


canvas_element = CanvasGrid(market_portrayal, 100, 100, 500, 500)

model_params = {
    "height": 40,
    "width": 40,
    "N": UserSettableParameter("slider", "Numero vucumprà", 1, 1, 20, 1),
    "M": UserSettableParameter("slider", "Numero compratori", 1, 1, 30, 1),
}
server = ModularServer(
    Mercato, [canvas_element], "Mercato", model_params
)