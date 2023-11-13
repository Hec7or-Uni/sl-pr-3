from PIL import Image, ImageGrab
import pytesseract as pt

nombre = "menu"
imagen = nombre+".png"
archivo = nombre+".gt.txt"

def Eliminar_lineas_vacias(string):
    # Divide el texto en líneas y filtra las líneas no vacías
    lines = [line for line in string.splitlines() if line.strip()]

    # Une las líneas en un solo string nuevamente
    cleaned_string = '\n'.join(lines)

    return cleaned_string


# imagen = Image.open(f"./train_data/{imagen}")
string = pt.image_to_string(imagen, lang="spa_prueba", config='--psm 6')
print(string)
# cleaned_string = Eliminar_lineas_vacias(string)

# with open(f"./train_data/{archivo}", 'w') as archivo:
#     archivo.write(cleaned_string)
# print(pt.get_languages())