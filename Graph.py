import pandas as pd
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np

## Abrimos el archivo de Excel a trabajar
xl= load_workbook('Sorted-Type.xlsx')

## Se crean las listas en donde se almacenarán las variables para las gráficas
agr=[]
otr=[]
mes= ["enero", "febrero","marzo", "abril", "mayo", "junio","julio","agosto","septiembre","octubre","noviembre","diciembre","enero 24","febrero 24","marzo 24","abril 24"]

## Creamos un For para recorrer todas las hojas del excel que estan separadas por mes y obtener los datos de cada una
for sheet in xl.worksheets:
	columna=sheet['A']
	conteo = len(columna) - 1

	## Obtenemos el tipo de comentarios para almacenarlos
	ws=sheet.title
	styr=ws.split("_")
	stat=styr[1]

	##Almacenamos el comentario dependiendo de su contenido
	if stat == "Agradecimientos":
		agr.append(conteo)
	elif stat == "Otros":
		otr.append(conteo)

## Guardamos las listas en variables
meses = mes
agradecimientos = agr
otros = otr

## Creamos la gráfica
plt.figure(figsize=(10, 6))

## Graficar las interacciones
plt.plot(meses, agradecimientos, label='Agradecimientos', marker='o')
plt.plot(meses, otros, label='Otros', marker='o')

## Personalizamos la gráfica
plt.title('Interacciones en Twitter')
plt.xlabel('Mes')
plt.ylabel('Tweets')
plt.xticks(meses)
plt.grid(True)
plt.legend()

## Mostrar la gráfica
plt.tight_layout()
plt.show()