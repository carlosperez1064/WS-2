from flask import Flask, request, json, Response
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'


#app = Flask(__name__)

#Conexión
#conexion = "host='localhost' dbname='MediosTransporte' user='administrador' password='admin'"
#print("conectando...\n	->%s" % (conexion))

# Realizar la conexión a DB
#conn = psycopg2.connect(conexion)

mapa = nx.Graph() #Crear el grafo


def GrafoMapa():

#Agregar nodos al grafo con atributos
    mapa.add_node(1, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(2, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(3, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(4, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :True})
    mapa.add_node(5, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :True})
    mapa.add_node(6, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(7, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :True})
    mapa.add_node(8, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(9, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :False})
    mapa.add_node(10, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(11, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(12, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :False})
    mapa.add_node(13, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :False})
    mapa.add_node(14, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(15, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :False})
    mapa.add_node(16, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(17, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(18, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(19, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :True})
    mapa.add_node(20, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(21, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :True})
    mapa.add_node(22, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    mapa.add_node(23, {"Bus" : True, "Taxi" : True, "Tren" : True, "Avion" :False})
    mapa.add_node(24, {"Bus" : True, "Taxi" : True, "Tren" : False, "Avion" :False})
    print(mapa.nodes(data=True))

    # Lista de edges y pesos que será insertada (nodo origen, nodo destino, distancia en km)
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
             (20, 21, 13),
             (19, 4, 364),
             (19, 5, 505),
             (19, 7, 275),
             (24, 4, 286),
             (24, 5, 426),
             (24, 7, 196),
             (5, 4, 480),
             (5, 7, 391)]

    mapa.add_weighted_edges_from(lista) #Agregar los bordes con sus respectivos pesos
    nx.draw_networkx(mapa,with_labels=True) #Dibujar rutas del mapa (nodos conectados)
    plt.show()

def consultas(origen, destino, tipoTransporte):
    #origen = 19
    #destino = 20
    # tipoTransporte = 'Avion'

    # Determinar Rutas más cortas
    Grafo = nx.dijkstra_path(mapa, origen,destino) #Tomar parametros para determinar ruta corta (usa algoritmo Dijkstra)
    #plt.savefig("path.png")
    print (Grafo)

    #Determinar Rutas vecinas
    if mapa.node[origen][tipoTransporte] and mapa.node[destino][tipoTransporte]:
        print ("Viaje directo")
    else:
        vecinos= mapa.neighbors(destino)
        print (vecinos)
        for vecino in vecinos:
            if mapa.node[vecino][tipoTransporte]:
                print ("Viaje a ", vecino, " y luego en otro medio de transporte disponible")

    #elif mapa.node[origen]['Avion'] and mapa.neighbors(destino)[]



#if __name__ == '__main__':
    #app.run(port=8000, host='0.0.0.0')

GrafoMapa()
consultas(19,20,'Avion')

#CREATE TABLE tren (id integer, data json);
#INSERT INTO tren VALUES (12,'{"NombreCompania": "Inconfer","Ruta": {"Origen": "San Jose","Destino": "Cartago","Horario": "L-D"}}');
