from flask import Flask, request, json, Response
import psycopg2

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'


app = Flask(__name__)


 # Conexión
conexion = "host='localhost' dbname='MediosTransporte' user='administrador' password='admin'"

print("conectando...\n	->%s" % (conexion))

# Realizar la conexión
conn = psycopg2.connect(conexion)

  #para consultas a BD
  #  cursor = conn.cursor()
   # print ("Connected!\n")


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')

