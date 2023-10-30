from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import subprocess
import signal
import time
import os
import re

from lib.window import Window
from lib.keyboard import Keyboard

app = Flask(__name__)
db = False

def obtener_info():
    patron = r'\d+'  # Este patrón busca uno o más dígitos consecutivos

    lineNum = read_line(2)
    num  = re.findall(patron, lineNum)[0]

    lineMem = read_line(5)
    palabras = lineMem.split()
    n = palabras[0] # Obtiene la primera palabra
    if n!="Memoria":
        lineMem = read_line(4)
        ord = False
    else:
        ord = True    
    mem = re.findall(patron, lineMem)[0]

    lineOrden = read_line(3)
    if ord==False:
        lineOrden = read_line(4)
        palabras = lineOrden.split()
        orden = palabras[7] # Obtiene la octava palabra
    else:
        lineOrden = read_line(3)
        palabras = lineOrden.split()
        orden = palabras[9] # Obtiene la decima palabra
    
    return num, mem, orden, ord

def iniciar():
    global ventana, teclado, database, db
    if db==False:
        database=subprocess.Popen("cd Database-MSDOS && .\\database.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(4)
        ventana = Window("DOSBox 0.74, Cpu speed:     3000 cycles, Frameskip  0, Program:  GWBASIC")
        teclado = Keyboard()
        db = True

def terminar():
    global ventana, teclado, database, db
    ventana.Cerrar_ventana()
    del ventana
    del teclado
    database.terminate()
    db = False
    archivo_a_eliminar = "ventana.txt"
    if os.path.exists(archivo_a_eliminar):
        os.remove(archivo_a_eliminar) 

@app.route('/')
def route():
    return render_template('index.html')

@app.route('/op', methods=['POST', 'GET'])
def op():
    iniciar()
    return render_template('listado.html')

@app.route('/op1', methods=['POST'])
def op1():
    time.sleep(3)
    teclado.Click_tecla('1')
    time.sleep(1)
    ventana_a_archivo()
    line = read_line(2)
    return render_template('op1.html', data=line)

@app.route('/op1_1', methods=['POST'])
def op1_1():
    time.sleep(3)
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    cinta = request.form['cinta']
    print(nombre)
    print(tipo)
    print(cinta)

    teclado.Escribir_frase(nombre)
    teclado.Enter()
    time.sleep(0.5)
    teclado.Escribir_frase(tipo)
    teclado.Enter()
    time.sleep(0.5)
    teclado.Escribir_frase(cinta)
    teclado.Enter()
    time.sleep(0.5)
    teclado.Enter()
    time.sleep(0.5)
    teclado.Enter()
    return redirect('/op')

@app.route('/op2', methods=['POST'])
def op2():
    time.sleep(3)
    teclado.Click_tecla('2')
    teclado.Enter()
    time.sleep(1)
    return render_template('op2.html')

@app.route('/op2_1', methods=['POST'])
def op2_1():
    time.sleep(3)
    teclado.Click_tecla('1')
    teclado.Enter()
    time.sleep(1)
    return redirect('/op')

@app.route('/op2_2', methods=['POST'])
def op2_2():
    time.sleep(3)
    teclado.Click_tecla('2')
    teclado.Enter()
    time.sleep(1)
    return redirect('/op')

@app.route('/op2_3', methods=['POST'])
def op2_3():
    time.sleep(3)
    teclado.Click_tecla('3')
    teclado.Enter()
    time.sleep(1)
    return redirect('/op')

@app.route('/op3', methods=['POST'])
def op3():
    time.sleep(3)
    teclado.Click_tecla('3')
    time.sleep(1)
    ventana_a_archivo()

    _, _, orden, ord = obtener_info()

    if ord==True:
        data=f"Ordenada por el campo '{orden}'."
    else:
        data="No está ordenada."

    return render_template('op3.html', data=data)

@app.route('/op3_1', methods=['POST'])
def op3_1():
    orden = request.form['orden']

    if orden=="Nombre":
        teclado.Click_tecla('1')
        teclado.Enter()
    elif orden=="Tipo":
        teclado.Click_tecla('2')
        teclado.Enter()
    elif orden=="Cinta":
        teclado.Click_tecla('3')
        teclado.Enter()
    elif orden=="Antigüedad":
        teclado.Click_tecla('4')
        teclado.Enter()

    return redirect('/op')

@app.route('/op4', methods=['POST'])
def op4():
    time.sleep(3)
    teclado.Click_tecla('4')
    time.sleep(1)
    ventana_a_archivo()

    num, mem, orden, ord = obtener_info()

    teclado.Enter()

    return render_template('op4.html',num=num,mem=mem,orden=orden,ord=ord)

@app.route('/op5', methods=['POST'])
def op5():
    mensaje = "Función a implementar más adelante."
    return render_template('listado.html', mensaje=mensaje)

@app.route('/op6', methods=['POST'])
def op6():
    mensaje = "Función a implementar más adelante."
    return render_template('listado.html', mensaje=mensaje)

@app.route('/op7', methods=['POST'])
def op7():
    mensaje = "Función a implementar más adelante."
    return render_template('listado.html', mensaje=mensaje)

@app.route('/op8', methods=['POST'])
def op8():
    terminar()
    return redirect('/')




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
    terminar()
    exit(0)

def ventana_a_archivo():
    with open('ventana.txt', 'w') as archivo:
        window = ventana.Eliminar_lineas_vacias(ventana.Info_ventana())
        archivo.write(window)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminar_app)
    app.run(host='0.0.0.0', port=8080)