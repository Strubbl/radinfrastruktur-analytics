import pandas as p
import os
import matplotlib.pylab as plt
import numpy as np

os.chdir("C:/github_repos/Radinfrastruktur-analytics")

class Plotter():

    def plotBar(self, x, y, title, color=(0.2,0.4,0.9,1), plot_y=False, line_width=1, rotate_x=False, fully_rotate_x=False, margin=0.5, height_scale=1.1):
        fig = plt.figure(figsize=(1.1*6.25984252,height_scale*3.12992126))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.axhline(np.mean(y), color='black', linewidth=1.4)
        plt.bar(x, y, line_width, color=color)
        ax1.grid(which='major', axis='y', linewidth=0.71, linestyle='-', color='0.75')
        ax1.set_axisbelow(True)
        plt.title(title)
        if plot_y is not False:
            h=plt.ylabel(plot_y)
        fig.tight_layout()
        if rotate_x:
            plt.xticks(rotation=45, ha="right")
            plt.subplots_adjust(bottom=margin)
        if fully_rotate_x:
            plt.xticks(rotation=90, ha="center")
            plt.subplots_adjust(bottom=margin)
        plt.show()

pl = Plotter()

class Reader():
    def __init__(self, filename):
        self.data=p.read_csv(filename, sep=";")
        print(self.data)

    def getCities(self):
        cities_for = [{'city': 'Barcelona', 'state': 'Catalonia', 'country': 'Spain'},
             {'city': 'Utrecht', 'country': 'Netherlands'},
              {'city': 'Antwerpen', 'country': 'Belgien'},
              {'city': 'Montreal', 'country': 'Canada'},
              {'city': 'New York City', 'country': 'USA'}
             ]
        cities_bike=[{'city': 'Karlsruhe', 'country': 'Deutschland'},
            {'city': 'Münster', 'country': 'Deutschland'},
                {'city': 'Erlangen', 'country': 'Deutschland'},
                {'city': 'Freiburg im Breisgau', 'country': 'Deutschland'},
                {'city': 'Heidelberg', 'country': 'Deutschland'},
                {'city': 'Kiel', 'country': 'Deutschland'},
                {'city': 'Greifswald', 'country': 'Deutschland'},
                {'city': 'München', 'country': 'Deutschland'},
                {'city': 'Bonn', 'country': 'Deutschland'}
            ]     
        cities_stand = [
            {'city': 'Stuttgart', 'country': 'Deutschland'},
            {'city': 'Berlin', 'country': 'Deutschland'},
            {'city': 'Hamburg', 'country': 'Deutschland'},
            {'city': 'Leipzig', 'country': 'Deutschland'},
            {'city': 'Bremen', 'country': 'Deutschland'},
            {'city': 'Dresden', 'country': 'Deutschland'},
            {'city': 'Düsseldorf', 'country': 'Deutschland'},
            {'city': 'Erfurt', 'country': 'Deutschland'},
            {'city': 'Hannover', 'country': 'Deutschland'},
            {'city': 'Magdeburg', 'country': 'Deutschland'},
            {'city': 'Mainz', 'country': 'Deutschland'},
            {'city': 'Potsdam', 'country': 'Deutschland'},
            {'city': 'Saarbrücken', 'country': 'Deutschland'},
            {'city': 'Schwerin', 'country': 'Deutschland'},
            {'city': 'Wiesbaden', 'country': 'Deutschland'}
        ]

        c_foreign=[]
        c_bike=[]
        c_standard=[]
        for c in cities_for:
            c_foreign.append(c["city"])
        for c in cities_bike:
            c_bike.append(c["city"])
        for c in cities_stand:
            c_standard.append(c["city"])

        return c_foreign, c_bike, c_standard

    def calcFeatures(self, bike, car):
        ret={}
        try:
            ret["r_total"]=float(bike["Länge total in m"])/float(car["Länge total in m"])
            ret["r_single"]=float(bike["Länge einzeln in m"])/float(car["Länge einzeln in m"])
            ret["r_avrg"]=float(bike["Durchschn. Strassenlänge in m"])/float(car["Durchschn. Strassenlänge in m"])
        except:
            print(bike)
            print(car)

        return ret

    def getData(self):
        cf, cb, cs = self.getCities()
        y_1 = {}
        y_2 = {}
        y_3 = {}
        for city in cf+cb+cs:
            bike = self.data.loc[self.data['Stadt'] == city+", Bike"]
            car = self.data.loc[self.data['Stadt'] == city+", Car"]
            ret = self.calcFeatures(bike, car)
            y_1[city] = ret["r_total"]
            y_2[city] = ret["r_single"]
            y_3[city] = ret["r_avrg"]

        return y_1, y_2, y_3, self.data

r = Reader("data/cities.csv")

class Statistics():
    def byEdgelength(self):
        y1, y2, y3, _ = r.getData()
        cf, cb, cs = r.getCities()

        colors = []
        y1={k: v for k, v in sorted(y1.items(), key=lambda item: item[1])}
        for key in y1:
            if key in cf:
                colors.append((0.9,0.6,0,1))
            elif key in cb:
                colors.append((0.2,0.4,0.9,1))
            elif key in cs:
                colors.append((0,0.7,0.1,1))
            else:
                colors.append((1,1,1,1))
        pl.plotBar(y1.keys(),list(y1.values()), "Verhältnis der Kantenlänge - Rad zu Auto", plot_y="r_total [-]", rotate_x=True, color=colors, line_width=0.8, margin=0.4)

        colors = []
        y2={k: v for k, v in sorted(y2.items(), key=lambda item: item[1])}
        for key in y2:
            if key in cf:
                colors.append((0.9,0.6,0,1))
            elif key in cb:
                colors.append((0.2,0.4,0.9,1))
            elif key in cs:
                colors.append((0,0.7,0.1,1))
            else:
                colors.append((1,1,1,1))
        pl.plotBar(y2.keys(),list(y2.values()), "Verhältnis der Strassenlänge - Rad zu Auto", plot_y="r_single [-]", rotate_x=True, color=colors, line_width=0.8, margin=0.4)

        colors = []
        y3={k: v for k, v in sorted(y3.items(), key=lambda item: item[1])}
        for key in y3:
            if key in cf:
                colors.append((0.9,0.6,0,1))
            elif key in cb:
                colors.append((0.2,0.4,0.9,1))
            elif key in cs:
                colors.append((0,0.7,0.1,1))
            else:
                colors.append((1,1,1,1))
        pl.plotBar(y3.keys(),list(y3.values()), "Verhältnis der durchschn. Strassenlänge - Rad zu Auto", plot_y="r_avrg [-]", rotate_x=True, color=colors, line_width=0.8, margin=0.4)

s = Statistics()
s.byEdgelength()


