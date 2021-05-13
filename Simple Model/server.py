from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import NetworkModule

from Mercato import Mercato

COLORS = {"Vucumpra": "#00AA00", "Umarell": "#880000"}

W, H = 10, 10


def network_portrayal(G):
    # The model ensures there is 0 or 1 agent per node

    portrayal = dict()
    portrayal["nodes"] = []
    
    for (node_id, agents) in G.nodes.data("agent"):

        element = {
            "id": node_id,
            "size": 3 if agents else 1,
            "color": '#333333' if not agents else "#FF0000" if agents[0].agent_type == 'Vucumpra' else "#00FF00",
            # "label": None
            # if not agents
            # else "Agent:{} Wealth:{}".format(agents[0].unique_id, agents[0].wealth),
        }
        
        portrayal["nodes"].append(element)

    portrayal["edges"] = [
        {"id": edge_id, "source": source, "target": target, "color": "#000000"}
        for edge_id, (source, target) in enumerate(G.edges)
    ]

    return portrayal


grid = NetworkModule(network_portrayal, 500, 500, library="sigma")
# chart = ChartModule(
#     [{"Label": "Gini", "Color": "Black"}], data_collector_name="datacollector"
# )



# def market_portrayal(cell):
#     if cell is None:
#         return
#     portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
#     (x, y) = cell.pos
#     portrayal["x"] = x
#     portrayal["y"] = y
#     portrayal["Color"] = COLORS[cell.agent_type]
#     return portrayal

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "N": UserSettableParameter("slider", "Numero vucumprà", 10, 1, 20, 1),
    "M": UserSettableParameter("slider", "Numero compratori", 10, 1, 30, 1),
}
server = ModularServer(
    Mercato, [grid], "Mercato", model_params
)