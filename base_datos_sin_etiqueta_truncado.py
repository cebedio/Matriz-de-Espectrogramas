import numpy as np
import scipy.io.wavfile as wawe
import matplotlib.pyplot as plt
import os    # El módulo os de la librería estándar de Python se utilizan para acceder al sistema de 
             #ficheros y explorar sus directorios. 
import librosa
from scipy import signal


#La función os.listdir() devuelve una lista que contiene los nombres de las entradas (archivos y directorios) 
# del directorio indicado (path). La lista no sigue ningún tipo de orden y no se incluyen las entradas '.' y '..

#con esto busco leer todos los archivos que tengo dentro de la carpeta....
#directorio=os.path.dirname("C:/Users/celeste/desktop/CelesteTest/delfines/Bottlenose Dolphin")  
# recordar utilizar las barras invertidas a lo que figura en la ruta de windows


print('Este programa crea una tensor de espectogramas normalizados en frecuencia y amplitud, a partir de una carpeta con diferentes archivos ".wav". ')
print('Cada archivo de audio, es unificado a extensión .wav y en salida mono')
print('La dimensión del tensor generado será [cantidad_archivos, X,Y] ')
print('Los archivos de audio pueden ser de diferentes tamaños,y no necesitan estar normalizados, el programa lo hace')
print('El programa guarda la matriz creada como un archivo .py y la ubica donde el usuario desee')
print('El programa preguntará, en primer lugar, la ubicación de la carpeta que se quiere leer.')
print('Devolverá como resultado, una lista con los archivos ubicados dentro de esa carpeta y preguntará el valor de truncamiento')
print('Luego, devolverá una lista con la longitud (cantidad de muestras) de cada archivo .wav dentro de la carpeta,')
print('especificando el valor máximo, el valor mínimo y la cantidad de archivos que cumplen con la condición dada por el usuario')


#---------------------------------------------------------------------------------
#PRIMER PASO
#Se leen y colocan en forma de lista todos los archivos pertenecientes a la carpeta 
#donde se encuentran los archivos de audio
#---------------------------------------------------------------------------------

print('Escriba la ruta donde se encuentra la carpeta con los archivos de audio (recuerde que se usan las barras invertidas a lo que figura en window, es decir,C:/Users/celeste/desktop..')
carpeta=input()  # Este comando sirve para que el usuario pueda ingresar la ruta de la carpeta que desea
# poe ej: C:/Users/celeste/desktop/CelesteTest/delfines/Bottlenose Dolphin en windows. En linux va la barra al reves
lista_archivos=os.listdir(carpeta)   # me muestra todos los archivos en formato de lista. 
cantidad_archivos=len(lista_archivos)  #Me dice la cantidad de archivos que hay dentro de la carpeta. 
#print('Archivos contenidos dentro de  la carpeta especificada :',lista_archivos)
#print('Cantidad de archivos dentro de la carpeta especificada:', cantidad_archivos)

#---------------------------------------------------------------------------------
#2° PASO
## Remuestreo de los datos. Para realizar una normalización en frecuencia es necesario remuestrar longitud de los archivos .wav . 
# El usuario elije la frecuencia de remuestreo.
## ---------------------------------------------------------------------------------

print('Ingrese la frecuencia de remuestreo deseada')
frec_obj=int(input())
tamaño=[]   # se define una lista que luego indicará el tamaño de cada archivo de audio dentro de la carpeta
tramos_enteros=1
tramos=[]
print('Ingrese la longitud de normalización de los audios, en segundos')
tiempo=int(input())
muestrasmaximas=tiempo*frec_obj
lista_truncada=[]
tamaño_lista_truncada=0
sonido_posta=[]

# Este For se hace para saber la cantidad de archivos que tienen muestras mayores a las especificadas y otros datos
for j  in range(cantidad_archivos): 
  dato=os.path.join(carpeta, lista_archivos[j]) 
  sonido,f=librosa.load(dato, sr=44100, mono=True , offset=0.0 , res_type='kaiser_best' ) #sr es la frecuencia objetivo (la de resample). Por defecto lo carga como flotante
  longitud=np.shape(sonido)
  tamaño.append(longitud)  # Se obtiene una lista con la cantidad de muestras de cada uno de los archivos ".wav" dentro de la carpeta delfines remuestreados
  if longitud[0]>muestrasmaximas:     #comparo con un tamaño de muestra deseado, para que que la cantidad de muestras sea la misma
    tramos_enteros=longitud[0]//muestrasmaximas
    tramos.append(tramos_enteros)
    lista_truncada.append(lista_archivos[j])   #armo un lista de archivos .wav que posean una cantidad de muestras mayores a .....
    tamaño_lista_truncada=len(lista_truncada)  # me indica la cantidad de archivos dentro de la carpeta que superaron el limite
z=0
#print(tramos)
t=0
# se comienza con la etapa de normalización y segmentación.
Pxx=[]
if   tamaño_lista_truncada != 0 :     #se normalizan los datos y se segmentan las muestras
  for x in range (tamaño_lista_truncada):
      dato=os.path.join(carpeta, lista_truncada[x]) #armo la ruta para que busque el audio. Esto se debe realizar porque el .py se encuentra en otra carpeta
      sonido,f=librosa.load(dato, sr=frec_obj, mono=True , offset=0.0 , res_type='kaiser_best' )
      absoluto=np.abs(sonido)
      maximo=np.max(absoluto)
      sonido_normalizado=absoluto/maximo
      for i in range (tramos[x]):
        r=i*muestrasmaximas
        p=(i+1)*muestrasmaximas 
        sonido_posta.append([])
        sonido_posta[i]=sonido_normalizado[r:p]
        frecuencia, tiempo, Sxx = signal.spectrogram(sonido_posta[i] ,fs=frec_obj, nfft=256)
        Sxx =10*np.log10(Sxx) #Es para redondear y ver si puedo achicar el tamaño de los archivos
        Sxx = np.clip(Sxx, -150, 50) #elimina el problema de infinito
        Pxx = np.append(Pxx,Sxx)
        t=t+1
  s=len(frecuencia)
  h=len(tiempo)
  print()
  Pxx=np.reshape(Pxx,(s,h,t))
  print (np.shape(Pxx))
   
else:
 print('todos los archivos son menores a la cantidad de muestras especificada') 
#forma=np.array([t,s,h])
print('ingrese el nombre con el que quiere guardar la matriz de datos (sin extension txt)')
e=input()
np.save(e,Pxx)    # La matriz de espectrograma logaritmica
np.save('frecuencia',frecuencia) #conviene guardarlo para después poder dibujar
np.save('tiempo',tiempo) #conviene guardarlo para después poder dibujar
#np.save(e+'shape',forma)

#C:/Users/el_lu/Desktop/proyectospython/Datos/Ballenaa/ballena franca glacial    (Esta es la forma de ingresar la ruta)
