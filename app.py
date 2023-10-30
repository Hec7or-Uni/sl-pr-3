from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from PIL import Image
import pytesseract as pt
import subprocess
import signal
import time
import os

from lib.window import Window
from lib.keyboard import Keyboard

app = Flask(__name__)
database=subprocess.Popen("cd Database-MSDOS && .\\database.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
app.config['SESSION_TYPE'] = 'filesystem'  # Almacena los datos de sesión en el sistema de archivos
Session(app)

@app.route('/')
def route():
    return render_template('index.html')

@app.route('/op1', methods=['POST'])
def op1():
    teclado.Click_tecla('1')
    time.sleep(1)
    ventana_a_archivo()
    line = read_line(2)
    data = {"line": line}
    
    # return  jsonify({'redirect': '/op1_1', 'data': data})
    # Construye la URL de redirección con los datos en la cadena de consulta
    # redirect_url = f"/op1_1.html?line={data['line']}"
    print(line)
    # session['line'] = line
    return render_template('op1_1.html', data=line)

@app.route('/op1_1', methods=['GET'])
def op1_1():
    line = request.args['line']
    line = session['line']
    print(line)
    return redirect(f"op1_1?line={line}")


# @app.route('/op1_1', methods=['POST'])
# def op1_1():
#     data = request.get_json()
        
#     # data contendrá los datos enviados en formato JSON
#     # Puedes acceder a los valores específicos de esta manera:
#     nombre_value = data.get('nombre')
#     tipo_value = data.get('tipo')
#     print(nombre_value)
#     print(tipo_value)

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
    line = line - 1
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
    teclado = Keyboard()
    app.run(host='0.0.0.0', port=8080)