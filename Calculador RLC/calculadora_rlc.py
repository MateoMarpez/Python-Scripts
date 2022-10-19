import matplotlib.pyplot as plt
import numpy as np
import math
pi = np.pi


#@title Carga de datos
e_max =   12#@param {type: "number"}
frecuencia =   60#@param {type: "number"}
resistencia =   8#@param {type: "number"}
inductancia =  52 #@param {type: "number"}
capacitancia =  468 #@param {type: "number"}

#Reasignamos las variables para trabajar mas comodamente
frec = frecuencia
r = resistencia
l = (inductancia*(pow(10,-3)))
c = (capacitancia*(pow(10,-6)))

#Realizamos el calculo para los diferentes datos requeridos
w = 2*pi*frec     #Frecuencia angular
xc = (1/(w*c))    #Reactancia Capacitiva
xl = (w*l)        #Reactancia Inductiva
z = math.sqrt(pow(r,2)+pow((xl-xc),2)) #Impedancia Z
i_max = ((e_max)/z)           #Corriente máxima
irms = (i_max/(math.sqrt(2))) #Corriente promedio
vrms = (e_max/(math.sqrt(2))) #Voltaje promedio
vr = (i_max * r)              #Voltaje máximo en la resistencia
vl = (i_max * xl)             #Voltaje máximo en el inductor
vc = (i_max * xc)             #Voltaje máximo en el capacitor
res = (1/(math.sqrt(l*c)))    #Frecuencia de resonancia
fi = math.atan((xl-xc)/r)     #Angulo de fase
fi_grad = (fi*180)/pi         #Angulo de fase expresado en grados
fac_pot = math.cos(fi)        #Factor de potencia
p_prom = pow(irms, 2)*r       #Potencia promedio
q = ((w*l)/r)                 #Facctor Q

#Mostramos los datos calculados
print("""
  Corriente Máxima: {} A
  Voltaje en el Inductor {} V
  Voltaje en la Resistencia {} V
  Voltaje en el Capacitor {} V
  Potencia promedio: {} W
  Factor Q: {}
  Factor de potencia: {}
  Impedancia Compleja Z: {}
  Frecuencia de Resonancia {}
  
  
  """ .format(round(i_max, 3), round(vl, 3), round(vr, 3),
              round(vc, 3), round(p_prom, 3), round(q, 3),
              round(fac_pot, 3), round(z, 3),
              round(res, 3)))
if r > abs(xl-xc):
  print('El sistema es mayormente resistivo')
elif (xl > xc):
  print('El sistema es mayormente inductivo')
else:
  print('El sistema es mayormente capacitivo') 

#A continuacion se realizan los dos graficos requeridos

#Diagrama de fasores:
limites = [xl, xc, r]
xy = 0
for limite in limites:
  if xy < limite:
    xy = limite
xy = round(xy+1)

# Crear una figura de 8x6 puntos de tamaño, 80 puntos por pulgada
fasores = plt.figure(num=1,figsize=(8, 8), dpi=80)
# Establecer límites del eje x
plt.xlim(-xy, xy)
# Ticks en x
plt.xticks(np.linspace(-xy,xy, (2*xy+1), endpoint=True))
# Establecer límites del eje y
plt.ylim(-xy, xy)
# Ticks en y
plt.yticks(np.linspace(-xy, xy, (2*xy+1), endpoint=True))
# Agregamos ejes coordenoados
ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

#Graficamos los vectores del diagrama de fasores
# Vector Impedancia Z
plt.quiver(0,0,r,(xl-xc),color='red', angles='xy', scale_units='xy', scale=1)
# Vector Reactancia Inductiva
plt.quiver(0,0,0,xl,color='blue', angles='xy', scale_units='xy', scale=1)
# Vector Reactancia Capacitiva
plt.quiver(0,0,0,-xc,color='blue', angles='xy', scale_units='xy', scale=1)
# Vector Reactancia X (xl - xc)
plt.quiver(0,0,0,(xl-xc),color='green', angles='xy', scale_units='xy', scale=1)
# Vector Resistencia
plt.quiver(0,0,r,0, angles='xy', scale_units='xy', scale=1)


#Diagrama de las tensiones
# Crear una figura de 8x6 puntos de tamaño, 80 puntos por pulgada
tensiones = plt.figure(num=2,figsize=(8, 8), dpi=80)

# Agregamos ejes coordenoados
ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
# Ticks en x
plt.xticks(np.linspace(0, 4*pi, 9, endpoint=True))

# Calculamos las funciones seno para los distintos valores requeridos
pi=np.pi
t = [i for i in np.arange(0,4*pi,pi/4000)]
# Corriente
corriente=i_max*np.sin(t)
# Tension aportada por la fuente 
tension = e_max*np.sin(t)
# Tension en la resistencia
tension_vr = vr*np.sin(t)
# Tensión en el Inductor
tension_vl = vl*np.sin(t+np.ones(len(t))*pi/2)
# Tensión en el Capacitor
tension_vc = vc*np.sin(t-np.ones(len(t))*pi/2)
# Graficamos en funcion del tiempo t
plt.plot(t,corriente,t, tension, t, tension_vr, t, tension_vl, t, tension_vc, '-')

# Damos nombre al eje X
plt.xlabel("Eje X")
# Damos nombre al eje Y
plt.ylabel("Eje Y")
# Agregamos título y etiquetas al gráfico
plt.title("Onda seno")
plt.legend(["Corriente","e_max","Vr", "Vl", "Vc"])
# Ajustamos la resolución de la figura generada
plt.figure(dpi=100) 
# Mostramos el gráfico una vez finalizado
plt.show() 

#Escribimos y mostramos las ecuaciones requeridas
plt.text(1, 1.6,r'$i =I_{max} \cdot sen  (\omega t - \phi)$', fontsize=40)
plt.text(1, 1.4,r'$i = {} \cdot sen({}  t - {}°)$' .format(round(i_max,3), round(w,3), round(fi_grad,3)), fontsize=40)
plt.text(1, 1.2,r'$\Delta v = \Delta V_{max} \cdot sen(\omega t)$', fontsize=40)
plt.text(1, 1,r'$\Delta v = {}V \cdot sen({} \cdot t)$' .format(e_max, round(w,3)), fontsize=40)
plt.axis('off')
plt.show()
