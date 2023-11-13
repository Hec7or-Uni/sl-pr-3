import subprocess, signal, time, os, re
from flask import Flask, render_template, request, redirect, session

from lib.window import Window
from lib.keyboard import Keyboard

app = Flask(__name__)
delayScreen = 1
db = False

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

def iniciar():
    global ventana, teclado, database, db
    database=subprocess.Popen("cd Database-MSDOS && .\\database.bat", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    ventana = Window("DOSBox 0.74, Cpu speed:     3000 cycles, Frameskip  0, Program:  GWBASIC")
    teclado = Keyboard()
    db = True

def ventana_a_archivo(file="ventana.txt"):
    with open(file, 'w') as archivo:
        window = ventana.Eliminar_lineas_vacias(ventana.Info_ventana())
        archivo.write(window)

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

def read_word(word, line):
    word = word - 1    
    palabras = line.split()
    return palabras[word]

def obtener_num_registros():
    teclado.Click_tecla('4')
    time.sleep(delayScreen)
    ventana_a_archivo()
    teclado.Enter()
    word = read_word(2,read_line(2))
    return word

@app.route('/', methods=['GET'])
def inicio():
    if db==True:
        terminar()
    iniciar()    

    data = {
        "numReg": obtener_num_registros(),
        "encontrado": "SI",
        "datos": []
    }
    return render_template("app.html", data=data)

@app.route('/nombre', methods=['GET'])
def nombre_get():
    return redirect('/')

@app.route('/nombre', methods=['POST'])
def nombre_post():
    time.sleep(3) # Borrar

    teclado.Click_tecla('7')
    time.sleep(delayScreen)
    teclado.Click_tecla('N')
    
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(delayScreen)
    teclado.Escribir_frase(request.form['nombre'])
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(4)
    ventana_a_archivo()
    line = read_line(4)
    print("LINEA: '", line, "'")

    if line=="NO HAY NINGUN PROGRAMA CON ESE NOMBRE; PULSA ENTER": # Programa no encontrado
        print("NO ENCONTRADO")
        teclado.Enter()
        time.sleep(delayScreen)
        teclado.Click_tecla('N')
        teclado.Enter()
        print("AQUI")
        data = {
            "numReg": obtener_num_registros(),
            "encontrado": "NO",
            "datos": []
        }

    else : # Programa encontrado
        print("ENCONTRADO")
        teclado.Enter()
        time.sleep(delayScreen)
        teclado.Enter()
        time.sleep(delayScreen)
        teclado.Enter()
        time.sleep(delayScreen)

        
        numero = read_word(1,read_line(1))
        nombre = read_word(3,read_line(1))
        tipo = read_word(4,read_line(1))
        tmp = read_word(6,read_line(1))
        cinta = tmp.split(':')[1]
        data = {
            "numReg": obtener_num_registros(),
            "encontrado": "SI",
            "datos": [{ 
                "numero": numero,
                "nombre": nombre,
                "tipo": tipo,
                "cinta": cinta
            }]
        }
        
    return render_template("app.html", data=data)

@app.route('/cinta', methods=['GET'])
def cinta_get():
    return redirect('/')

@app.route('/cinta', methods=['POST'])
def cinta_post():
    time.sleep(3) # Borrar
    
    teclado.Enter()
    time.sleep(delayScreen)
    teclado.Click_tecla('6')
    time.sleep(delayScreen)
    teclado.Enter()
    time.sleep(delayScreen)

    data = {
        "numReg": 0,
        "encontrado": "NO",
        "datos": []
    }

    hayProgramas = True
    while hayProgramas:
        ventana_a_archivo()
        i=2
        while i<20 and hayProgramas:
            if read_line(i)==0:
                hayProgramas = False
            else:
                palabras = read_line(i).split()
                numero = palabras[0]
                nombre_tipo = palabras[1:-2]
                cinta = (palabras[-2:-1])[0]
                cinta_ok = False
                # print("Cinta: ",cinta)
                # print("Nombre_Tipo: ",nombre_tipo)
                if cinta.find("-")!=-1:
                    cintas = cinta.split("-")
                    j=0
                    while j<len(cintas):
                        if cintas[i]==request.form['cinta']:
                            cinta_ok = True
                        j = j + 1
                elif cinta==request.form['cinta']:
                    cinta_ok = True

                if cinta_ok:
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
                
                    data["encontrado"] = "SI"
                    data["datos"].append({"numero": numero, "nombre": nombre, "tipo": tipo, "cinta": cinta})
                    # print("Data: ", data)
            i = i+1
        teclado.Click_tecla(" ")
        time.sleep(delayScreen)

    data["numReg"] = obtener_num_registros()

    return render_template("app.html", data=data)





def terminar_app(signum, frame):
    if db==True:
        terminar()
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminar_app)
    app.run(host='0.0.0.0', port=8080)


@app.route('/ej', methods=['POST'])
def ej():
    # Tu funcionalidad aquí
    return