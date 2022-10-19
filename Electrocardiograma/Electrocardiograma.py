# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
from IPython.display import clear_output


if os.path.exists('electrocardiograma.xlsx') == False:
  ! wget "https://raw.githubusercontent.com/IEEESBITBA/Curso-Python/master/Clase_4_datos/electrocardiograma.xlsx"
  clear_output()

resultados = []
edades = [(1,2),(3,4),(5,6),(7,9),(10,150)]
estados = [{},{},{},{},{},{}]
estados[0] = {'sueño':(20, 79), 'reposo':(80, 130), 'actividad':(131, 300)}
estados[1] = {'sueño':(20, 79), 'reposo':(80, 120), 'actividad':(122, 300)}
estados[2] = {'sueño':(20, 74), 'reposo':(75, 115), 'actividad':(116, 300)}
estados[3] = {'sueño':(20, 69), 'reposo':(70, 110), 'actividad':(111, 300)}
estados[4] = {'sueño':(20, 59), 'reposo':(60, 100), 'actividad':(101, 300)}
estados[5] = {'sueño':(20, 39), 'reposo':(40, 60), 'actividad':(61, 300)}

def calcular_picos(X, Y):
  peakX = []
  peakY = []
  peaks = sg.find_peaks(Y, height = (0.6, 2))[0] #Lista con las posiciones de los picos en "X"
  for peak in peaks:
    peakX.append(X[peak])
    peakY.append(Y[peak])
  return peakX, peakY

def calcular_peaks(X, Y, hmin, hmax):
  xP = []
  yP = []
  peaks = sg.find_peaks(Y, height=(hmin, hmax), width=5)[0] #Lista con las posiciones de los picos en "X"
  
  for peak in peaks:
    i = peak
    j= peak
    while (abs(X[peak] - X[i]) < 0.09):
      xP.append(X[i])
      yP.append(Y[i])
      i += 1
    xP.append(np.nan)
    yP.append(np.nan)
    while (abs(X[peak] - X[j]) < 0.09):
      xP.append(X[j])
      yP.append(Y[j])
      j -= 1 
    xP.append(np.nan)
    yP.append(np.nan)
      
  return xP, yP

def calcular_P(X, Y): #(0, 0.25)
  xP, yP = calcular_peaks(X, Y, 0, 0.25)      
  return np.array(xP), np.array(yP)

def calcular_T(X, Y): #(0.2, 0.6)
  xT, yT = calcular_peaks(X, Y, 0.2, 0.6)
  return np.array(xT), np.array(yT)

def frecuencia(peakX):
  n = len(peakX) -1
  t = []
  for i in range(1, n):
    t.append(peakX[i] - peakX[i-1])
  frec = (sum(t)/len(t))**-1
  return round(frec * 60, 2)

def estado_paciente(edad, bpm, edades, estados, act):
  if act == True:
    x = 5
  else:
    i = 0
    for rango in edades:
      if edad in range(rango[0],rango[1]):
        x = i
      i += 1
  for key in estados[x]:
    a, b = estados[x][key][0], estados[x][key][1]
    if bpm in range(a, b):
      return key
    
def save(file_name, text_lines):
  textFile = open(file_name, 'w')
  for lines in text_lines:
    textFile.write(lines)
    textFile.write('\n')
  textFile.close()

#Convertimos el archivo excel en DataFrame para trabajar mas comodamente
data = pd.read_excel('electrocardiograma.xlsx')
xList = []
yList = []

for index, var in data.iterrows():
  xList.append(var['tiempo'])
  yList.append(var['señal'])
  
X = np.array(xList)
Y = np.array(yList)

#Llamamos a las funciones para calcular los datos requeridos
peakX, peakY = calcular_picos(X, Y)
xP, yP = calcular_P(X, Y)
xT, yT = calcular_T(X, Y)
frec = frecuencia(peakX)
resultados.append('la Frecuencia cardiaca del paciente es de {} pulsaciones por minuto' .format(frec))

#Estado paciente
numeros = {'0','1', '2','3','4','5','6','7','8','9'}
texto2 = ''
while texto2 == '':
  texto = input("Ingrese la edad del paciente: ")
  for l in texto:
    if l in numeros:
      texto2 = texto2 + l
edad = int(texto2)
while edad not in range(0, 150) or texto2 == '':
  print('La edad ingresada no es valida.\nIngrese solo años como números y vuelva a intentar')
  texto2 = ''
  texto = input("Ingrese la edad del paciente: ")
  for l in texto:
    if l in numeros:
      texto2 = texto2 + l
  edad = int(texto2)
act = False
act_fisica = input("¿El paciente es un atleta profesional? S/N").lower()
while (act_fisica != 'n') and (act_fisica != 's'):
  print('Comando ingresado no valido. Ingrese solo una letra')
  act_fisica = input("¿El paciente es un atleta profesional? S/N").lower()
if act_fisica == 's':
  act = True
bpm = int(round(frec))
estado = estado_paciente(edad, bpm, edades, estados, act)
textoEstado = {
    'sueño':'El paciente se encuentra en estado de sueño profundo',
    'reposo':'El paciente se encuentra en reposo',
    'actividad': 'El paciente se encuentra realizando actividad física',
    'error':'Se ha producido un error'
}
resultados.append(textoEstado.get(estado))
print(textoEstado.get(estado))

#Guardar resultados
saveT = False
save_input = input("¿Desea guardar un archivo de texto con los datos? S/N").lower()
while (save_input != 'n') and (save_input != 's'):
  print('Comando ingresado no valido. Ingrese solo una letra')
  save_input = input("¿Desea guardar un archivo de texto con los datos? S/N").lower()
if save_input == 's':
  saveT = True
  if saveT == True:
    file_name = input("Ingrese el nombre del archivo (sin extensión): ")
    while os.path.exists(file_name + '.txt') == True:
      print("El nombre de archivo ingresado esta en uso.")
      file_name = input("Por favor ingrese nuevamente el nombre del archivo: ")
    save(str(file_name + '.txt'), resultados)


#Creamos una figura
fig = plt.figure(num=1,figsize=(20, 5))
fig.suptitle('Electrocardiograma', fontsize= 18
             , fontweight='bold')
ax = fig.add_subplot(1, 1, 1)
ax.set_title('la Frecuencia cardiaca es de {} pulsaciones por minuto' .format(round(frec)))

#Graficos
#ax = fig.add_subplot(1, 2, 1)
#plt.xlim(0, 16)
#plt.xticks(np.linspace(0,2*(len(X)), 2*(len(X))))
plt.plot(X, Y)
plt.plot(xP, yP, 'r', label = 'Onda P')
plt.plot(xT, yT, 'm', label = 'Onda T')
plt.plot(peakX, peakY, 'r.', label = 'Pico complejo QRS')


#Mostramos los datos y gráficas
plt.legend()
plt.show()
plt.pause(0.05)

saveFig = False
saveFig_input = input("¿Desea guardar un archivo con el grafico? S/N").lower()
while (saveFig_input != 'n') and (saveFig_input != 's'):
  print('Comando ingresado no valido. Ingrese solo una letra')
  saveFig_input = input("¿Desea guardar un archivo con el gráfico? S/N").lower()
if saveFig_input == 's':
  saveFig = True
if saveFig == True:
  fig_name = input("Ingrese el nombre del archivo (sin extensión): ")
  plt.savefig(fig_name)

