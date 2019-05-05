#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import numpy as np
import matplotlib.pyplot as plt
import os
os.system("clear")

vidPath = '/home/fabouzz/Vidéos/mesuresBille/'
mesPath = vidPath + 'denoised_mesures_acous/'
fName = 'mes_cam_bille1_2'
fEch = 5e5  # Fréquence d'échantillonnage de la caméra

# Recherche de la fréqunce d'échantillonage de la caméra, de la startFrame et vidLength dans le file.cih
with open(vidPath + fName + '.cih') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith('Record Rate(fps) :'):
            fps = int(line.split(' : ')[1])
        if line.startswith('Start Frame :'):
            startFrame = int(line.split(' : ')[1])
        if line.startswith('Total Frame :'):
            vidLength = int(line.split(' : ')[1])

# Calcul des temps auxquels la video commence et se termine dans la mesure
vidStart = startFrame / fps
vidEnd = (startFrame + vidLength) / fps

# Echantillons de signal correspondant à ces temps
startEch = int(fEch * vidStart)
endEch = int(fEch * vidEnd)

print('Vid start : {}, vid end : {}'.format(vidStart, vidEnd))
print('startEch : {}, endEch : {}'.format(startEch, endEch))
datas = np.loadtxt(mesPath + 'denoised_' + fName + '.txt')
time = datas[startEch:endEch + 1, 0]  # Slice des valeurs de signal correspondant à la vidéo
mic = datas[startEch:endEch + 1, 1]  # endEch + 1 car le dernier élément n'est pas compris dans le slice
hyd = datas[startEch:endEch + 1, 2]
print('Acquis start : {}, acquis end {}'.format(time[0], time[-1]))
