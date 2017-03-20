from flask import Flask, request, json, Response
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'


#app = Flask(__name__)


 # Conexión
#conexion = "host='localhost' dbname='MediosTransporte' user='administrador' password='admin'"

#print("conectando...\n	->%s" % (conexion))

# Realizar la conexión a DB
#conn = psycopg2.connect(conexion)

  #para consultas a BD
  #  cursor = conn.cursor()
   # print ("Connected!\n")


#if __name__ == '__main__':
 #   app.run(port=8000, host='0.0.0.0')

# Grapho
G= nx.Graph();
G.add_nodes_from({1,24})
G.
lista=[(19,24,8),
       (19,6,3),
       (24,11,2),
       (11,6,5),
       (11,3,5),
       (6,8,3),
       (6,22,5),
       (8,16,1),
       (22,16,3),
       (16,9,9),
       (16,1,2),
       (3,1,1),
       (3,7,6),
       (1,9,8),
       (7,23,2),
       (7,2,9),
       (7,15,5),
       (9,23,3),
       (9,4,5),
       (2,13,3),
       (2,14,7),
       (15,23,2),
       (15,12,1),
       (15,13,6),
       (23,4,7),
       (4,10,11),
       (4,12,7),
       (14,8,3),
       (14,5,9),
       (14,13,2),
       (13,18,2),
       (12,8,4),
       (12,17,8),
       (5,20,11),
       (8,20,4),
       (8,17,2),
       (17,10,5),
       (10,21,2),
       (20,21,3)]
G.add_weighted_edges_from(lista)
#nx.draw_networkx(G,with_labels=True)
#plt.show()
print (nx.dijkstra_path(G, 19,18))