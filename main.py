#Script básico para extraer información de xml's
from tkinter import Tk as tk
from tkinter import filedialog
import pandas as pd

def main():
    files = get_files_xml()

def get_receptor_xml(file,namespaces):
    names = ['Nombre', 'DomicilioFiscalReceptor', 'RegimenFiscalReceptor','UsoCFDI']
    types = {'Nombre':'string', 'DomicilioFiscalReceptor':'string', 'RegimenFiscalReceptor':'string','UsoCFDI':'string'}
    df = pd.read_xml(file,xpath=".//cfdi:Receptor",namespaces=namespaces)
    return df[names]

def get_header_xml(file,namespaces):
    names = ['Folio','Fecha','MetodoPago','FormaPago','Moneda']
    types = {'Folio':'string','Fecha':'string','MetodoPago':'string','FormaPago':'string','Moneda':'string'}
    df = pd.read_xml(file,xpath="/cfdi:Comprobante",namespaces=namespaces,attrs_only=True,dtype=types)
    return df[names]

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