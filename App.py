from flask import Flask, request, json, Response, jsonify
import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import re, string
from flask import render_template
#from flask-HTTPBasicAuthttpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

app = Flask(__name__)
mapa = nx.Graph()  # Crear el grafo
auth = HTTPBasicAuth()


# ---------------------------------------------- CONECTAR A BASE DE DATOS ----------------------------------------------#
#conexion = "host='localhost' dbname='MediosTransporte' user='postgres' password='admin'"
#conn = psycopg2.connect(conexion)
#cursor = conn.cursor()

@app.route('/formulario')
def formulario():
    return render_template('/login.html')


@app.route('/registro', methods=['POST'])
def registro():
    usuario =  request.form['usuario']
    contrasena = request.form['contrasena']
    return json.dumps({'status':'OK','usuario':usuario,'contrasena':contrasena})

# ---------------- MÉTODO PARA AGREGAR NODOS CON ATRIBUTOS AL GRAFO Y LISTA CON RELACIONES Y DISTANCIAS ----------------#
def GrafoMapa():
    # Agregar nodos al grafo con atributos
    mapa.add_node(1, {"Nombre": "Volcan Arenal", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(2, {"Nombre": "Quepos", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(3, {"Nombre": "Las Juntas", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(4, {"Nombre": "Cariari Pococi", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": True})
    mapa.add_node(5, {"Nombre": "Puerto Jimenez", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": True})
    mapa.add_node(6, {"Nombre": "Volcan Rincon de la Vieja", "zona": "A", "bus": True, "taxi": True, "tren": False,
                      "avion": False})
    mapa.add_node(7, {"Nombre": "San Jose", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": True})
    mapa.add_node(8, {"Nombre": "Upala", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(9, {"Nombre": "Puerto Viejo Sarapiqui", "zona": "B", "bus": True, "taxi": True, "tren": False,
                      "avion": False})
    mapa.add_node(10, {"Nombre": "Cahuita", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(11, {"Nombre": "Filadelfia", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(12,
                  {"Nombre": "Volcan Turrialba", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(13, {"Nombre": "San isidro del General", "zona": "C", "bus": True, "taxi": True, "tren": True,
                       "avion": False})
    mapa.add_node(14, {"Nombre": "Uvita", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(15, {"Nombre": "Volcan Irazu", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(16,
                  {"Nombre": "Volcan Tenorio", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(17, {"Nombre": "Moravia", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(18,
                  {"Nombre": "Cerro Chirripo", "zona": "C", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(19, {"Nombre": "La Casona Santa Rosa", "zona": "A", "bus": True, "taxi": True, "tren": False,
                       "avion": True})
    mapa.add_node(20, {"Nombre": "Bribri", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(21, {"Nombre": "Puerto Viejo Talamanca", "zona": "C", "bus": True, "taxi": True, "tren": False,
                       "avion": True})
    mapa.add_node(22, {"Nombre": "Los Chiles", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})
    mapa.add_node(23, {"Nombre": "Volcan Barva", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": False})
    mapa.add_node(24, {"Nombre": "Santa Cruz", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})

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
             (20, 21, 13)]

    mapa.add_weighted_edges_from(lista)  # Agregar los bordes con sus respectivos pesos
    #nx.draw_networkx(mapa, with_labels=True)  # Dibujar rutas del mapa (nodos conectados)
    # plt.show()


# -------------------------------------- MÉTODO PARA OBTENER NOMBRES DE LOS NODOS --------------------------------------#
def obtengaElNombreDe(param):
    for nodo in mapa.node:
        if nodo == param:
            return (mapa.node[nodo]["Nombre"])


# ---------------------------------------- MÉTODO PARA OBTENER ZONAS DE LOS NODOS --------------------------------------#
def obtengaLaZonaDe(param):
    for nodo in mapa.node:
        if nodo == param:
            return (mapa.node[nodo]["zona"])


# --------------------------- MÉTODO PARA REALIZA DETERMINAR MEDIOS DE TRANSPORTE DISPONIBLES --------------------------#
@app.route('/api/viajando/consultas', methods=['POST'])
def consulteMediosDeTransporte():
    # in_args = request.args  # Obtener todos los parámetros

    # elNodoDeOrigen = in_args['elNodoDeOrigen'] #Seleccionar parametro con clave elNodoDeOrigen
    # elNodoDeDestino = in_args['elNodoDeDestino'] #Seleccionar parametro con clave elNodoDeDestino
    # elTipoTransporte = in_args['elTipoTransporte'] #Seleccionar parametro con clave elTipoTransporte

    elNodoDeOrigen = 19
    elNodoDeDestino = 21
    elTipoTransporte = 'taxi'

    losVecinosDelNodoDestino = mapa.neighbors(elNodoDeDestino)
    losVecinosDelNodoOrigen = mapa.neighbors(elNodoDeOrigen)

    # Determinar si en los nodos vecinos al elNodoDeDestino final, existe un medio de transporte más rápido (avión o tren)
    # en cuyo caso, enviaría a la persona hasta ese nodo en cualquiera de esos dos medios de transporte, y luego al
    # nodo de elNodoDeDestino final en bus o en taxi.
    elNodoOrigenTieneTipoDeTransporte = mapa.node[elNodoDeOrigen][elTipoTransporte]
    elNodoDestinoTieneTipoDeTransporte = mapa.node[elNodoDeDestino][elTipoTransporte]

    # --------------------------- AVIONES Y TRENES --------------------------#

    if elTipoTransporte == 'avion' or elTipoTransporte == 'tren':
        if elNodoOrigenTieneTipoDeTransporte and elNodoDestinoTieneTipoDeTransporte:
            print("Viaje directo de ", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elNodoDeDestino),
                  "en", elTipoTransporte)
            if elTipoTransporte == 'tren':
                lasEstaciones = consulteTrenes(elNodoDeOrigen, elNodoDeDestino)
                print(lasEstaciones)
        else:
            if elNodoOrigenTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoDestino:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino), "en",
                              elTipoTransporte, "y luego a", obtengaElNombreDe(elNodoDeDestino),
                              "en bus o taxi")
                        if elTipoTransporte == 'tren':
                            lasEstaciones = consulteTrenes(elNodoDeOrigen, elVecino)
                            print(lasEstaciones)
            elif elNodoDestinoTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoOrigen:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino),
                              "en bus o taxi y luego de", obtengaElNombreDe(elVecino), "a",
                              obtengaElNombreDe(elNodoDeDestino),
                              "en", elTipoTransporte)
                        if elTipoTransporte == 'tren':
                            lasEstaciones = consulteTrenes(elVecino, elNodoDeDestino)
                            print(lasEstaciones)
            else:
                for elVecinodeNodoOrigen in losVecinosDelNodoOrigen:
                    if mapa.node[elVecinodeNodoOrigen][elTipoTransporte]:
                        for elVecinodeNodoDestino in losVecinosDelNodoDestino:
                            if mapa.node[elVecinodeNodoDestino][elTipoTransporte]:
                                print("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a",
                                      obtengaElNombreDe(elVecinodeNodoOrigen), "en bus o taxi, luego de",
                                      obtengaElNombreDe(elVecinodeNodoOrigen), "en", elTipoTransporte, "a",
                                      obtengaElNombreDe(elVecinodeNodoDestino), "y por ultimo en bus o taxi a",
                                      obtengaElNombreDe(elNodoDeDestino))
                                if elTipoTransporte == 'tren':
                                    print(elVecinodeNodoOrigen, elVecinodeNodoDestino)
                                    lasEstaciones = consulteTrenes(elVecinodeNodoOrigen, elVecinodeNodoDestino)
                                    print(lasEstaciones)
                            else:
                                print("Imposible ir en Avión o Tren, verifique en Bus o Taxi")


    # --------------------------- TAXIS --------------------------#
    # Tomar parametros para determinar ruta corta (usa algoritmo Dijkstra)
    elif elTipoTransporte=='taxi':
        laRutaCorta = nx.dijkstra_path(mapa, elNodoDeOrigen, elNodoDeDestino)
        print("La ruta mas corta es pasando por: ")
        for elNodoRuta in laRutaCorta:
            losNombresDeLosNodos = obtengaElNombreDe(elNodoRuta)
            print(losNombresDeLosNodos)
        zonaOrigen = obtengaLaZonaDe(elNodoDeOrigen)
        facturacion(600, elNodoDeOrigen, elNodoDeDestino)
        # --------------------------- TAXIS --------------------------#

        # Se obtiene la zona desde donde se requiere el servicio (origen) para ofrecer un taxi que opere en dicha zona



    #if elTipoTransporte == 'taxi':

        #if zonaOrigen == 'A':
            #print("--- Estos son los ID de los taxis cercanos a " + obtengaElNombreDe(elNodoDeOrigen))
            #cursor.execute(
                #"""SELECT "ID","Informacion" ->> 'Zona' AS Zona FROM public."Uber" WHERE "Informacion" ->> 'Zona' = 'A';""")
            #rows = cursor.fetchall()
            #for row in rows:
                #print("   ", row)

        #if zonaOrigen == 'B':
            #print("--- Estos son los ID de los taxis cercanos a " + obtengaElNombreDe(elNodoDeOrigen))
            #cursor.execute(
                #"""SELECT "ID","Informacion" ->> 'Zona' AS Zona FROM public."Uber" WHERE "Informacion" ->> 'Zona' = 'B';""")
            #rows = cursor.fetchall()
            #for row in rows:
                #print("   ", row)

        #if zonaOrigen == 'C':
            #print("--- Estos son los ID de los taxis cercanos a " + obtengaElNombreDe(elNodoDeOrigen))
            #cursor.execute(
                #"""SELECT "ID","Informacion" ->> 'Zona' AS Zona FROM public."Uber" WHERE "Informacion" ->> 'Zona' = 'C';""")
            #rows = cursor.fetchall()
            #for row in rows:
                #print("   ", row)
    # --------------------------- BUSES --------------------------#

    if elTipoTransporte == 'bus':
        consulteBuses(elNodoDeOrigen, elNodoDeDestino)
        facturacion(20, elNodoDeOrigen, elNodoDeDestino)

        # Cada asiento debería ser un botoncito, que se puede tocar un sola vez, al tocarse se actualiza en la BD la plaza ocupada
        # Cada bus tiene sus botones (en update modificamos ID)...
#        cursor.execute("""UPDATE public."Bus" SET "Plaza1" = 1 WHERE "ID" = 1""")
 #       cursor.execute(""" COMMIT; """)


# ------------------------------------------ MÉTODO PARA RECORRIDOS DEL TREN -------------------------------------------#
def consulteTrenes(elNodoDeOrigen, elNodoDeDestino):
    lasEstacionesDelTren = [11, 8, 16, 1, 7, 23, 15, 13, 18]
    elMensaje = []
    elNodoDeOrigen = lasEstacionesDelTren.index(elNodoDeOrigen)
    elNodoDeDestino = lasEstacionesDelTren.index(elNodoDeDestino)

    if elNodoDeDestino > elNodoDeOrigen:
        for laEstacion in lasEstacionesDelTren:
            if lasEstacionesDelTren.index(laEstacion) >= elNodoDeOrigen and lasEstacionesDelTren.index(
                    laEstacion) <= elNodoDeDestino:
                elMensaje.append(laEstacion)
    elif elNodoDeDestino < elNodoDeOrigen:
        for laEstacion in range(len(lasEstacionesDelTren) - 1, -1, -1):
            if laEstacion >= elNodoDeDestino and laEstacion <= elNodoDeOrigen:
                elMensaje.append(lasEstacionesDelTren[laEstacion])
    lasIndicaciones = "Sus estaciones son: "
    for laEstacion in elMensaje:
        lasIndicaciones += obtengaElNombreDe(laEstacion)
        lasIndicaciones += ", "
    if elMensaje.count(7) > 0:
        laPosicion = elMensaje.index(7)
        if laPosicion > 0 and laPosicion < elMensaje.__len__() - 1:
            lasIndicaciones += "y no olvide hacer cambio de tren en Volcan Poas (estacion #7)"
    return (lasIndicaciones)


# ------------------------------------------ MÉTODO PARA RECORRIDOS DEL BUS --------------------------------------------#
def consulteBuses(elNodoDeOrigen, elNodoDeDestino):
    lasRutas = [[19, 24, 11, 3, 7],
                [19, 6, 22, 8, 16, 1, 7],
                [7, 1, 9, 4, 10, 21, 20, 5],
                [7, 23, 15, 13, 14, 5],
                [7, 23, 15, 12, 11, 18, 20, 5],
                [7, 2, 14, 5]]
    elOrigenHaSidoEncontrado = False
    elDestinoHaSidoEncontrado = False
    elMensaje = ""
    for laRuta in lasRutas:
        if laRuta.count(elNodoDeOrigen) > 0 and not elOrigenHaSidoEncontrado:
            origen = "Origen encontrado en ruta " + str(lasRutas.index(laRuta))
            elOrigenHaSidoEncontrado = True
            laRuta1 = laRuta
        if laRuta.count(elNodoDeDestino) > 0 and not elDestinoHaSidoEncontrado:
            destino = "y Destino encontrado en ruta " + str(lasRutas.index(laRuta))
            elDestinoHaSidoEncontrado = True
            laRuta2 = laRuta
    print(origen, destino)

    if laRuta1 != laRuta2:
        for i in laRuta1:
            if i in laRuta2:
                print("Transbordo en",obtengaElNombreDe(i))
    else:
        print("Viaje directo")


# ---------------------------------------------- MÉTODO PARA FACTURAR --------------------------------------------------#
def facturacion(laDistancia, origen, destino):
    distancia = nx.dijkstra_path_length(mapa, origen, destino)
    total = laDistancia * distancia
    print(mapa.get_edge_data(origen,destino))
    print("El costo es de", total)


# ----------------------------------------------- EJECUCIÓN DE MÉTODOS -------------------------------------------------#

#GrafoMapa()
#consulteMediosDeTransporte()
#consulteBuses(5, 19)

# facturacion(18,22,23)

if __name__ == '__main__':
 app.run(port=5000, host='127.0.0.1')

# http://amol-mandhane.github.io/htmlPy/
