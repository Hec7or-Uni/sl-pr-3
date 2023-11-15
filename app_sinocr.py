import subprocess, signal, time, os, re
from flask import Flask, render_template, request, redirect, session

from lib.window import Window
from lib.keyboard import Keyboard

app = Flask(__name__)
delayScreen = 0.3
archivo = "./Database-MSDOS/Database/SALIDA.TXT"
leido = False
database = {
    "numReg": 0,
    "datos": []
}

def iniciar():
    global ventana, teclado, basededatos, db
    basededatos=subprocess.Popen("cd Database-MSDOS && .\\database.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    ventana = Window("DOSBox 0.74, Cpu speed:     3000 cycles, Frameskip  0, Program:  GWBASIC")
    teclado = Keyboard()
    db = True

def terminar():
    global ventana, teclado, basededatos, db
    ventana.Cerrar_ventana()
    del ventana
    del teclado
    basededatos.terminate()
    db = False

def lectura():
    teclado.Click_tecla('6')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(delayScreen)

    i = 1
    while i<=43:
        teclado.Click_tecla(' ')
        time.sleep(delayScreen)
        i = i+1

    teclado.Click_tecla('8')
    time.sleep(delayScreen)
    teclado.Click_tecla('S')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(delayScreen)
    teclado.Escribir_frase('LIST')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(3)
    teclado.Escribir_frase('RUN')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(2)

    global leido
    leido = True

def procesar(file=archivo):
    # Abre el archivo en modo lectura
    with open(file, "r") as archivo:
        lineas = archivo.readlines()  # Lee todas las líneas del archivo
        i = 15
        while (lineas[i].strip()!="1 - INTRODUCIR DATOS"):
            # print(i,": '",lineas[i].strip(),"',")
            print("Nombre: ",lineas[i].strip(),", Tipo: ",lineas[i+1].strip(),", Cinta: ",lineas[i+2].strip())
            database["datos"].append({"Numero": i-14,"Nombre": lineas[i].strip(),"Tipo": lineas[i+1].strip(),"Cinta": lineas[i+2].strip()})
            database["numReg"] = lineas[i+3].strip()
            i = i + 5
        # print("NumReg: ",database["numReg"])

def inicio():
    iniciar()
    lectura()
    terminar()
    procesar()

@app.route('/', methods=['GET'])
def index():
    data = {
        "numReg": database["numReg"],
        "encontrado": "SI",
        "datos": []
    }
    return render_template("app.html", data=data)

@app.route('/nombre', methods=['GET'])
def nombre_get():
    return redirect('/')

@app.route('/nombre', methods=['POST'])
def nombre_post():
    data = {
        "numReg": database["numReg"],
        "encontrado": "NO",
        "datos": []
    }
    nombre = request.form['nombre'].upper()
    instancias_conversacionales = [instancia for instancia in database["datos"] if nombre in instancia["Nombre"]]
    if len(instancias_conversacionales)>0:
        data["encontrado"] = "SI"
        for instancia in instancias_conversacionales:
            data["datos"].append({"numero": instancia["Numero"], "nombre": instancia["Nombre"], "tipo": instancia["Tipo"], "cinta": instancia["Cinta"]})
    return render_template("app.html", data=data)

@app.route('/cinta', methods=['GET'])
def cinta_get():
    return redirect('/')

@app.route('/cinta', methods=['POST'])
def cinta_post():
    data = {
        "numReg": database["numReg"],
        "encontrado": "NO",
        "datos": []
    }
    cinta = request.form['cinta'].upper()
    instancias_conversacionales = [instancia for instancia in database["datos"] if cinta in instancia["Cinta"]]
    if len(instancias_conversacionales)>0:
        data["encontrado"] = "SI"
        for instancia in instancias_conversacionales:
            data["datos"].append({"numero": instancia["Numero"], "nombre": instancia["Nombre"], "tipo": instancia["Tipo"], "cinta": instancia["Cinta"]})
    return render_template("app.html", data=data)

def terminar_app(signum, frame):
    if leido==True:
        archivo_a_eliminar = archivo
        if os.path.exists(archivo_a_eliminar):
            os.remove(archivo_a_eliminar)
        archivo_a_eliminar = "./Database-MSDOS/salida.txt"
        if os.path.exists(archivo_a_eliminar):
            os.remove(archivo_a_eliminar)
    exit(0)

if __name__ == '__main__':
    inicio()
    signal.signal(signal.SIGINT, terminar_app)
    app.run(host='0.0.0.0', port=8080)