import pandas as pd
import SortMonths


# Cargar el archivo Excel con varias hojas
archivo_entrada = "Sorted-Months.xlsx"
archivo_salida = "Sorted-Type.xlsx"

# Cargar todas las hojas del archivo Excel
sheets = pd.read_excel(archivo_entrada, sheet_name=None)

# Crear un ExcelWriter para escribir en un archivo Excel
writer = pd.ExcelWriter(archivo_salida, engine="openpyxl")

# Iterar sobre todas las hojas
for sheet_name, df in sheets.items():
    # Separar los tweets por categoría en esta hoja
    tweets_agradecimientos = df[df["tweet"].str.lower().str.contains("gracias", na=False)]
    tweets_otros = df[~df["tweet"].str.lower().str.contains("gracias", na=False)]

    # Escribir los resultados en el archivo Excel
    tweets_agradecimientos.to_excel(writer, sheet_name=f"{sheet_name}_Agradecimientos", index=False)
    tweets_otros.to_excel(writer, sheet_name=f"{sheet_name}_Otros", index=False)

# Guardar y cerrar el archivo Excel

writer.close()


print("El archivo de tweets modificados creado exitosamente")