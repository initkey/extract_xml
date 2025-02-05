#Script básico para extraer información de xml's
from tkinter import Tk as tk
from tkinter import filedialog

def main():
    files = get_files_xml()
    print(f"Archivos: {files}")

#Función encargada de obtener los archivos xml
def get_files_xml():
    window = tk()
    window.withdraw()
    return filedialog.askopenfilenames(
        initialdir='/',
        title = 'Selecciona una carpeta',
        filetypes=[("Archivos xml","*.xml")]
    )
    

if __name__ == "__main__":
    main()

