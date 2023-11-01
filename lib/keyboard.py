from pynput.keyboard import Controller, Key

class Keyboard:
    def __init__(self):
        self.__keyboard = Controller()
    
    def Click_tecla(self, nombre):
        nombre = nombre.lower()
        if nombre==" ":
            self.__keyboard.press(Key.space)
            self.__keyboard.release(Key.space)
        else:
            if nombre.isalpha():
                self.__keyboard.press(Key.shift)
                self.__keyboard.press(nombre)
                self.__keyboard.release(nombre)
                self.__keyboard.release(Key.shift)
            elif nombre.isdigit():
                self.__keyboard.press(nombre)
                self.__keyboard.release(nombre)


    def Escribir_frase(self, frase):
        for char in frase:
            self.Click_tecla(char)
        
    def Enter(self):
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)
                