import pandas as pd
from openpyxl import Workbook
from datetime import datetime

## Leer el archivo CSV
archivo_csv = "Dathaton.csv"  ## Asegúrate de que el nombre del archivo sea correcto
datos = pd.read_csv(archivo_csv)

## Convertir la columna 'date' a formato de fecha
datos['date'] = pd.to_datetime(datos['date'])

## Eliminar la parte de la hora manteniendo solo la fecha
datos['date'] = datos['date'].dt.strftime('%m/%d/%Y')

## Crear un nuevo archivo Excel y un escritor de Excel
archivo_nuevo = "Sorted-Months.xlsx"
writer = pd.ExcelWriter(archivo_nuevo, engine='openpyxl')

# Dividir los datos por año y luego por mes, escribir en hojas separadas
for nombre_anio, grupo_anio in datos.groupby(datos['date'].str.split('/').str[2]):
    for nombre_mes, grupo_mes in grupo_anio.groupby(grupo_anio['date'].str.split('/').str[0]):
        nombre_hoja = f"{nombre_mes}-{nombre_anio}"  # Nombre de la hoja (por ejemplo: '01-2023' para enero de 2023)
        grupo_mes.to_excel(writer, sheet_name=nombre_hoja, index=False)

## Guardar el archivo Excel y cerrar el escritor
writer.close()
print("El archivo Excel con las hojas divididas por año y mes se ha creado exitosamente.")