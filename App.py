from flask import Flask, request, json, Response
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'


app = Flask(__name__)


 # Conexión
conexion = "host='localhost' dbname='MediosTransporte' user='administrador' password='admin'"

print("conectando...\n	->%s" % (conexion))

# Realizar la conexión a DB
conn = psycopg2.connect(conexion)


# Grapho
G= nx.Graph()

# "Mapeo", nodo origen, nodo destino, distancia en km
lista = [(19, 24, 148),
         (19, 6, 52),
         (24, 11, 74),
         (11, 6, 92),
         (11, 3, 112),
         (6, 8, 69),
         (6, 22, 235),
         (8, 16, 46),
         (22, 16, 179),
         (16, 9, 178),
         (16, 1, 69),
         (3, 1, 104),
         (3, 7, 160),
         (1, 9, 113),
         (7, 23, 43),
         (7, 2, 187),
         (7, 15, 103),
         (9, 23, 97),
         (9, 4, 87),
         (2, 13, 76),
         (2, 14, 61),
         (15, 23, 82),
         (15, 12, 19),
         (15, 13, 145),
         (23, 4, 121),
         (4, 10, 177),
         (4, 12, 156),
         (14, 18, 111),
         (14, 5, 149),
         (14, 13, 54),
         (13, 18, 60),
         (12, 18, 114),
         (12, 17, 61),
         (5, 20, 591),
         (18, 20, 274),
         (18, 17, 94),
         (17, 10, 190),
         (10, 21, 16),
         (20, 21, 13)]

G.add_weighted_edges_from(lista)
nx.draw_networkx(G,with_labels=True)
plt.show()

origen = 19
destino = 18
ilustracionGrafo = nx.dijkstra_path(G, origen,destino) #Tomar parametros para determinar ruta corta (usa algoritmo Dijkstra)
print (ilustracionGrafo)


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')