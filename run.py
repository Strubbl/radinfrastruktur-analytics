import osmnx as ox
import networkx as nx
import csv

class OsmCalc():
    def getBike(self, place):
        useful_tags = ox.settings.useful_tags_way + ['cycleway'] + ['bicycle'] + ['oneway'] + ['bicycle:lanes'] + ['cycleway:right'] + ['cycleway:left'] + ['bicycle_road']
        ox.utils.config(use_cache=True, log_console=True, useful_tags_way=useful_tags)
        G = ox.graph_from_place(query=place, network_type='bike', simplify=False,  retain_all=True)
        attributes = []

        non_cyc = []
        for u,v,k,d in G.edges(keys=True, data=True):
            for a in d:
                name=str(a)+": "+str(d[a])
                excluded = ['osmid', 'ref', 'length', 'width', 'name']
                if a in excluded:
                    pass
                elif name not in attributes:
                    attributes.append(name)
            
            bi = False
            if "bicycle" in d:
                if d['bicycle']=='designated' or d['bicycle']=='official' or d['bicycle']=='track' or d['bicycle']=='use_sidepath':
                    bi = True
            if "bicycle:lanes" in d:
                if "designated" in d['bicycle:lanes']:
                    bi = True
                    
            if d['highway']=='cycleway':
                pass
            elif 'cycleway' in d and d['cycleway'] != "no" and d['cycleway'] != "opposite":
                pass
            elif 'cycleway:right' in d and d['cycleway:right'] != "no":
                pass
            elif 'cycleway:left' in d and d['cycleway:left'] != "no":
                pass
            elif 'bicycle_road' in d and d['bicycle_road'] == "yes":
                pass
            elif bi:
                pass
            else:
                non_cyc.append((u,v,k))

        G.remove_edges_from(non_cyc)
        G = ox.utils_graph.remove_isolated_nodes(G)
        try:
            G = ox.simplify_graph(G)
        except:
            pass
        attributes.sort()
        #print(attributes)
        return G

    def getCar(self,place):
        G = ox.graph_from_place(place, network_type='drive', retain_all=True, truncate_by_edge=True, simplify=False)
        return G

    def calcStats(self, G, city):
        gdf = ox.gdf_from_place(city)
        area = ox.project_gdf(gdf).unary_union.area
        stats = ox.stats.basic_stats(G, area=area)
        stat = {}
        stat["length_total"] = stats["edge_length_total"]
        stat["length_single"] = stats["street_length_total"]
        stat["length_average"] = stats["street_length_avg"]
        stat["length_density"] = stats["edge_density_km"]
        stat["intersection_density"] = stats["intersection_density_km"]
        return stat
    
    def plotG(self,G,colored=False, save=False, filepath=False):
        if colored:
            ec=[]
            for _,_,_, d in G.edges(keys=True, data=True):

                bi = False
                if "bicycle" in d:
                    if d['bicycle']=='designated' or d['bicycle']=='official' or d['bicycle']=='track' or d['bicycle']=='use_sidepath':
                        bi = True
                if "bicycle:lanes" in d:
                    if "designated" in d['bicycle:lanes']:
                        bi = True

                if d['highway']=='cycleway':
                    ec.append('#3366e6')
                elif 'cycleway' in d and d['cycleway'] != "no" and d['cycleway'] != "opposite":
                   ec.append('#3366e6')
                elif bi:
                    ec.append('#3366e6')
                elif 'cycleway:right' in d and d['cycleway:right'] != "no":
                    ec.append('#3366e6')
                elif 'cycleway:left' in d and d['cycleway:left'] != "no":
                    ec.append('#3366e6')
                elif 'bicycle_road' in d and d['bicycle_road'] == "yes":
                    ec.append('#3366e6')
                else:
                    ec.append('#d4d4d4')
            fig, ax = ox.plot_graph(G, edge_color=ec, save=save, show=True, filepath=filepath, node_color='#7d7d7d', edge_alpha=0.6, node_size=0, figsize=(37.5590551,18.7795276), dpi=1200, bgcolor="#FFFFFF", edge_linewidth=3)
        else:
            fig, ax = ox.plot_graph(G)
            
    def writeCsv(self, data):
        with open('cities.csv', 'a+') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                     quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(data)

cities=[{"city": "Hamburg"}]            
            
o = OsmCalc()

for city in cities:
    G_bike = o.getBike(city)
    G_car = o.getCar(city)
    G = nx.compose(G_car, G_bike)
    #o.writeCsv([str(city.split(",")[0])+" Bike"]+list(o.calcStats(G_bike, city).values()))
    #o.writeCsv([str(city.split(",")[0])+" Car"]+list(o.calcStats(G_car, city).values()))
    o.plotG(G, save=True, filepath=str(city.split(",")[0])+".png", colored=True)
