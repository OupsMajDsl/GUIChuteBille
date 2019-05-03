#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import numpy as np
import matplotlib.pyplot as plt
import os
os.system("clear")

path = '/home/fabouzz/Vidéos/'
fname = 'test_cam6.cih'

with open(path + fname) as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith('Record Rate(fps) :'):
            fps = int(line.split(' : ')[1])
        if line.startswith('Start Frame :'):
            startFrame = int(line.split(' : ')[1])
