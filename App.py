import time

import networkx as nx

import matplotlib.pyplot as plt
import re, string
import psycopg2
from flask import Flask, request, json
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
mapa = nx.Graph()  # Crear el grafo

# ---------------------------------------------- CONECTAR A BASE DE DATOS ----------------------------------------------#
conexion = "host='localhost' dbname='MediosTransporte' user='postgres' password='admin'"
conn = psycopg2.connect(conexion)
cursor = conn.cursor()

user = ""


# ------------------------------------------- REGISTRO DE NUEVO USUARIO ------------------------------------------------#
@app.route('/registro', methods=['POST'])
def registro():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    usuarioStr = "'" + usuario + "'"
    contrasenaStr = "'" + contrasena + "'"

    userExist = ""

    cursor.execute("""SELECT correo FROM public.usuarios""")
    rows = cursor.fetchall()
    for row in rows:
        usersExistentesStr = str(row).replace("(", "").replace(")", "").replace(",", "").replace('[',"").replace(']',"")
        userExist = usersExistentesStr[1:-1]

    if userExist != usuario:
        cursor.execute("INSERT INTO public.usuarios(correo,pass) VALUES (" + usuarioStr + "," + contrasenaStr + ");")
        respuesta = "Se ha registrado exitosamente"
    else:
        respuesta = str(usuario) + " ya existe"

    return json.dumps({'respuesta': respuesta})


# --------------------------------------------  AUTENTICACIÓN DE USUARIO -----------------------------------------------#
@auth.get_password
def get_pw(username):
    cursor.execute("""SELECT pass FROM public.usuarios WHERE "correo"="""+ "'" + username + "'")
    rows = cursor.fetchall()
    contrasena = str(rows).replace("(", "").replace(")", "").replace(",", "").replace('[',"").replace(']',"")
    contrasenaPura = contrasena[1:-1]

    return contrasenaPura
# ------------------------------------------------ LOGIN DE USUARIO ----------------------------------------------------#
@app.route('/login', methods=['GET'])
@auth.login_required
def loginUser():

    respuesta = json.dumps({'status': 'OK', 'usuario': auth.username()})
    return respuesta


# ---------------- MÉTODO PARA AGREGAR NODOS CON ATRIBUTOS AL GRAFO Y LISTA CON RELACIONES Y DISTANCIAS ----------------#

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


# nx.draw_networkx(mapa, with_labels=True)  # Dibujar rutas del mapa (nodos conectados)
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

# Determinar si en los nodos vecinos al elNodoDeDestino final, existe un medio de transporte más rápido (avión o tren)
# en cuyo caso, enviaría a la persona hasta ese nodo en cualquiera de esos dos medios de transporte, y luego al
# nodo de elNodoDeDestino final en bus o en taxi.

@app.route('/viajando/consultas', methods=['POST'])
@auth.login_required
def consulteMediosDeTransporte():
    unOrigen = request.form['origen']
    unDestino = request.form['destino']
    elTipoTransporte = request.form['tipoTransporte']  # Seleccionar parametro con clave elTipoTransporte

    elNodoDeOrigen = int(unOrigen)
    elNodoDeDestino = int(unDestino)

    losVecinosDelNodoDestino = mapa.neighbors(elNodoDeDestino)
    losVecinosDelNodoOrigen = mapa.neighbors(elNodoDeOrigen)

    elNodoOrigenTieneTipoDeTransporte = mapa.node[elNodoDeOrigen][elTipoTransporte]
    elNodoDestinoTieneTipoDeTransporte = mapa.node[elNodoDeDestino][elTipoTransporte]

    elCosto = 0
    # --------------------------- AVIONES Y TRENES --------------------------#
    if elTipoTransporte == 'avion' or elTipoTransporte == 'tren':
        if elNodoOrigenTieneTipoDeTransporte and elNodoDestinoTieneTipoDeTransporte:
            resultado = (
                "Viaje directo de ", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elNodoDeDestino),
                "en", elTipoTransporte)
            if elTipoTransporte == 'tren':
                lasEstaciones = consulteTrenes(elNodoDeOrigen, elNodoDeDestino)
                resultado = (lasEstaciones)
                elCosto = facturacion(17, elNodoDeOrigen, elNodoDeDestino)
        else:
            if elNodoOrigenTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoDestino:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        resultado = (
                            "Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino), "en",
                            elTipoTransporte, "y luego a", obtengaElNombreDe(elNodoDeDestino),
                            "en bus o taxi")
                        if elTipoTransporte == 'tren':
                            lasEstaciones = consulteTrenes(elNodoDeOrigen, elVecino)
                            resultado = (lasEstaciones)
            elif elNodoDestinoTieneTipoDeTransporte:
                for elVecino in losVecinosDelNodoOrigen:
                    elVecinoTieneTipoDeTransporte = mapa.node[elVecino][elTipoTransporte]
                    if elVecinoTieneTipoDeTransporte:
                        resultado = ("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a", obtengaElNombreDe(elVecino),
                                     "en bus o taxi y luego de", obtengaElNombreDe(elVecino), "a",
                                     obtengaElNombreDe(elNodoDeDestino),
                                     "en", elTipoTransporte)
                        if elTipoTransporte == 'tren':
                            lasEstaciones = consulteTrenes(elVecino, elNodoDeDestino)
                            resultado = (lasEstaciones)
            else:
                for elVecinodeNodoOrigen in losVecinosDelNodoOrigen:
                    if mapa.node[elVecinodeNodoOrigen][elTipoTransporte]:
                        for elVecinodeNodoDestino in losVecinosDelNodoDestino:
                            if mapa.node[elVecinodeNodoDestino][elTipoTransporte]:
                                resultado = ("Viaje de", obtengaElNombreDe(elNodoDeOrigen), "a",
                                             obtengaElNombreDe(elVecinodeNodoOrigen), "en bus o taxi, luego de",
                                             obtengaElNombreDe(elVecinodeNodoOrigen), "en", elTipoTransporte, "a",
                                             obtengaElNombreDe(elVecinodeNodoDestino), "y por ultimo en bus o taxi a",
                                             obtengaElNombreDe(elNodoDeDestino))
                                if elTipoTransporte == 'tren':
                                    print(elVecinodeNodoOrigen, elVecinodeNodoDestino)
                                    lasEstaciones = consulteTrenes(elVecinodeNodoOrigen, elVecinodeNodoDestino)
                                    resultado = (lasEstaciones)
                            else:
                                resultado = "Imposible ir en Avion o Tren, verifique en Bus o Taxi"


    # --------------------------- TAXIS --------------------------#

    elif elTipoTransporte == 'taxi':
        resultado = consulteTaxis(elNodoDeOrigen, elNodoDeDestino)
        elCosto = facturacion(600, elNodoDeOrigen, elNodoDeDestino)

    # --------------------------- BUSES --------------------------#

    if elTipoTransporte == 'bus':
        resultado = consulteBuses(elNodoDeOrigen, elNodoDeDestino)
        elCosto = facturacion(20, elNodoDeOrigen, elNodoDeDestino)

        # ----------------------- GUARDAR EN LOG -----------------------#

    jsonToBD = '{"usuario": "' + str(user) + '", "fecha": "' + str(time.strftime("%c")) + '", "origen": "' + str(
        elNodoDeOrigen) + '", "destino": "' + str(elNodoDeDestino) + '", "tipoTransporte": "' + str(
        elTipoTransporte) + '"}'
    toLog = "'" + jsonToBD + "'"
    cursor.execute("INSERT INTO public.log(historial)  VALUES (" + toLog + ");")
    cursor.execute("COMMIT;")
    # ID es un secuencia automática creada en al BD

    # --------------------------- RESPUESTA ------------------------#

    medios = ""
    if elTipoTransporte == 'avion' or elTipoTransporte == 'tren':
        medios = ExistentesEnBaseDatos(elTipoTransporte, elNodoDeOrigen)
    # Muestra los datos por medios de transporte que existen en el punto de origen solicitado, si no hay avion,
    # no muestra nada, debe seleccionar, otro medio que lo lleve a donde exista avion,
    # (esas instrucciones también son dadas anteriorme, se le sugiere ir a otros nodos donde sí hay ese medio).
    if elTipoTransporte == 'avion':
        elCosto = facturacion(900, elNodoDeOrigen, elNodoDeDestino)

    respuesta = {"Costo": elCosto, "Respuesta ": (str(resultado) + str(medios))}
    jsonConRespuesta = json.dumps(respuesta)
    print(jsonConRespuesta)

    return jsonConRespuesta


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


# ------------------------------------------ MÉTODO PARA RECORRIDOS DE TAXIS -------------------------------------------#
def consulteTaxis(elNodoDeOrigen, elNodoDeDestino):
    ruta = []
    laRutaCorta = nx.dijkstra_path(mapa, elNodoDeOrigen, elNodoDeDestino)
    for elNodoRuta in laRutaCorta:
        losNombresDeLosNodos = obtengaElNombreDe(elNodoRuta)
        ruta += [losNombresDeLosNodos]

    zonaOrigen = obtengaLaZonaDe(elNodoDeOrigen)
    resultado = []

    # Se obtiene la zona desde donde se requiere el servicio (origen) para ofrecer un taxi que opere en dicha zona

    if zonaOrigen == 'A':
        cursor.execute(
            """SELECT "ID","Informacion" FROM public."taxi" WHERE "Informacion" ->> 'Zona' = 'A';""")
        rows = cursor.fetchall()
        for row in rows:
            resultado += [row]

    if zonaOrigen == 'B':
        cursor.execute(
            """SELECT "ID","Informacion" FROM public."taxi" WHERE "Informacion" ->> 'Zona' = 'B';""")
        rows = cursor.fetchall()
        for row in rows:
            resultado += [row]

    if zonaOrigen == 'C':
        cursor.execute(
            """SELECT "ID","Informacion" FROM public."taxi" WHERE "Informacion" ->> 'Zona' = 'C';""")
        rows = cursor.fetchall()
        for row in rows:
            resultado += [row]

    respuesta = "La ruta mas corta es pasando por " + str(ruta) + ". Estos son los taxis de la zona " + str(
        resultado)

    return respuesta


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

    for laRuta in lasRutas:
        if laRuta.count(elNodoDeOrigen) > 0 and not elOrigenHaSidoEncontrado:
            origen = "Origen encontrado en ruta " + str(lasRutas.index(laRuta))
            elOrigenHaSidoEncontrado = True
            laRuta1 = laRuta
        if laRuta.count(elNodoDeDestino) > 0 and not elDestinoHaSidoEncontrado:
            destino = "y Destino encontrado en ruta " + str(lasRutas.index(laRuta))
            elDestinoHaSidoEncontrado = True
            laRuta2 = laRuta
    resultado = (origen, destino)

    if laRuta1 != laRuta2:
        for i in laRuta1:
            if i in laRuta2:
                resultado = "Su viaje es directo hasta " + str(obtengaElNombreDe(i)) + ", en donde debe realizar " \
                                                                                       "un transbordo hacia su destino"
    else:
        resultado = "Viaje directo"

    medioDisponible = ExistentesEnBaseDatos("bus", elNodoDeOrigen)

    return resultado + str(medioDisponible)


# ------------------------------------------- MÉTODO PARA TRAER INFO DE BD----------------------------------------------#

def ExistentesEnBaseDatos(transporteSelecionado, elNodoDeOrigen):
    # Muestra los medios de transporte que están en el punto de origen solicitado
    if transporteSelecionado != "bus" and transporteSelecionado != "taxi":
        paraConsulta = """SELECT "Informacion" FROM public.""" + transporteSelecionado

        resultado = ""

        origenKey = {}
        nodoOrigenDelTransporte = 0

        cursor.execute(paraConsulta)
        rows = cursor.fetchall()
        for row in rows:
            jsons = json.dumps(row)
            data = json.loads(jsons)
            for item in data:
                origenKey = item["Ruta"]
            for i in origenKey:
                nodoOrigenDelTransporte = origenKey["Origen"]
            if nodoOrigenDelTransporte == elNodoDeOrigen:
                resultado = jsons
    else:
        cursor.execute("""SELECT * FROM public."bus" WHERE "RutaNodo" = """ + str(elNodoDeOrigen))
        rows = cursor.fetchall()
        for row in rows:
            resultado = rows

    return ". Estos son los medios disponibles : " + str(resultado)


# ---------------------------------------------- MÉTODO PARA FACTURAR --------------------------------------------------#
def facturacion2(elCostoPorKilometro, distancia, origen, destino):
    distancia = nx.dijkstra_path_length(mapa, origen, destino)
    total = elCostoPorKilometro * distancia
    # print(mapa.get_edge_data(origen, destino))
    return "El costo es de " + str(total)


def facturacion(elCostoPorKilometro, origen, destino):
    distancia = nx.dijkstra_path_length(mapa, origen, destino)
    total = elCostoPorKilometro * distancia
    # print(mapa.get_edge_data(origen, destino))
    return "El costo es de " + str(total)


# -------------------------------------------- MÉTODO PARA RESERVACIONES -----------------------------------------------#

# Actualizar espacio en BD (reservaciones en bus y avion), el cliente selecciona un ID de los mostrados en las consultas
# Primero se obtiene la cantidad que hay en la BD y luego, se le resta la cantidad de asientos

@app.route('/viajando/reservacion', methods=['POST'])
@auth.login_required
def reservaciones():
    transporteSelecionado = request.form['tipoTransporte']
    elID = int(request.form['ID'])
    cantidadReservaciones = int(request.form['cantidad'])

    resultado = ""

    if transporteSelecionado == "bus":

        cursor.execute("""SELECT "Capacidad" FROM public."bus" WHERE "ID" = """ + str(elID))
        rows = cursor.fetchall()
        for row in rows:
            capacidad = int(str(row).replace("(", "").replace(")", "").replace(",", ""))

        if cantidadReservaciones <= capacidad:
            paraActualizar = "UPDATE public.bus" + " SET " + '"Capacidad" ' + "= " + str(
                capacidad - cantidadReservaciones) + \
                             " WHERE " + '"ID"' + "= " + str(elID)

            cursor.execute(paraActualizar)
            cursor.execute("COMMIT;")
            resultado = str(cantidadReservaciones) + " asiento(s) reservado(s)"
        else:
            resultado = "Lo sentimos. Hay " + str(capacidad) + " espacio(s)"

    elif transporteSelecionado == "avion":

        paraConsulta = """SELECT "Informacion" FROM public."avion"; """

        cantidad = 0
        cursor.execute(paraConsulta)
        rows = cursor.fetchall()
        for row in rows:
            jsons = json.dumps(row)
            data = json.loads(jsons)
            for item in data:
                cantidad = item["CantidadPasajeros"]
            if cantidadReservaciones <= cantidad:
                paraActualizar = "UPDATE public.avion" + " SET " + '"Informacion" ' + "= " + \
                                 '"Informacion"' + ":: jsonb -" + " 'CantidadPasajeros' " + "||" + \
                                 "'{"'"CantidadPasajeros"'":" + str(
                    cantidad - cantidadReservaciones) + "}'" + ":: jsonb" + \
                                 " WHERE " + '"ID"' + "= " + str(elID);

                cursor.execute(paraActualizar)
                cursor.execute("COMMIT;")
                resultado = str(cantidadReservaciones) + " asiento(s) reservado(s)"

            else:
                resultado = "Lo sentimos. Hay " + str(cantidad) + " espacio(s)"


    else:
        resultado = "No es posible realizar la reservacion. " \
                    "Para tren debe ir a la estacion, y para taxi " \
                    "debe contactar al conductor"

    respuesta = {"Respuesta ": resultado}
    jsonConRespuesta = json.dumps(respuesta)
    print(jsonConRespuesta)

    return jsonConRespuesta


def calculeLaDistancia(losNodos):
    laDistancia = 0
    for elNodo in losNodos:
        laDistancia += mapa.get_edge_data(elNodo, losNodos(elNodo + 1))
    return laDistancia

# ----------------------------------------------------- EJECUCIÓN ------------------------------------------------------#
if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
