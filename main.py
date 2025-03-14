#Script básico para extraer información de xml's
from tkinter import Tk as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from decimal import Decimal

def main():
    messagebox.showinfo(message="Seleccione los xml a guardar", title="Mensaje informativo")
    files = get_files_xml()
    dataframe = get_data(files)
    messagebox.showinfo(message="Guarde el archivo generado a continuación", title="Mensaje informativo")
    save_file(dataframe)

#Función encargada de guardar la información extraída en un excel
def save_file(dataframe):
    root = tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    
    if save_path:
        dataframe.to_excel(save_path,index=False)
        new_name = save_path.split('/')[-1]
        messagebox.showinfo(message=f"Archivo {new_name} generado correctamente", title="Guardado")
    else:
        messagebox.showinfo(message="Guardado cancelado", title="Cancelado")

#Función encargada de unir los dataframe de la información de los xml
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
    df.insert(2,'Mes', df['Fecha'].dt.month_name())
    return df

#Función encargada de obtener el dataframe del nodo Traslado
def get_traslado_xml(file,namespaces):
    types = {'Impuesto':'string','Importe':'string'}
    names = ['Impuesto','ImpuestoTrasladado']
    df = pd.read_xml(file,xpath=".//cfdi:Traslado",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'ImpuestoTrasladado'}, inplace=True)
    df['ImpuestoTrasladado'] = df['ImpuestoTrasladado'].apply(lambda x: Decimal(x) if x else Decimal('0.00'))
    return df[names]

#Función encargada de obtener el dataframe del nodo Concepto
def get_concepto_xml(file,namespaces):
    types = {'Descripcion':'string','Cantidad':'int64','Importe':'string'}
    names = ['Descripcion','Cantidad','Subtotal']
    df = pd.read_xml(file,xpath=".//cfdi:Concepto",namespaces=namespaces,dtype=types)
    df.rename(columns={'Importe':'Subtotal'}, inplace=True)
    df['Subtotal'] = df['Subtotal'].apply(lambda x: Decimal(x) if x else Decimal('0.00'))
    return df[names] 

#Función encargada de obtener el dataframe del nodo Receptor
def get_receptor_xml(file,namespaces):
    types = {'Nombre':'string', 'DomicilioFiscalReceptor':'string', 'RegimenFiscalReceptor':'string','UsoCFDI':'string'}
    names = ['Nombre', 'DomicilioFiscalReceptor', 'RegimenFiscalReceptor','UsoCFDI']
    df = pd.read_xml(file,xpath=".//cfdi:Receptor",namespaces=namespaces,dtype=types)
    return df[names]

#Función encargada de obtener el dataframe del Encabezado del xml
def get_header_xml(file,namespaces):
    types = {'Folio':'string','Fecha':'string','MetodoPago':'string','FormaPago':'string','Moneda':'string'}
    names = ['Folio','Fecha','MetodoPago','FormaPago','Moneda']
    df = pd.read_xml(file,xpath="/cfdi:Comprobante",namespaces=namespaces,attrs_only=True,dtype=types)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
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