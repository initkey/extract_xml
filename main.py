#Script básico para extraer información de xml's
from tkinter import Tk as tk
from tkinter import filedialog
import pandas as pd

def main():
    files = get_files_xml()

def get_traslado_xml(file,namespaces):
    types = {'Impuesto':'string','Importe':'string'}
    names = ['Impuesto','ImpuestoTrasladado']
    df = pd.read_xml(file,xpath=".//cfdi:Traslado",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'ImpuestoTrasladado'}, inplace=True)
    return df[names]

def get_concepto_xml(file,namespaces):
    types = {'Descripcion':'string','Cantidad':'string','Importe':'string'}
    names = ['Descripcion','Cantidad','Subtotal']
    df = pd.read_xml(file,xpath=".//cfdi:Concepto",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'Subtotal'}, inplace=True)
    return df[names]

def get_receptor_xml(file,namespaces):
    types = {'Nombre':'string', 'DomicilioFiscalReceptor':'string', 'RegimenFiscalReceptor':'string','UsoCFDI':'string'}
    names = ['Nombre', 'DomicilioFiscalReceptor', 'RegimenFiscalReceptor','UsoCFDI']
    df = pd.read_xml(file,xpath=".//cfdi:Receptor",namespaces=namespaces,dtype=types)
    return df[names]

def get_header_xml(file,namespaces):
    types = {'Folio':'string','Fecha':'string','MetodoPago':'string','FormaPago':'string','Moneda':'string'}
    names = ['Folio','Fecha','MetodoPago','FormaPago','Moneda']
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