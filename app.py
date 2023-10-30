from flask import Flask, render_template, redirect, url_for
from PIL import Image
import pytesseract as pt
import subprocess
import signal
import time
import os

from lib.window import Window

app = Flask(__name__)
database=subprocess.Popen("cd Database-MSDOS && .\\database.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route('/')
def route():
    return render_template('index.html')

@app.route('/op1', methods=['POST'])
def op1():
    return render_template('index_falso.html')

@app.route('/op2', methods=['POST'])
def op2():
    return "Operación 2 realizada"

@app.route('/op3', methods=['POST'])
def op3():
    return "Operación 3 realizada"

@app.route('/op4', methods=['POST'])
def op4():
    return "Operación 4 realizada"

@app.route('/op5', methods=['POST'])
def op5():
    return "Operación 5 realizada"

@app.route('/op6', methods=['POST'])
def op6():
    return "Operación 6 realizada"

@app.route('/op7', methods=['POST'])
def op7():
    return "Operación 7 realizada"

@app.route('/op8', methods=['POST'])
def op8():
    return "Operación 8 realizada"




def read_line(line, file="ventana.txt"):
    # Abre el archivo en modo lectura
    with open(file, "r") as archivo:
        lineas = archivo.readlines()  # Lee todas las líneas del archivo

        if 0 <= line < len(lineas):
            linea_deseada = lineas[line]
            return linea_deseada.strip()  # strip() elimina los caracteres de nueva línea
        else:
            return 0

def terminar_app(signum, frame):
    global ventana
    ventana.Cerrar_ventana()
    del ventana
    database.terminate()
    archivo_a_eliminar = "ventana.txt"
    if os.path.exists(archivo_a_eliminar):
        os.remove(archivo_a_eliminar)
    exit(0)   

def ventana_a_archivo():
    with open('ventana.txt', 'w') as archivo:
        window = ventana.Eliminar_lineas_vacias(ventana.Info_ventana())
        archivo.write(window)

if __name__ == '__main__':
    global ventana
    signal.signal(signal.SIGINT, terminar_app)
    time.sleep(4)
    ventana = Window("DOSBox 0.74, Cpu speed:     3000 cycles, Frameskip  0, Program:  GWBASIC")
    ventana_a_archivo()
    app.run(host='0.0.0.0', port=8080)