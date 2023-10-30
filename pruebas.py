from flask import Flask
import pytesseract as pt
from PIL import Image

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hola, mundo!"

# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=8080)
imagen = Image.open('prueba.JPG')

print(pt.image_to_string(imagen))
