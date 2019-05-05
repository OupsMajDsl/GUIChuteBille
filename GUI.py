"""Routine permettant de synchroniser un fichier vidéo avec les signaux temporels afin de faciliter l'analyse de ces derniers."""
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QLabel, QCheckBox, QComboBox,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox,
                             QSpacerItem, QFrame, QSlider, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class GUI(QDialog):
    """GUI class."""

    def __init__(self):
        """GUI definition."""
        super(GUI, self).__init__()
        self.setWindowTitle("Synchronisation Audio/vidéo pour la chute de billes")

        # Chemin des différents fichiers à charger
        # self.pathVid = "/media/mathieu/Nouveau nom/videos_bille/{}.avi"
        # self.pathTxt = "/media/mathieu/Nouveau nom/mesures_acous/{}.txt"
        # self.pathCih = "/media/mathieu/Nouveau nom/videos_bille/{}.cih"

        self.pathVid = "/home/fabouzz/Vidéos/mesuresBille/{}.avi"
        self.pathTxt = "/home/fabouzz/Vidéos/mesuresBille/denoised_mesures_acous/denoised_{}.txt"
        self.pathCih = "/home/fabouzz/Vidéos/mesuresBille/{}.cih"

        self.fEch = 5e5  # Fréquence d'echantillonage de la carte d'acquisition
        self.vidLength = 1000  # "Random" vidLength before loading the video

        # Position des capteurs et du point d'impact
        self.impact = [155e-3, 45e-3, 290e-3]  # Coordonnées x, y, z de l'impact
        self.micro = [200e-3, 50e-3, 330e-3]
        self.hydro = [100e-3, 80e-3, 270e-3]

        # Fonction à appeler dans l'initialisation
        self.objets()
        self.display()

    def objets(self):
        """Define visual objets to place in GUI."""
        self.filename = QLineEdit("mes_cam_bille1_2")
        self.load = QPushButton("Charger")
        self.load.clicked.connect(self.loadFiles)
        self.WindowSize = QLineEdit("30e-3")

        # Création des objets figure

        # Spectrogramme de l'hydrophone
        self.figSpec = Figure(figsize=(8, 4), dpi=100, tight_layout=True)
        # Allure temporelle de l'hydrohpone
        self.figTemp = Figure(figsize=(8, 4), dpi=100, tight_layout=True)
        # Allure temporelle du microphone
        self.figMicro = Figure(figsize=(8, 4), dpi=100, tight_layout=True)
        # Allure globale du signal pour savoir où on se place
        self.figSign = Figure(figsize=(19, 3), dpi=100, tight_layout=True)
        # Figure contenant l'image de la vidéo
        self.figVid = Figure(figsize=(8, 4), dpi=100, tight_layout=True)

        # Création des canvas contenant les figures
        self.canvasSpec = FigureCanvas(self.figSpec)
        self.canvasTemp = FigureCanvas(self.figTemp)
        self.canvasMicro = FigureCanvas(self.figMicro)
        self.canvasSign = FigureCanvas(self.figSign)
        self.canvasVid = FigureCanvas(self.figVid)

        # Crétion du slider
        # self.toolbarSpec = NavigationToolbar(self.canvasSpec, self)
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setMinimum(0)
        self.Slider.setMaximum(100)
        self.Slider.setTickInterval(1)
        self.Slider.setValue(0)
        self.Slider.valueChanged.connect(self.sliderUpdate)

    def display(self):
        """GUI layout using previous objets."""
        MainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.canvasVid, 0, 0)
        grid.addWidget(self.canvasSpec, 0, 1)
        grid.addWidget(self.canvasTemp, 1, 1)
        grid.addWidget(self.canvasMicro, 1, 0)

        HLayout = QHBoxLayout()
        HLayout.addWidget(self.filename)
        HLayout.addWidget(self.load)
        HLayout.addWidget(self.WindowSize)

        MainLayout.addLayout(HLayout)
        MainLayout.addLayout(grid)
        MainLayout.addWidget(self.canvasSign)
        MainLayout.addWidget(self.Slider)
        self.setLayout(MainLayout)

    def changeSliderMax(self):
        """Change slider maximum position for slider/vid sync once video loaded"""
        filename = self.filename.text()
        with open(self.pathCih.format(filename)) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Total Frame :'):
                    self.vidLength = int(line.split(' : ')[1])
        self.Slider.setMaximum(self.vidLength)

    def loadFiles(self):
        """Load file function."""
        filename = self.filename.text()  # Récupération du filename dans la barre de texte
        self.cvVideo = cv2.VideoCapture(self.pathVid.format(filename))  # Chargement video
        self.changeSliderMax()

        # Recherche de FPS et startFrame pour calcul ultérieur des echantillons temporels
        with open(self.pathCih.format(filename)) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Record Rate(fps) :'):
                    self.fps = int(line.split(' : ')[1])
                if line.startswith('Start Frame :'):
                    self.startFrame = int(line.split(' : ')[1])

        self.data = np.loadtxt(self.pathTxt.format(filename))
        self.plot()

    def sliderUpdate(self):
        """Update the bottom screen slider. Useful for updating datas."""
        # print(str(self.Slider.value()))
        self.plot(pos=self.Slider.value())

    def plot(self, pos=0):
        """Plot a video frame, temporal signals and spectorgam on the GUI."""
        MidFen = pos / self.vidLength

        # Calcul des temps auxquels la video commence et se termine dans la mesure
        vidStart = self.startFrame / self.fps
        vidEnd = (self.startFrame + self.vidLength) / self.fps

        # Echantillons de signal correspondant à ces temps
        startEch = int(self.fEch * vidStart)
        endEch = int(self.fEch * vidEnd)

        time = self.data[startEch:endEch + 1, 0]  # Slice des valeurs de signal correspondant à la vidéo
        micro = self.data[startEch:endEch + 1, 1]  # endEch + 1 car le dernier élément n'est pas compris dans le slice
        hydro = self.data[startEch:endEch + 1, 2]

        print('Vid start : {}, vid end : {}'.format(vidStart, vidEnd))
        print('startEch : {}, endEch : {}'.format(startEch, endEch))
        print('Acquis start : {}, acquis end {}'.format(time[0], time[-1]))

        # Allure générale des signaux
        self.figSign.clear()
        ax = self.figSign.add_subplot(111)
        ax.plot(time, hydro)
        ax.axvline(MidFen - float(self.WindowSize.text()), color='r')
        ax.axvline(MidFen + float(self.WindowSize.text()), color='r')
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.fill_between()
        self.canvasSign.draw()

        # Tracé temporel du microphone
        self.figMicro.clear()
        ax = self.figMicro.add_subplot(111)
        ax.plot(time, micro)
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.axvline(MidFen, color='r')
        ax.set_title("Micro")
        self.canvasMicro.draw()

        # Tracé temporel de l'hydrophone
        self.figTemp.clear()
        ax = self.figTemp.add_subplot(111)
        ax.plot(time, hydro)
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.axvline(MidFen, color='r')
        ax.set_title("Hydrophone temporel")
        self.canvasTemp.draw()

        # Tracé du spectrogramme
        self.figSpec.clear()
        ax = self.figSpec.add_subplot(111)
        fs = len(time) / max(time)
        f, t, spectrogram = sig.spectrogram(hydro, fs)
        ax.pcolormesh(t, f, spectrogram, cmap='Greens')
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.axvline(MidFen, color='r')
        ax.set_title("Hydrophone spectrogramme")
        ax.set_ylim(0, 30e3)
        self.canvasSpec.draw()
        self.figVid.clear()

        # Extraction d'une certaine frame de la vidéo
        self.cvVideo.set(cv2.CAP_PROP_POS_FRAMES, self.Slider.value())
        ret, self.frame = self.cvVideo.read()

        ax = self.figVid.add_subplot(111)
        ax.imshow(self.frame)
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvasVid.draw()

    def flightTime(self):
        """Calculate wave flight time in water and air for sync."""
        c_air = 343  # Sound speed in air
        c_eau = 1500  # Sound speed in water

        # Distance between impact zone and microphone
        d_micro = np.sqrt((self.micro[0] - self.impact[0])**2 +
                          (self.micro[1] - self.impact[1])**2 +
                          (self.micro[2] - self.impact[2])**2)

        # Distance between impact zone and microphone
        d_hydro = np.sqrt((self.hydro[0] - self.impact[0])**2 +
                          (self.hydro[1] - self.impact[1])**2 +
                          (self.hydro[2] - self.impact[2])**2)

        # Wave flight time between impact/mic and impact/hydrohpone
        tdv_micro = d_micro / c_air
        tdv_hydro = d_hydro / c_eau


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = GUI()
    clock.show()
    sys.exit(app.exec_())
