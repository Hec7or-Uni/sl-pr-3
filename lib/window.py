import pygetwindow as gw

class Window:

    def __init__(self,nombre):
        self._nombre = nombre
        self.__window = gw.getWindowsWithTitle(self._nombre)[0]

    def Cerrar_ventana(self):
        self.__window.close()