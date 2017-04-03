from flask import Flask, request, json
from flask import render_template


__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

app = Flask(__name__)

@app.route('/test')
def test():
    return "Hola"

# ------------------------------------------------ MOSTRAR FORMULARIO --------------------------------------------------#
@app.route('/formulario')
def formulario():
    return render_template('registro.html')

# ------------------------------------------ MOSTRAR HTML PARA CONSULTAS -----------------------------------------------#
@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

# ----------------------------------------------------- EJECUCIÓN ------------------------------------------------------#
if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
