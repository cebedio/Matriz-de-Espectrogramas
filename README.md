# Matriz-de-Espectrogramas
Programa realizado en Python que automatiza la generación de una matriz de espectrograma normalizada, a partir de archivos de audio. 

El programa se encarga de generar, a aprtir de audios contenidos en una carpeta, una matriz de espectrogramas.
El usuario debe:
- Especificar la ruta a la carpeta que contiene los archivos de audio. Estos audios dpueden ser de cualquier longitud temporal y muestreados a cualquier frecuencia. El formato de los archivos de audios es .wav. 
- El usuario debe especificar la frecuencia de remuestreo. Esto se reazia para que todos los archivos esten muestreados a la mmisma frecuencia.
- El usuario determina la longitud temporal de cada espectrograma. Tenga en cuenta que si un archivo posee mayor duración, estos archivos se segmentaran según el tiempo especificado. 
El programa genera la matriz espectrograma y la guardo en un archivo con extensión .py. El usuario debe ingresar la ruta y el nombre de como lo qiuire guardar. Se generan, además archivos para los ejes de frecuencia y tiempo. Esto se utiliza para realizar una imagen.

