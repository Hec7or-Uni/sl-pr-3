from pynput.keyboard import Controller, Key

class Keyboard:
    def __init__(self):
        self.__keyboard = Controller()
    
    def Click_tecla(self, nombre):
        self.__keyboard.press(nombre)
        self.__keyboard.release(nombre)