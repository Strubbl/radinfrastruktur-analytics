import csv
import datetime
import networkx as nx
import os
import osmnx as ox
import sys

from run import OsmCalc

curr_date = datetime.date.today().strftime("%Y-%m-%d")
o = OsmCalc()
city = sys.argv[1]
filename = "images" + os.sep + "München-Bezirke" + os.sep + city.replace(" ", "_") + "_" + curr_date
print(filename)
G_bike = o.getBike(city)
G_car = o.getCar(city)
G = nx.compose(G_car, G_bike)
o.writeCsv([city + " Bike"]+list(o.calcStats(G_bike, city).values()), "cities_" + curr_date + ".csv")
o.writeCsv([city + " Car"]+list(o.calcStats(G_car, city).values()), "cities_" + curr_date + ".csv")
o.plotG(G, save=True, filepath=filename+".png", colored=True)

