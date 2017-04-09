import time
import networkx as nx
import psycopg2
from flask import Flask, request, json, Response
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'
app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
elMapa = nx.Graph()  # Crear el grafo

# ---------------------------------------------- CONECTAR A BASE DE DATOS ----------------------------------------------#

laConexion = "host='localhost' dbname='MediosTransporte' user='postgres' password='admin'"
conn = psycopg2.connect(laConexion)
cursor = conn.cursor()


# ------------------------------------------- REGISTRO DE NUEVO USUARIO ------------------------------------------------#
@app.route('/registro', methods=['POST'])
def registro():
    elUsuario = request.form['usuario']
    laContrasena = request.form['contrasena']
    elUsuarioComoString = "'" + elUsuario + "'"
    laContrasenaComoString = "'" + laContrasena + "'"
    elUsuarioExiste = False

    cursor.execute("""SELECT correo FROM public.usuarios""")
    rows = cursor.fetchall()
    for row in rows:
        losUsuariosExistentesComoString = str(row).replace("(", "").replace(")", "").replace(",", "").replace('[', "").replace(']',"")
        elUsuarioEncontrado = str(losUsuariosExistentesComoString[1:-1])
        if elUsuarioExiste == elUsuario:
            elUsuarioExiste = True
    if not elUsuarioExiste:
        cursor.execute("INSERT INTO public.usuarios(correo,pass) VALUES (" + elUsuarioComoString + "," + laContrasenaComoString + ");")
        cursor.execute("COMMIT;")
        laRespuesta = "Se ha registrado exitosamente"
    else:
        laRespuesta = str(elUsuario) + " ya existe"
    elJsonConRespuesta = json.dumps({'respuesta': laRespuesta})
    laRespuestaARetornar = Response(elJsonConRespuesta, 200, mimetype='application/json')

    return laRespuestaARetornar


# --------------------------------------------  AUTENTICACIÓN DE USUARIO -----------------------------------------------#
@auth.get_password
def get_pw(username):
    cursor.execute("""SELECT pass FROM public.usuarios WHERE "correo"=""" + "'" + username + "'")
    rows = cursor.fetchall()
    laContrasena = str(rows).replace("(", "").replace(")", "").replace(",", "").replace('[', "").replace(']', "")
    soloLaContrasena = laContrasena[1:-1]

    return soloLaContrasena


# ------------------------------------------------ LOGIN DE USUARIO ----------------------------------------------------#
@app.route('/login', methods=['GET'])
@auth.login_required
def loginUser():
    laRespuesta = json.dumps({'estado': 'OK', 'usuario': auth.username()})
    laRespuestaARetornar = Response(laRespuesta, 200, mimetype='application/json')

    return laRespuestaARetornar


# ---------------- MÉTODO PARA AGREGAR NODOS CON ATRIBUTOS AL GRAFO Y LISTA CON RELACIONES Y DISTANCIAS ----------------#

elMapa.add_node(1, {"Nombre": "La Fortuna", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(2, {"Nombre": "Quepos", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(3, {"Nombre": "Las Juntas", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(4, {"Nombre": "Guapiles", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": True})
elMapa.add_node(5, {"Nombre": "Golfito", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": True})
elMapa.add_node(6, {"Nombre": "Liberia", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": True})
elMapa.add_node(7, {"Nombre": "San Jose", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": True})
elMapa.add_node(8, {"Nombre": "Upala", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(9, {"Nombre": "Puerto Viejo Sarapiqui", "zona": "B", "bus": True, "taxi": True, "tren": False,
                    "avion": False})
elMapa.add_node(10, {"Nombre": "Cahuita", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(11, {"Nombre": "Canas", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(12, {"Nombre": "Turrialba", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(13, {"Nombre": "Perez Zeledon", "zona": "C", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(14, {"Nombre": "Uvita", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(15, {"Nombre": "Cartago", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(16, {"Nombre": "Tilaran", "zona": "A", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(17, {"Nombre": "Moravia", "zona": "B", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(18, {"Nombre": "Cerro Chirripo", "zona": "C", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(19, {"Nombre": "Santa Elena", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(20, {"Nombre": "Bribri", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(21, {"Nombre": "Talamanca", "zona": "C", "bus": True, "taxi": True, "tren": False, "avion": True})
elMapa.add_node(22, {"Nombre": "Los Chiles", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})
elMapa.add_node(23, {"Nombre": "Heredia", "zona": "B", "bus": True, "taxi": True, "tren": True, "avion": False})
elMapa.add_node(24, {"Nombre": "Santa Cruz", "zona": "A", "bus": True, "taxi": True, "tren": False, "avion": False})

laLista = [(19, 24, 60),
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

elMapa.add_weighted_edges_from(laLista)


# -------------------------------------- MÉTODO PARA OBTENER NOMBRES Y ZONAS DE LOS NODOS --------------------------------------#
def obtengaElNombreDe(elNodoABuscar):
    for elNodo in elMapa.node:
        if elNodo == elNodoABuscar:
            return (elMapa.node[elNodo]["Nombre"])


def obtengaLaZonaDe(elNodoABuscar):
    for elNodo in elMapa.node:
        if elNodo == elNodoABuscar:
            return (elMapa.node[elNodo]["zona"])


# --------------------------- MÉTODO PARA REALIZA DETERMINAR MEDIOS DE TRANSPORTE DISPONIBLES --------------------------#
@app.route('/viajando/consultas', methods=['POST'])
@auth.login_required
def consulteMediosDeTransporte():
    elOrigen = request.form['origen']
    elDestino = request.form['destino']
    elTipoDeTransporte = request.form['tipoTransporte']  # Seleccionar parametro con clave elTipoTransporte

    elNodoDeOrigen = int(elOrigen)
    elNodoDeDestino = int(elDestino)

    losVecinosDelNodoDestino = elMapa.neighbors(elNodoDeDestino)
    losVecinosDelNodoOrigen = elMapa.neighbors(elNodoDeOrigen)

    elNodoOrigenTieneTipoDeTransporte = elMapa.node[elNodoDeOrigen][elTipoDeTransporte]
    elNodoDestinoTieneTipoDeTransporte = elMapa.node[elNodoDeDestino][elTipoDeTransporte]

    elResultado = ''
    laRespuestaARetornar=[]
    # --------------------------- AVIONES Y TRENES --------------------------#
    if elNodoDeOrigen != elNodoDeDestino:
        if elTipoDeTransporte == 'avion' or elTipoDeTransporte == 'tren':
            if elNodoDeDestino not in losVecinosDelNodoOrigen:
                if elNodoOrigenTieneTipoDeTransporte and elNodoDestinoTieneTipoDeTransporte:
                    elResultado = ("Viaje directo de " + obtengaElNombreDe(elNodoDeOrigen) + " a " + obtengaElNombreDe(elNodoDeDestino) + " en " + elTipoDeTransporte)
                    laRespuestaARetornar.append(elResultado)
                    if elTipoDeTransporte=='avion':
                        laRespuestaARetornar.append(consulteAvionesOTrenesEnLaBaseDeDatosDe(elNodoDeOrigen, elNodoDeDestino, 'avion'))
                        laRespuestaARetornar.append(obtengaLaFacturaDe(300, elNodoDeOrigen, elNodoDeDestino))
                    else:
                        laRespuestaARetornar.append(consulteTrenes(elNodoDeOrigen, elNodoDeDestino))
                        laRespuestaARetornar.append(obtengaLaFacturaDe(5, elNodoDeOrigen, elNodoDeDestino))
                else:
                    if elNodoOrigenTieneTipoDeTransporte:
                        for elNodoVecino in losVecinosDelNodoDestino:
                            elVecinoTieneTipoDeTransporte = elMapa.node[elNodoVecino][elTipoDeTransporte]
                            if elVecinoTieneTipoDeTransporte:
                                elResultado = ("Viaje de " + obtengaElNombreDe(elNodoDeOrigen) + " a " + obtengaElNombreDe(elNodoVecino)
                                               + " en " + elTipoDeTransporte + " y luego a " + obtengaElNombreDe(elNodoDeDestino) + " en bus o taxi")
                                laRespuestaARetornar.append(elResultado)
                                if elTipoDeTransporte == 'avion':
                                    laRespuestaARetornar.append("AVION DE "+obtengaElNombreDe(elNodoDeOrigen)+" A "+obtengaElNombreDe(elNodoVecino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(300,elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append(consulteAvionesOTrenesEnLaBaseDeDatosDe(elNodoDeOrigen, elNodoVecino, 'avion'))
                                    laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoVecino)+" A "+obtengaElNombreDe(elNodoDeDestino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(20, elNodoVecino, elNodoDeDestino))
                                    laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoVecino, elNodoDeDestino))
                                else:
                                    laRespuestaARetornar.append("TREN DE "+obtengaElNombreDe(elNodoDeOrigen)+" A "+obtengaElNombreDe(elNodoVecino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(5, elNodoDeOrigen,elNodoVecino))
                                    laRespuestaARetornar.append(consulteTrenes(elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoVecino)+" A "+obtengaElNombreDe(elNodoDeDestino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(20, elNodoVecino, elNodoDeDestino))
                                    laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoVecino,elNodoDeDestino))
                    elif elNodoDestinoTieneTipoDeTransporte:
                        for elNodoVecino in losVecinosDelNodoOrigen:
                            elVecinoTieneTipoDeTransporte = elMapa.node[elNodoVecino][elTipoDeTransporte]
                            if elVecinoTieneTipoDeTransporte:
                                elResultado = ("Viaje de " + obtengaElNombreDe(elNodoDeOrigen) + " a " + obtengaElNombreDe(elNodoVecino) +
                                               " en bus o taxi y luego de " + obtengaElNombreDe(elNodoVecino) + " a " + obtengaElNombreDe(elNodoDeDestino) +
                                               " en " + elTipoDeTransporte)
                                laRespuestaARetornar.append(elResultado)
                                if elTipoDeTransporte == 'avion':
                                    laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoDeOrigen)+ " A "+ obtengaElNombreDe(elNodoVecino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(20, elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append("AVION DE "+obtengaElNombreDe(elNodoVecino)+ " A "+ obtengaElNombreDe(elNodoDeDestino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(300, elNodoVecino, elNodoDeDestino))
                                    laRespuestaARetornar.append(consulteAvionesOTrenesEnLaBaseDeDatosDe(elNodoVecino, elNodoDeDestino, 'avion'))
                                else:
                                    laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoDeOrigen)+ " A "+ obtengaElNombreDe(elNodoVecino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(20, elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elNodoVecino))
                                    laRespuestaARetornar.append("TREN DE "+obtengaElNombreDe(elNodoVecino)+ " A "+ obtengaElNombreDe(elNodoDeDestino))
                                    laRespuestaARetornar.append(obtengaLaFacturaDe(5, elNodoVecino, elNodoDeDestino))
                                    laRespuestaARetornar.append(consulteTrenes(elNodoVecino, elNodoDeDestino))
                    else:
                        for elVecinodeNodoOrigen in losVecinosDelNodoOrigen:
                            if elMapa.node[elVecinodeNodoOrigen][elTipoDeTransporte]:
                                for elVecinodeNodoDestino in losVecinosDelNodoDestino:
                                    if elMapa.node[elVecinodeNodoDestino][elTipoDeTransporte]:
                                        resultado = ("Viaje de " + obtengaElNombreDe(elNodoDeOrigen) + " a " + obtengaElNombreDe(elVecinodeNodoOrigen) + " en bus o taxi, luego de " +
                                                     obtengaElNombreDe(elVecinodeNodoOrigen) + " en " + elTipoDeTransporte + " a " +
                                                     obtengaElNombreDe(elVecinodeNodoDestino) + " y por ultimo en bus o taxi a " +
                                                     obtengaElNombreDe(elNodoDeDestino))
                                        laRespuestaARetornar.append(resultado)
                                        if elTipoDeTransporte == 'avion':
                                            laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoDeOrigen)+" A "+ obtengaElNombreDe(elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append(obtengaLaFacturaDe(20,elNodoDeOrigen, elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append("AVION DE "+obtengaElNombreDe(elVecinodeNodoOrigen)+" A "+obtengaElNombreDe(elVecinodeNodoDestino))
                                            laRespuestaARetornar.append(300, elVecinodeNodoOrigen, elVecinodeNodoDestino)
                                            laRespuestaARetornar.append(consulteAvionesOTrenesEnLaBaseDeDatosDe(elVecinodeNodoOrigen, elVecinodeNodoDestino, 'avion'))
                                            laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elVecinodeNodoDestino)+" A "+obtengaElNombreDe(elNodoDeDestino))
                                            laRespuestaARetornar.append(obtengaLaFacturaDe(20, elVecinodeNodoDestino, elNodoDeDestino))
                                            laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elVecinodeNodoDestino, elNodoDeDestino))
                                        else:
                                            laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elNodoDeOrigen)+" A "+ obtengaElNombreDe(elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append(obtengaLaFacturaDe(20, elNodoDeOrigen, elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elVecinodeNodoOrigen))
                                            laRespuestaARetornar.append("TREN DE "+obtengaElNombreDe(elVecinodeNodoOrigen)+" A "+obtengaElNombreDe(elVecinodeNodoDestino))
                                            laRespuestaARetornar.append(obtengaLaFacturaDe(5, elVecinodeNodoOrigen, elVecinodeNodoDestino))
                                            laRespuestaARetornar.append(consulteTrenes(elVecinodeNodoOrigen, elVecinodeNodoDestino))
                                            laRespuestaARetornar.append("BUS DE "+obtengaElNombreDe(elVecinodeNodoDestino)+" A "+obtengaElNombreDe(elNodoDeDestino))
                                            laRespuestaARetornar.append(obtengaLaFacturaDe(20, elVecinodeNodoDestino, elNodoDeDestino))
                                            laRespuestaARetornar.append(consulteLasOpcionesDeBusesDe(elVecinodeNodoDestino,elNodoDeDestino))
            else:
                elResultado = "Las únicas opciones entre " + obtengaElNombreDe(
                    elNodoDeOrigen) + " y " + obtengaElNombreDe(
                    elNodoDeDestino) + " son bus y taxi"
                laRespuestaARetornar.append(elResultado)

        # --------------------------- TAXIS --------------------------#
        elif elTipoDeTransporte == 'taxi':
            elResultado = consulteLasOpcionesDeTaxisEnLaBaseDeDatos(elNodoDeOrigen, elNodoDeDestino) + obtengaLaFacturaDe(600, elNodoDeOrigen, elNodoDeDestino)
            laRespuestaARetornar.append(elResultado)
        # --------------------------- BUSES --------------------------#

        elif elTipoDeTransporte == 'bus':
            elResultado = consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elNodoDeDestino) + obtengaLaFacturaDe(20, elNodoDeOrigen, elNodoDeDestino)
            laRespuestaARetornar.append(elResultado)
    else:
        elResultado +="El origen y el destino son el mismo"
        laRespuestaARetornar.append(elResultado)

        # ----------------------- GUARDAR EN LOG -----------------------#

    jsonToBD = '{"usuario": "' + str(auth.username()) + '", "fecha": "' + str(time.strftime("%c")) + '", "origen": "' + str(elNodoDeOrigen) \
               + '", "destino": "' + str(elNodoDeDestino) + '", "tipoTransporte": "' + str(elTipoDeTransporte) + '"}'
    toLog = "'" + jsonToBD + "'"
    cursor.execute("INSERT INTO public.log(historial)  VALUES (" + toLog + ");")
    cursor.execute("COMMIT;")
    # ID es un secuencia automática creada en al BD

    # --------------------------- RESPUESTA ------------------------#

    laRespuesta = str(laRespuestaARetornar).replace("[","").replace("]","").replace("'","")
    jsonConRespuesta = json.dumps({"respuesta ": laRespuesta})
    resp = Response(jsonConRespuesta, 200, mimetype='application/json')
    print(jsonConRespuesta)

    return laRespuesta

# ------------------------------------------ MÉTODO PARA RECORRIDOS DEL TREN -------------------------------------------#
def consulteTrenes(elOrigen, elDestino):
    lasEstacionesDelTren = [11, 8, 16, 1, 7, 23, 15, 13, 18]
    elMensaje = []
    elNodoDeOrigen = lasEstacionesDelTren.index(elOrigen)
    elNodoDeDestino = lasEstacionesDelTren.index(elDestino)
    laEstacionCentral = lasEstacionesDelTren.index(7)
    lasIndicaciones = ""
    if elNodoDeDestino > elNodoDeOrigen:
        if elNodoDeOrigen < laEstacionCentral:
            lasIndicaciones += consulteAvionesOTrenesEnLaBaseDeDatosDe(11, 7, 'tren')
        else:
            lasIndicaciones += consulteAvionesOTrenesEnLaBaseDeDatosDe(7, 11, 'tren')
        for laEstacion in lasEstacionesDelTren:
            if lasEstacionesDelTren.index(laEstacion) >= elNodoDeOrigen and lasEstacionesDelTren.index(
                    laEstacion) <= elNodoDeDestino:
                elMensaje.append(laEstacion)
    elif elNodoDeDestino < elNodoDeOrigen:
        if elNodoDeOrigen > laEstacionCentral:
            lasIndicaciones += consulteAvionesOTrenesEnLaBaseDeDatosDe(18, 7, 'tren')
        else:
            lasIndicaciones += consulteAvionesOTrenesEnLaBaseDeDatosDe(7, 18, 'tren')
        for laEstacion in range(len(lasEstacionesDelTren) - 1, -1, -1):
            if laEstacion >= elNodoDeDestino and laEstacion <= elNodoDeOrigen: elMensaje.append(
                lasEstacionesDelTren[laEstacion])
    lasIndicaciones += " Sus estaciones son: "
    for laEstacion in elMensaje:
        lasIndicaciones += obtengaElNombreDe(laEstacion)
        lasIndicaciones += ", "
    if elMensaje.count(7) > 0:
        laPosicion = elMensaje.index(7)
        if laPosicion > 0 and laPosicion < elMensaje.__len__() - 1:
            lasIndicaciones += "y no olvide hacer cambio de tren en San Jose (estacion #7)"

    return (lasIndicaciones)


# ---------------------------------------- MÉTODO VERIFICAR EN BD TREN O AVION -----------------------------------------#

def consulteAvionesOTrenesEnLaBaseDeDatosDe(elNodoDeOrigen, elNodoDeDestino, elTipoDeTransporte):
    if elTipoDeTransporte == 'avion':
        cursor.execute(
            """SELECT "id", "NombreAerolinea","Horario" FROM public.avion WHERE "Origen"=""" + str(elNodoDeOrigen)
            + """AND "Destino"=""" + str(elNodoDeDestino))
    elif elTipoDeTransporte == 'tren':
        cursor.execute(
            """SELECT "ID", "NombreCompania","Horario" FROM public.tren WHERE "Origen"=""" + str(elNodoDeOrigen)
            + """AND "Destino"=""" + str(elNodoDeDestino))
    rows = cursor.fetchall()

    elMensaje = " "
    for row in rows:
        elMensaje += str(row[1] + ". Horario: " + str(row[2]))
        if elTipoDeTransporte == 'avion':
            elMensaje += ", CODIGO DE RESERVACION: " + str(row[0]) + ". "

    return elMensaje


# ------------------------------------------ MÉTODO PARA RECORRIDOS DE TAXIS -------------------------------------------#
def consulteLasOpcionesDeTaxisEnLaBaseDeDatos(elNodoDeOrigen, elNodoDeDestino):
    if elNodoDeOrigen != elNodoDeDestino:
        ruta = []
        laRutaCorta = nx.dijkstra_path(elMapa, elNodoDeOrigen, elNodoDeDestino)
        for elNodoRuta in laRutaCorta:
            losNombresDeLosNodos = obtengaElNombreDe(elNodoRuta)
            ruta += [losNombresDeLosNodos]

        zonaOrigen = obtengaLaZonaDe(elNodoDeOrigen)
        resultado = []
        cursor.execute(
            """SELECT "Informacion" FROM public."taxi" WHERE "Informacion" ->> 'Zona' = """ + "'" + zonaOrigen + "'" + """;""")
        rows = cursor.fetchall()
        contadorDeOpciones = 0
        for row in rows:
            contadorDeOpciones +=1
            resultado += [" OPCIÓN "+str(contadorDeOpciones)+": "+str(row)]
            opciones = str(resultado).replace("[", "").replace("]", "").replace("'", "").replace("(", "").replace(")","").replace('"',"")
            respuesta = "La ruta mas corta es pasando por " + str(ruta).replace("[", "").replace("]", "").replace("'","")\
                        + ". Taxis de la zona: " + opciones

    return respuesta


# ------------------------------------------ MÉTODO PARA RECORRIDOS DEL BUS --------------------------------------------#
def consulteLasOpcionesDeBusesDe(elNodoDeOrigen, elNodoDeDestino):
    elRecordatorioDeCambio = ""
    lasRutas = [[19, 24, 11, 3, 7],
                [19, 6, 22, 8, 16, 1, 7],
                [7, 1, 9, 4, 10, 21, 20, 5],
                [7, 23, 15, 13, 14, 5],
                [7, 23, 15, 12, 11, 18, 20, 5],
                [7, 2, 14, 5]]
    lasOpcionesParaLaRuta = []
    lasOpcionesEnCasoDeNecesitarHacerCambio = []
    seNecesitaHacerCambio = True
    for laRuta in lasRutas:
        if laRuta.count(elNodoDeOrigen) and laRuta.count(elNodoDeDestino):
            lasOpcionesParaLaRuta.append(lasRutas.index(laRuta))
            seNecesitaHacerCambio = False
    if seNecesitaHacerCambio:
        for laRuta in lasRutas:
            if laRuta.count(elNodoDeOrigen):
                lasOpcionesParaLaRuta.append(lasRutas.index(laRuta))
                for laRuta in lasRutas:
                    if laRuta.count(elNodoDeDestino):
                        if lasOpcionesEnCasoDeNecesitarHacerCambio.count(lasRutas.index(laRuta)) < 1:
                            lasOpcionesEnCasoDeNecesitarHacerCambio.append(lasRutas.index(laRuta))
        elRecordatorioDeCambio = "Recuerde hacer cambio en San Jose... "
    elResultadoARetornar = []
    for laRuta in lasOpcionesParaLaRuta:
        cursor.execute("""SELECT "id","ID","NombreCompania", "Conductor", "Capacidad", "Horario" FROM public."bus" WHERE "ID"=""" + str(laRuta))
        rows = cursor.fetchall()
        for row in rows:
            elResultadoARetornar += ["Sale de: " + obtengaElNombreDe(elNodoDeOrigen) + ", Ruta: " + str(row[1]) + ", bus: " + row[2]
                                     + ", conductor: " + row[3] + ", capacidad disponible: " + str(row[4]) + ", horario: "
                                     + str(row[5]) + ", CODIGO DE RESERVACION: " + str(row[0])+". "]
    if len(lasOpcionesEnCasoDeNecesitarHacerCambio) > 0:
        for laRuta in lasOpcionesEnCasoDeNecesitarHacerCambio:
            cursor.execute(
                """SELECT "id","ID","NombreCompania", "Conductor", "Capacidad", "Horario" FROM public."bus" WHERE "ID"=""" + str(
                    laRuta))
            rows = cursor.fetchall()
            for row in rows:
                elResultadoARetornar += ["Sale de San Jose, Ruta: " + str(row[1]) + ", bus: " + row[2] + ", conductor: " + row[3]
                                         + ", capacidad disponible: " + str(row[4]) + ", horario: " + str(row[5]) + ", CODIGO DE RESERVACION: "
                                         + str(row[0])+". "]
    for laOpcion in elResultadoARetornar:
        return elRecordatorioDeCambio + laOpcion


# ---------------------------------------------- MÉTODO PARA FACTURAR --------------------------------------------------#

def obtengaLaFacturaDe(elCostoPorKilometro, elOrigen, elDestino):
    laDistancia = nx.dijkstra_path_length(elMapa, elOrigen, elDestino)
    elTotal = elCostoPorKilometro * laDistancia
    return " El costo es de: " + str(elTotal)+ " colones"


# -------------------------------------------- MÉTODO PARA RESERVACIONES -----------------------------------------------#

# Actualizar espacio en BD (reservaciones en bus y avion), el cliente selecciona un ID de los mostrados en las consultas
# Primero se obtiene la cantidad que hay en la BD y luego, se le resta la cantidad de asientos

@app.route('/viajando/reservacion', methods=['POST'])
@auth.login_required
def realiceLaReservacion():
    elTransporteSeleccionado = request.form['tipoTransporte']
    elID = int(request.form['ID'])
    laCantidadDeReservaciones = int(request.form['cantidad'])
    elResultado = ""
    if elTransporteSeleccionado == "avion" or elTransporteSeleccionado == "bus":
        cursor.execute("""SELECT "Capacidad" FROM public.""" + elTransporteSeleccionado + """ WHERE "id" = """ + str(elID))
        rows = cursor.fetchall()
        for row in rows:
            laCapacidad = int(str(row).replace("(", "").replace(")", "").replace(",", ""))
        if laCantidadDeReservaciones <= laCapacidad:
            elComandoSQLParaActualizarLaCapacidad = "UPDATE public." + elTransporteSeleccionado + " SET " + '"Capacidad" ' + "= " \
                                                    + str(laCapacidad - laCantidadDeReservaciones) + " WHERE " + '"id"' + "= " + str(elID)
            cursor.execute(elComandoSQLParaActualizarLaCapacidad)
            cursor.execute("COMMIT;")
            elResultado = str(laCantidadDeReservaciones) + " asiento(s) reservado(s) con éxito"

        else:
            elResultado = "Lo sentimos. Hay " + str(laCapacidad) + " espacio(s)"

    elJsonConLaRespuesta = json.dumps({'Respuesta ': elResultado})
    laRespuestaARetornar = Response(elJsonConLaRespuesta, 200, mimetype='application/json')
    print(elJsonConLaRespuesta)

    return elResultado

# ----------------------------------------------------- EJECUCIÓN ------------------------------------------------------#
if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
