from flask import Flask, request, json, Response

__author__ = 'Carlos Perez', 'Diana Camacho', 'Hillary Brenes'

# Inicialización de Flask
app = Flask(__name__)


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')