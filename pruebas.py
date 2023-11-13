from flask import Flask
import pytesseract as pt
from PIL import Image
from lib.window import Window
import time

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hola, mundo!"

# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=8080)
# imagen = Image.open('prueba.JPG')

# print(pt.image_to_string(imagen))

# linea = "1 M6sY JUEGO DE MESA A 1"
# palabras = linea.split()
# # numero nombre de varias palabras tipo de 3 cinta registro
# numero = palabras[0]
# nombre_tipo = palabras[1:-2]
# cinta = palabras[-2:-1]


# encontrado=False
# var=1
# while encontrado==False and var<=3:
#     tmp = "".join(nombre_tipo[-var:])
#     print(tmp)
#     encontrado = True
#     if tmp=="UTILIDAD":
#         tipo = "UTILIDAD"
#     elif tmp=="ARCADE":
#         tipo = "ARCADE"
#     elif tmp=="CONVERSACIONAL":
#         tipo = "CONVERSACIONAL"
#     elif tmp=="VIDEOAVENTURA":
#         tipo = "VIDEOAVENTURA"
#     elif tmp=="SIMULADOR":
#         tipo = "SIMULADOR"
#     elif tmp=="JUEGODEMESA":
#         tipo = "JUEGO DE MESA"
#     elif tmp=="S.DEPORTIVO":
#         tipo = "S. DEPORTIVO"
#     elif tmp=="ESTRATEGIA":
#         tipo = "ESTRATEGIA"
#     else:
#         tipo = "DESCONOCIDO"
#         encontrado = False
#     var = var + 1

# var = var - 1
# nombre = " ".join(nombre_tipo[:-var])

# print("Tipo: ",tipo)
# print("Nombre: ",nombre)
# print(numero, nombre, tipo, cinta)



# time.sleep(10)
# ventana = Window("DOSBox 0.74, Cpu speed:     3000 cycles, Frameskip  0, Program:  GWBASIC")
# print(ventana.Info_ventana_completa())

# import cv2
# import pytesseract

# img = cv2.imread('.\\train_data\\menu.png')

# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img) 
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)


import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread('.\\train_data\\menu.png')

d = pytesseract.image_to_data(img, output_type=Output.DICT)
# print(d.keys())

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)