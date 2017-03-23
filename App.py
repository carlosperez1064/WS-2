from flask import Flask, request, json, Response
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

app = Flask(__name__)

mapa = nx.Graph()  # Crear el grafo


def conectarBaseDatos():
    conexion = "host='localhost' dbname='MediosTransporte' user='administrador' password='admin'"
    print("conectando...\n	->%s" % (conexion))

    conn = psycopg2.connect(conexion)  # Realizar la conexión a DB


def GrafoMapa():
    # Agregar nodos al grafo con atributos
    mapa.add_node(1, {"Nombre": "Volcan Arenal", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(2, {"Nombre": "Quepos", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(3, {"Nombre": "Las Juntas", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(4, {"Nombre": "Cariari Pococi", "Bus": True, "Taxi": True, "Tren": False, "Avion": True})
    mapa.add_node(5, {"Nombre": "Puerto Jimenez", "Bus": True, "Taxi": True, "Tren": False, "Avion": True})
    mapa.add_node(6, {"Nombre": "Volcan Rincon de la Vieja", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(7, {"Nombre": "Volcan Poas", "Bus": True, "Taxi": True, "Tren": True, "Avion": True})
    mapa.add_node(8, {"Nombre": "Upala", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(9, {"Nombre": "Puerto Viejo Sarapiqui", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(10, {"Nombre": "Cahuita", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(11, {"Nombre": "Filadelfia", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(12, {"Nombre": "Volcan Turrialba", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(13, {"Nombre": "San isidro del General", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(14, {"Nombre": "Uvita", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(15, {"Nombre": "Volcan Irazu", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(16, {"Nombre": "Volcan Tenorio", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(17, {"Nombre": "Moravia", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(18, {"Nombre": "Cerro Chirripo", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(19, {"Nombre": "La Casona Santa Rosa", "Bus": True, "Taxi": True, "Tren": False, "Avion": True})
    mapa.add_node(20, {"Nombre": "Bribri", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(21, {"Nombre": "Puerto Viejo Talamanca", "Bus": True, "Taxi": True, "Tren": False, "Avion": True})
    mapa.add_node(22, {"Nombre": "Los Chiles", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    mapa.add_node(23, {"Nombre": "Volcan Barva", "Bus": True, "Taxi": True, "Tren": True, "Avion": False})
    mapa.add_node(24, {"Nombre": "Santa Cruz", "Bus": True, "Taxi": True, "Tren": False, "Avion": False})
    print(mapa.nodes(data=True))

    # Lista de edges y pesos que será insertada (nodo origen, nodo destino, distancia en km)
    lista = [(19, 24, 60),
             (19, 6, 40),
             (19, 11, 50),
             (24, 11, 74),
             (11, 6, 92),
             (11, 3, 112),
             (6, 8, 69),
             (6, 22, 60),
             (8, 16, 46),
             (22, 16, 70),
             (16, 9, 120),
             (16, 1, 69),
             (3, 1, 30),
             (3, 7, 60),
             (1, 9, 90),
             (7, 23, 43),
             (7, 2, 107),
             (7, 15, 40),
             (9, 23, 50),
             (9, 4, 87),
             (2, 13, 60),
             (2, 14, 61),
             (15, 23, 30),
             (15, 12, 10),
             (15, 13, 32),
             (23, 4, 70),
             (4, 10, 120),
             (4, 12, 80),
             (14, 18, 70),
             (14, 5, 90),
             (14, 13, 55),
             (13, 18, 20),
             (12, 18, 60),
             (12, 17, 61),
             (5, 20, 180),
             (18, 20, 50),
             (18, 17, 40),
             (17, 10, 20),
             (10, 21, 16),
             (20, 21, 13),
             (19, 4, 300),
             (19, 5, 500),
             (19, 7, 275),
             (24, 4, 260),
             (24, 5, 420),
             (24, 7, 190),
             (5, 4, 390),
             (5, 7, 400)]

    mapa.add_weighted_edges_from(lista)  # Agregar los bordes con sus respectivos pesos
    nx.draw_networkx(mapa, with_labels=True)  # Dibujar rutas del mapa (nodos conectados)
    plt.show()


def nombres(param):
    for nodo in mapa.node:
        if nodo == param:
            return (mapa.node[nodo]["Nombre"])


def medios(nodo1, nodo2, medio):
    if mapa.node[nodo1][medio] and mapa.node[nodo2][medio]:
        return True


@app.route('/api/viajando/consultas', methods=['POST'])
def consultas():
    # in_args = request.args  # Obtener todos los parámetros

    # origen = in_args['origen'] #Seleccionar parametro con clave origen
    # destino = in_args['destino'] #Seleccionar parametro con clave destino
    # tipoTransporte = in_args['tipoTransporte'] #Seleccionar parametro con clave tipoTransporte
    origen = 19
    destino = 10
    tipoTransporte = 'Avion'
    vecinosO = mapa.neighbors(origen)
    vecinosD = mapa.neighbors(destino)

    # Determinar Rutas más cortas
    # Grafo = nx.dijkstra_path(mapa, origen,destino) #Tomar parametros para determinar ruta corta (usa algoritmo Dijkstra)
    # plt.savefig("path.png")
    # print (Grafo)

    # Determinar si en los nodos vecinos al destino final, existe un medio de transporte más rápido (avión o tren)
    # en cuyo caso, enviaría a la persona hasta ese nodo en cualquiera de esos dos medios de transporte, y luego al
    # nodo de destino final en bus o en taxi.

    if tipoTransporte == 'Avion' or tipoTransporte == 'Tren':
        if mapa.node[origen][tipoTransporte] and mapa.node[destino][tipoTransporte]:
            print("Viaje directo de ", nombres(origen), "a", nombres(destino), "en", tipoTransporte)
        else:
            if mapa.node[origen][tipoTransporte]:
                for vecino in vecinosD:
                    if mapa.node[vecino][tipoTransporte]:
                        print("Viaje de", origen, "a", vecino, "en", tipoTransporte, "y luego a", destino,
                              "en bus o taxi")
            elif mapa.node[destino][tipoTransporte]:
                for vecino in vecinosO:
                    if mapa.node[vecino][tipoTransporte]:
                        print("Viaje de", origen, "a", vecino, "en bus o taxi", "y luego de", vecino, "a", destino,
                              "en avion")
            else:
                


# if __name__ == '__main__':
# app.run(port=8000, host='0.0.0.0')


# conectarBaseDatos()
GrafoMapa()
consultas()
# nombres()

# CREATE TABLE tren (id integer, data json);
# INSERT INTO tren VALUES (12,'{"NombreCompania": "Inconfer","Ruta": {"Origen": "San Jose","Destino": "Cartago","Horario": "L-D"}}');
