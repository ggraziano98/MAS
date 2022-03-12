#! python
import logging 

logging.basicConfig()

from model.server import server

print('SERVER STARTING')

server.launch()

print('SERVER STOPPED')