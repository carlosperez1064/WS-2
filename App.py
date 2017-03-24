from flask import Flask, request, json, Response
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

app = Flask(__name__)

mapa = nx.Graph()  # Crear el grafo


def conectarBaseDatos():

    conexion = "host='localhost' dbname='MediosTransporte' user='postgres' password='admin'"

    conn = psycopg2.connect(conexion)  # Realizar la conexión a DB
    print(conn)

def GrafoMapa():
    # Agregar nodos al grafo con atributos
    mapa.add_node(1, {"Nombre": "Volcan Arenal", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(2, {"Nombre": "Quepos", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(3, {"Nombre": "Las Juntas", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(4, {"Nombre": "Cariari Pococi", "Bus": True, "Uber": True, "Tren": False, "Avion": True})
    mapa.add_node(5, {"Nombre": "Puerto Jimenez", "Bus": True, "Uber": True, "Tren": False, "Avion": True})
    mapa.add_node(6, {"Nombre": "Volcan Rincon de la Vieja", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(7, {"Nombre": "Volcan Poas", "Bus": True, "Uber": True, "Tren": True, "Avion": True})
    mapa.add_node(8, {"Nombre": "Upala", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(9, {"Nombre": "Puerto Viejo Sarapiqui", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(10, {"Nombre": "Cahuita", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(11, {"Nombre": "Filadelfia", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(12, {"Nombre": "Volcan Turrialba", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(13, {"Nombre": "San isidro del General", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(14, {"Nombre": "Uvita", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(15, {"Nombre": "Volcan Irazu", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(16, {"Nombre": "Volcan Tenorio", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(17, {"Nombre": "Moravia", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(18, {"Nombre": "Cerro Chirripo", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(19, {"Nombre": "La Casona Santa Rosa", "Bus": True, "Uber": True, "Tren": False, "Avion": True})
    mapa.add_node(20, {"Nombre": "Bribri", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(21, {"Nombre": "Puerto Viejo Talamanca", "Bus": True, "Uber": True, "Tren": False, "Avion": True})
    mapa.add_node(22, {"Nombre": "Los Chiles", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    mapa.add_node(23, {"Nombre": "Volcan Barva", "Bus": True, "Uber": True, "Tren": True, "Avion": False})
    mapa.add_node(24, {"Nombre": "Santa Cruz", "Bus": True, "Uber": True, "Tren": False, "Avion": False})
    #print(mapa.nodes(data=True))

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
             (5, 4, 390),
             (5, 7, 400)]

    mapa.add_weighted_edges_from(lista)  # Agregar los bordes con sus respectivos pesos
    nx.draw_networkx(mapa, with_labels=True)  # Dibujar rutas del mapa (nodos conectados)
   # plt.show()


def obtengaElNombreDe(param):
    for nodo in mapa.node:
        if nodo == param:
            return (mapa.node[nodo]["Nombre"])


def medios(nodo1, nodo2, medio):
    if mapa.node[nodo1][medio] and mapa.node[nodo2][medio]:
        return True


@app.route('/api/viajando/consultas', methods=['POST'])
def consultas():
    # in_args = request.args  # Obtener todos los parámetros

    # elNodoDeOrigen = in_args['elNodoDeOrigen'] #Seleccionar parametro con clave elNodoDeOrigen
    # elNodoDeDestino = in_args['elNodoDeDestino'] #Seleccionar parametro con clave elNodoDeDestino
    # elTipoTransporte = in_args['elTipoTransporte'] #Seleccionar parametro con clave elTipoTransporte
    elNodoDeOrigen = 22
    elNodoDeDestino = 8
    elTipoTransporte = 'Tren'
    losVecinosDelNodoDestino = mapa.neighbors(elNodoDeDestino)
    losVecinosDelNodoOrigen = mapa.neighbors(elNodoDeOrigen)

    # Determinar si en los nodos vecinos al elNodoDeDestino final, existe un medio de transporte más rápido (avión o tren)
    # en cuyo caso, enviaría a la persona hasta ese nodo en cualquiera de esos dos medios de transporte, y luego al
    # nodo de elNodoDeDestino final en bus o en Uber.
    elNodoOrigenTieneTipoDeTransporte = mapa.node[elNodoDeOrigen][elTipoTransporte]
    elNodoDestinoTieneTipoDeTransporte = mapa.node[elNodoDeDestino][elTipoTransporte]
    if elTipoTransporte == 'Avion' or elTipoTransporte == 'Tren':
        if elNodoOrigenTieneTipoDeTransporte and elNodoDestinoTieneTipoDeTransporte:
            print("Viaje directo de ", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elNodoDeDestino), "en",
                  elTipoTransporte)
        else:
            if elNodoOrigenTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoDestino:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino), "en",
                              elTipoTransporte, "y luego a", obtengaElNombreDe(elNodoDeDestino),
                              "en bus o Uber")
            elif elNodoDestinoTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoOrigen:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino),
                              "en bus o Uber y luego de", obtengaElNombreDe(elVecino), "a",
                              obtengaElNombreDe(elNodoDeDestino),
                              "en avion")
            else:
                lasOpcionesCercanasAlNodoDeOrigen = []
                lasOpcionesCercanasAlNodoDeDestino = []
                for elVecinodeNodoOrigen in losVecinosDelNodoOrigen:
                    if mapa.node[elVecinodeNodoOrigen][elTipoTransporte]:
                        for elVecinodeNodoDestino in losVecinosDelNodoDestino:
                            if mapa.node[elVecinodeNodoDestino][elTipoTransporte]:
                                print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a",
                                      obtengaElNombreDe(elVecinodeNodoOrigen), "en bus o Uber, luego de",
                                      obtengaElNombreDe(elVecinodeNodoOrigen), "en avion a",
                                      obtengaElNombreDe(elVecinodeNodoDestino), "y por ultimo en bus o Uber a",
                                      obtengaElNombreDe(elNodoDeDestino))
                else:
                    rutaCorta = nx.dijkstra_path(mapa, elNodoDeOrigen,elNodoDeDestino) #Tomar parametros para determinar ruta corta (usa algoritmo Dijkstra)
                    print("Solo puede ir en bus o Uber, la ruta mas corta es pasando por: ")
                    for elNodoRuta in rutaCorta:
                        nombresDeNodos = obtengaElNombreDe(elNodoRuta)
                        print(nombresDeNodos)


# if __name__ == '__main__':
# app.run(port=8000, host='0.0.0.0')


#conectarBaseDatos()
GrafoMapa()
consultas()
# nombres()

# CREATE TABLE tren (id integer, data json);
# INSERT INTO tren VALUES (12,'{"NombreCompania": "Inconfer","Ruta": {"Origen": "San Jose","Destino": "Cartago","Horario": "L-D"}}');
