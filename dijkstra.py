from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import sys
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
from functools import reduce
import math

class Vertice:
    def __init__(self, i, j):
        self.id = i
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.costo = float('inf')
        self.pos = j

    def agregarVecino(self, v, p):
        if v not in self.vecinos:
            self.vecinos.append([v, p])

class Grafica:
    def __init__(self):
        self.vertices = {}

    def agregarVertice(self, id, pos):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id, pos)

    def agregarArista(self, a, b, p):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecino(b, p)
            self.vertices[b].agregarVecino(a, p)

    def imprimirGrafica(self):
        for v in self.vertices:
            print("El costo del vértice " + str(self.vertices[v].id) + " es " + str(
                self.vertices[v].costo) + " llegando desde " + str(self.vertices[v].padre))

    def camino(self, b):
        camino = []
        actual = b
        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        return [camino, self.vertices[b].costo]

    def minimo(self, l):
        if len(l) > 0:
            m = self.vertices[l[0]].costo
            v = l[0]
            for e in l:
                if m > self.vertices[e].costo:
                    m = self.vertices[e].costo
                    v = e
            return v
        return None

    def dijkstra(self, a):
        if a in self.vertices:

            self.vertices[a].costo = 0
            actual = a
            noVisitados = []

            for v in self.vertices:
                if v != a:
                    self.vertices[v].costo = float('inf')
                self.vertices[v].padre = None
                noVisitados.append(v)

            while len(noVisitados) > 0:

                for vec in self.vertices[actual].vecinos:
                    if self.vertices[vec[0]].visitado == False:

                        if self.vertices[actual].costo + vec[1] < self.vertices[vec[0]].costo:
                            self.vertices[vec[0]].costo = self.vertices[actual].costo + vec[1]
                            self.vertices[vec[0]].padre = actual

                self.vertices[actual].visitado = True
                noVisitados.remove(actual)

                actual = self.minimo(noVisitados)
        else:
            return False

def nudge(pos, x_shift, y_shift):
    return {n: (x - x_shift, y - y_shift) for n, (x, y) in pos.items()}

def draw():
    a.cla()
    pos = nx.get_node_attributes(G, 'pos')
    pos_nodes = nudge(pos, 0, 5)
    nx.draw(G, pos=pos, node_color='#6f30a0', edge_color='#6f30a0', node_size=30, with_labels=False)
    nx.draw_networkx_labels(G, pos=pos_nodes)
    plt.axis('off')
    a.set_xlim(0, 100)
    a.set_ylim(0, 100)
    plt.tight_layout(pad=0.0,h_pad=0.0,w_pad=0.0)
    canvas.draw()

def eleccion_vertice(o1, o2):
    pop_1.destroy()
    g.agregarVertice(o1,tuple(map(int, o2.split(','))))
    G.add_node(o1, pos=tuple(map(int, o2.split(','))))
    draw()

def eleccion_arista(o1, o2):
    pop_2.destroy()
    dist = math.hypot(g.vertices[o1].pos[0] - g.vertices[o2].pos[0], g.vertices[o1].pos[1] - g.vertices[o2].pos[1])
    g.agregarArista(o1, o2, dist)
    G.add_edge(o1, o2)
    draw()

def eleccion_ruta(o1, o2):
    pop_3.destroy()
    g.dijkstra(o1)
    ruta = g.camino(o2)
    path = ruta[0]

    a.cla()

    for e in G.edges():
        G[e[0]][e[1]]['color'] = '#6f30a0'

    for i in range(len(path) - 1):
        G[path[i]][path[i + 1]]['color'] = 'red'

    edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]

    pos = nx.get_node_attributes(G, 'pos')
    pos_nodes = nudge(pos, 0, 5)
    nx.draw(G, pos=pos, node_color='#6f30a0', edge_color=edge_color_list, node_size=30, with_labels=False)
    nx.draw_networkx_labels(G, pos=pos_nodes)

    plt.axis('off')
    a.set_xlim(0, 100)
    a.set_ylim(0, 100)
    plt.tight_layout(pad=0.0,h_pad=0.0,w_pad=0.0)
    canvas.draw()

def crear_vertice():
    global pop_1
    pop_1 = Toplevel(root)
    pop_1.wm_title("")
    pop_1.geometry("180x75")
    pop_1.config(bg="#00b0f0")

    pop_label = Label(pop_1, text="Nombre del nuevo vértice", bg="#00b0f0")
    pop_label.grid(row=0, column = 0)
    pop_entry = Entry(pop_1, width=5)
    pop_entry.grid(row=0, column=1)

    p_l = Label(pop_1, text="Posición", bg="#00b0f0")
    p_l.grid(row=1, column = 0)
    p_e = Entry(pop_1, width=5)
    p_e.grid(row=1, column=1)

    my_frame = Frame(pop_1, bg="#00b0f0")
    my_frame.grid(pady=5)

    yes = Button(my_frame, text="Aceptar", command=lambda: eleccion_vertice(pop_entry.get(), p_e.get()))
    yes.grid( padx=10)

def crear_arista():
    global pop_2
    pop_2 = Toplevel(root)
    pop_2.wm_title("")
    pop_2.geometry("180x75")
    pop_2.config(bg="#00b0f0")
    pop_label = Label(pop_2, text="Vértice inicial", bg="#00b0f0")
    pop_label.grid(row=0, column = 0)
    pop_entry = Entry(pop_2, width=5)
    pop_entry.grid(row=0, column=1)

    p_l = Label(pop_2, text="Vértice final", bg="#00b0f0")
    p_l.grid(row=1, column = 0)
    p_e = Entry(pop_2, width=5)
    p_e.grid(row=1, column=1)

    my_frame = Frame(pop_2, bg="#00b0f0")
    my_frame.grid(pady=5)

    yes = Button(my_frame, text="Aceptar", command=lambda: eleccion_arista(pop_entry.get(), p_e.get()))
    yes.grid( padx=10)

def mejor_ruta():
    global pop_3
    pop_3 = Toplevel(root)
    pop_3.wm_title("")
    pop_3.geometry("180x75")
    pop_3.config(bg="#00b0f0")
    pop_label = Label(pop_3, text="Vértice inicial", bg="#00b0f0")
    pop_label.grid(row=0, column = 0)
    pop_entry = Entry(pop_3, width=5)
    pop_entry.grid(row=0, column=1)

    p_l = Label(pop_3, text="Vértice final", bg="#00b0f0")
    p_l.grid(row=1, column = 0)
    p_e = Entry(pop_3, width=5)
    p_e.grid(row=1, column=1)

    my_frame = Frame(pop_3, bg="#00b0f0")
    my_frame.grid(pady=5)

    yes = Button(my_frame, text="Aceptar", command=lambda: eleccion_ruta(pop_entry.get(), p_e.get()))
    yes.grid( padx=10)


if __name__ == '__main__':
    g = Grafica()

    root = Tk()
    root.wm_title("")
    root.geometry("705x450")
    root.config(bg="#00b0f0")

    G = nx.Graph()

    f = plt.figure(figsize=(5, 4))
    a = f.add_subplot(111)

    B1 = Button(root, text="Crear vértice",width = 15, command=crear_vertice)
    B1.pack(pady=50)
    B1.place(x=25, y=25)
    B2 = Button(root, text="Crear arista",width = 15, command=crear_arista)
    B2.place(x=25, y=75)
    B3 = Button(root, text="Calcular mejor ruta",width = 15, command=mejor_ruta)
    B3.place(x=25, y=125)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=175, y=25)
    plt.axis('off')

    root.mainloop()