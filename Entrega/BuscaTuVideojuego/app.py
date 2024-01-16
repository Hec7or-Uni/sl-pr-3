import multiprocessing, subprocess, signal, time, os, sys
import pygetwindow as gw
from flask import Flask, render_template, request, redirect, session

from lib.window import Window
from lib.keyboard import Keyboard

app = Flask(__name__)
delayScreen = 0.3
archivo = "./Database-MSDOS/Database/SALIDA.TXT"
nombre = "DOSBox 0.74, Cpu speed: max 100% cycles, Frameskip  0, Program:  GWBASIC"
leido = False
database = {
    "numReg": 0,
    "datos": []
}

def cambiar_ciclos():
    teclado = Keyboard()
    teclado.Seleccionar_todo()
    teclado.Borrar()
    teclado.Escribir_frase_normal("[sdl]\n\nfullscreen=false\nfulldouble=false\nfullresolution=original\nwindowresolution=original\noutput=surface\nautolock=true\nsensitivity=100\nwaitonerror=true\npriority=higher,normal\nmapperfile=mapper-0.74.map\nusescancodes=true\n\n")
    teclado.Escribir_frase_normal("[dosbox]\n\nlanguage=\nmachine=svga_s3\ncaptures=capture\nmemsize=16\n\n")
    teclado.Escribir_frase_normal("[render]\n\nframeskip=0\naspect=false\nscaler=normal2x\n\n")
    teclado.Escribir_frase_normal("[cpu]\n\ncore=auto\ncputype=auto\ncycles=max\ncycleup=10\ncycledown=20\n\n")
    teclado.Escribir_frase_normal("[mixer]\n\nnosound=false\nrate=44100\nblocksize=1024\nprebuffer=20\n\n")
    teclado.Escribir_frase_normal("[midi]\n\nmpu401=intelligent\nmididevice=default\nmidiconfig=\n\n")
    teclado.Escribir_frase_normal("[sblaster]\n\nsbtype=sb16\nsbbase=220\nirq=7\ndma=1\nhdma=5\nsbmixer=true\noplmode=auto\noplemu=default\noplrate=44100\n\n")
    teclado.Escribir_frase_normal("[gus]\n\ngus=false\ngusrate=44100\ngusbase=240\ngusirq=5\ngusdma=3\nultradir=C:\\ULTRASND\n\n")
    teclado.Escribir_frase_normal("[speaker]\n\npcspeaker=true\npcrate=44100\ntandy=auto\ntandyrate=44100\ndisney=true\n\n")
    teclado.Escribir_frase_normal("[joystick]\n\njoysticktype=auto\ntimed=true\nautofire=false\nswap34=false\nbuttonwrap=false\n\n")
    teclado.Escribir_frase_normal("[serial]\n\nserial1=dummy\nserial2=dummy\nserial3=disabled\nserial4=disabled\n\n")
    teclado.Escribir_frase_normal("[dos]\n\nxms=true\nems=true\numb=true\nkeyboardlayout=auto\n\n")
    teclado.Escribir_frase_normal("[ipx]\n\nipx=false\n\n")
    teclado.Escribir_frase_normal("[autoexec]\n\n")
    teclado.Guardar() 
    time.sleep(1)
    del teclado

def modificarCiclosYRedireccion():
    configuracion=subprocess.Popen("cd .\\Database-MSDOS\\DOSBox-0.74 && .\\\"DOSBox 0.74 Options.bat\"", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    while chequearVentana("dosbox-0.74.conf: Bloc de notas")==False: 0
    config = Window("dosbox-0.74.conf: Bloc de notas")
    num_linea = cambiar_ciclos()
    configuracion.wait()
    config.Cerrar_ventana()
    del config

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

def chequearVentana(ventana):
    ventanas_abiertas = gw.getWindowsWithTitle(ventana)
    if ventanas_abiertas:
        return True
    else:
        return False

def iniciar():
    global ventana, teclado, basededatos, db
    # modificarCiclosYRedireccion()
    basededatos=subprocess.Popen("cd .\\Database-MSDOS && .\\database.bat > salida.txt", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    intentos=0
    while chequearVentana(nombre)==False:
        if intentos>5:
            print("Aqui")
            terminar_aplicacion()
            sys.exit(0)
        time.sleep(2)
        intentos = intentos + 1
    print("Aqui 1")
    ventana = Window(nombre)
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
    time.sleep(delayScreen)
    teclado.Escribir_frase('RUN')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(delayScreen)

    global leido
    leido = True

def procesar(file=archivo):
    # Abre el archivo en modo lectura
    with open(file, "r") as archivo:
        lineas = archivo.readlines()  # Lee todas las líneas del archivo
        i = 15
        id = 1
        while (lineas[i].strip()!="1 - INTRODUCIR DATOS"):
            database["datos"].append({"Numero": id,"Nombre": lineas[i].strip(),"Tipo": lineas[i+1].strip(),"Cinta": lineas[i+2].strip()})
            database["numReg"] = lineas[i+3].strip()
            i = i + 5
            id = id + 1

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
    if cinta.isdigit():
        instancias_conversacionales = [instancia for instancia in database["datos"] if cinta == instancia["Cinta"]]
    else:
        instancias_conversacionales = [instancia for instancia in database["datos"] if cinta in instancia["Cinta"]]
        
    if len(instancias_conversacionales)>0:
        data["encontrado"] = "SI"
        for instancia in instancias_conversacionales:
            data["datos"].append({"numero": instancia["Numero"], "nombre": instancia["Nombre"], "tipo": instancia["Tipo"], "cinta": instancia["Cinta"]})
    return render_template("app.html", data=data)

def terminar_aplicacion():
    if leido==True:
        archivo_a_eliminar = archivo
        if os.path.exists(archivo_a_eliminar):
            os.remove(archivo_a_eliminar)
        archivo_a_eliminar = "./Database-MSDOS/salida.txt"
        if os.path.exists(archivo_a_eliminar):
            os.remove(archivo_a_eliminar)

def terminar_app(signum, frame):
    terminar_aplicacion()
    sys.exit(0)

if __name__ == '__main__':
    inicio()
    signal.signal(signal.SIGINT, terminar_app)
    app.run(host='0.0.0.0', port=8080)
