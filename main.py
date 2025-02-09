#Script básico para extraer información de xml's
from tkinter import Tk as tk
from tkinter import filedialog
import pandas as pd
from decimal import Decimal

def main():
    files = get_files_xml()
    dataframe = get_data(files)
    print(dataframe)

def get_data(files):
    df = pd.DataFrame()
    namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}
    for file in files:
        df_header = get_header_xml(file,namespaces)
        df_receptor = get_receptor_xml(file,namespaces)
        df_concept = get_concepto_xml(file,namespaces)
        df_transfer = get_traslado_xml(file,namespaces)
        df_header = df_header.join(df_receptor,how='inner')
        if df_concept.shape[0] > 1:
            df_header = df_header.join(df_concept,how='outer')
            for column in df_header.columns[:df_header.columns.get_loc('UsoCFDI') + 1]:
                df_header[column] = df_header[column].ffill()
        else:
            df_header = df_header.join(df_concept,how='outer')
        total_concept = df_concept.shape[0]
        df_transfer = df_transfer.head(total_concept)
        df_header = df_header.join(df_transfer,how='outer')
        df = pd.concat([df,df_header],ignore_index=True)
    return df

def get_traslado_xml(file,namespaces):
    types = {'Impuesto':'string','Importe':'string'}
    names = ['Impuesto','ImpuestoTrasladado']
    df = pd.read_xml(file,xpath=".//cfdi:Traslado",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'ImpuestoTrasladado'}, inplace=True)
    df['ImpuestoTrasladado'] = df['ImpuestoTrasladado'].apply(lambda x: Decimal(x) if x else Decimal('0.00'))
    return df[names]

def get_concepto_xml(file,namespaces):
    types = {'Descripcion':'string','Cantidad':'int64','Importe':'string'}
    names = ['Descripcion','Cantidad','Subtotal']
    df = pd.read_xml(file,xpath=".//cfdi:Concepto",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'Subtotal'}, inplace=True)
    df['Subtotal'] = df['Subtotal'].apply(lambda x: Decimal(x) if x else Decimal('0.00'))
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