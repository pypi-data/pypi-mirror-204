
import sys
from PySide6.QtWidgets import QApplication
from QtGraphVisuals import quick_view 
from qt_material import apply_stylesheet
import networkx as nx

def graph1():
    G = nx.MultiDiGraph(name = 'graph_1')
    G.add_edges_from([(0,1), (1,2), (0,2)])
    return G

def graph2():
    G = nx.MultiDiGraph(name = 'graph_2')
    G.add_edges_from([(0,1), (0,1), (1,2), (2,3)])
    return G

def graph3():
    from tensorflow import keras
    #model = keras.applications.nasnet.NASNetMobile()
    model = keras.models.load_model("trim_nas.h5")
    return model

if __name__ == "__main__":

    quick_view({g.name:g for g in [graph1(), graph2(), graph3()]})
    #quick_view({g.name:g for g in [graph1(), graph2(), graph3()]})

