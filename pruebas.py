from flask import Flask
import pytesseract as pt
from PIL import Image

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hola, mundo!"

# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=8080)
# imagen = Image.open('prueba.JPG')

# print(pt.image_to_string(imagen))

linea = "1 M6sY JUEGO DE MESA A 1"
palabras = linea.split()
# numero nombre de varias palabras tipo de 3 cinta registro
numero = palabras[0]
nombre_tipo = palabras[1:-2]
cinta = palabras[-2:-1]


encontrado=False
var=1
while encontrado==False and var<=3:
    tmp = "".join(nombre_tipo[-var:])
    print(tmp)
    encontrado = True
    if tmp=="UTILIDAD":
        tipo = "UTILIDAD"
    elif tmp=="ARCADE":
        tipo = "ARCADE"
    elif tmp=="CONVERSACIONAL":
        tipo = "CONVERSACIONAL"
    elif tmp=="VIDEOAVENTURA":
        tipo = "VIDEOAVENTURA"
    elif tmp=="SIMULADOR":
        tipo = "SIMULADOR"
    elif tmp=="JUEGODEMESA":
        tipo = "JUEGO DE MESA"
    elif tmp=="S.DEPORTIVO":
        tipo = "S. DEPORTIVO"
    elif tmp=="ESTRATEGIA":
        tipo = "ESTRATEGIA"
    else:
        tipo = "DESCONOCIDO"
        encontrado = False
    var = var + 1

var = var - 1
nombre = " ".join(nombre_tipo[:-var])

print("Tipo: ",tipo)
print("Nombre: ",nombre)
# print(numero, nombre, tipo, cinta)