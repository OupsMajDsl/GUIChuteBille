
"""
Routine permettant de synchroniser un fichier vidéo avec les signaux temporels afin de faciliter l'analyse de ces derniers.
"""

import sys
import cv2
import numpy as np
import getpass
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
        self.setWindowIcon(QIcon("icon.jpeg"))
        self.setGeometry(200, 200, 800, 700)

        self.user = getpass.getuser()
        # Chemin des différents fichiers à charger selon l'utilisateur
        if self.user == 'mathieu':
            self.pathVid = "/media/mathieu/EHDD/videos_bille/{}.avi"
            self.pathTxt = "/media/mathieu/EHDD/denoised_mesures_acous/denoised_{}.txt"
            self.pathCih = "/media/mathieu/EHDD/videos_bille/{}.cih"

        elif self.user == 'fabouzz':
            self.pathVid = "/home/fabouzz/Vidéos/mesuresBille/{}.avi"
            self.pathTxt = "/home/fabouzz/Vidéos/mesuresBille/denoised_mesures_acous/denoised_{}.txt"
            self.pathCih = "/home/fabouzz/Vidéos/mesuresBille/{}.cih"

        self.Fs = 500e3  # Fréquence d'echantillonage de la carte d'acquisition
        self.nFrames = 0  # Initialisation: number of frames before loading the video

        # Position des capteurs et du point d'impact
        self.impact = [155e-3, 45e-3, 290e-3]  # Coordonnées x, y, z de l'impact
        self.micro = [200e-3, 50e-3, 330e-3]
        self.hydro = [100e-3, 80e-3, 270e-3]

        # Fonction à appeler dans l'initialisation
        self.objets()
        self.display()

    def objets(self):
        """Define visual objets to place in GUI."""
        self.filename = QLineEdit("mes_sh_b3_1")
        self.load = QPushButton("Charger")
        self.load.clicked.connect(self.loadFiles)
        self.WindowSize = QLineEdit("5e-4")
        self.WindowSize.setMaximumWidth(100)

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
        self.Canvas = [FigureCanvas(self.figVid), FigureCanvas(self.figSign), 
                        FigureCanvas(self.figMicro), FigureCanvas(self.figTemp), 
                        FigureCanvas(self.figSpec)]

        # Crétion du slider
        # self.toolbarSpec = NavigationToolbar(self.canvasSpec, self)
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setMinimum(1)
        self.Slider.setMaximum(100)
        self.Slider.setTickInterval(1)
        self.Slider.setValue(0)
        self.Slider.valueChanged.connect(self.sliderUpdate)

    def display(self):
        """GUI layout using previous objets."""
        MainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.Canvas[0], 0, 0)
        grid.addWidget(self.Canvas[4], 0, 1)
        grid.addWidget(self.Canvas[3], 1, 1)
        grid.addWidget(self.Canvas[2], 1, 0)

        HLayout = QHBoxLayout()
        HLayout.addWidget(self.filename)
        HLayout.addWidget(self.load)
        HLayout.addWidget(self.WindowSize)

        MainLayout.addLayout(HLayout)
        MainLayout.addLayout(grid)
        MainLayout.addWidget(self.Canvas[1])
        MainLayout.addWidget(self.Slider)
        self.setLayout(MainLayout)

    def loadFiles(self):
        """Load file function."""
        self.load.setDisabled(True)
        filename = self.filename.text()  # Récupération du filename dans la barre de texte
        self.cvVideo = cv2.VideoCapture(self.pathVid.format(filename))  # Chargement video
        self.data = np.loadtxt(self.pathTxt.format(filename))    # Chargement du fichier texte associé

        # Recherche de FPS et startFrame pour calcul ultérieur des echantillons temporels
        # dans le fichier de configuration des acquisitions vidéo
        with open(self.pathCih.format(filename)) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Record Rate(fps) :'):
                    self.fps = int(line.split(' : ')[1])
                if line.startswith('Start Frame :'):
                    self.startFrame = int(line.split(' : ')[1])
                if line.startswith('Total Frame :'):
                    self.nFrames = int(line.split(' : ')[1])

        # Calcul des temps auxquels la video commence et se termine dans la mesure
        self.vidStart = self.startFrame / self.fps
        self.vidEnd = (self.startFrame + self.nFrames) / self.fps

        # Ajustement du slider à la vidéo: il glisse de la première 
        # à la dernière frame de la vidéo
        self.Slider.setMaximum(self.nFrames)
        self.load.setDisabled(False)
        self.plot()

    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def keyPressEvent(self, event):
        """
        gestion des touches flèche droite / flèche gauche pour avancer / reculer 
        d'une seule image
        """
        if event.key() == Qt.Key_Right:
            self.slider.setValue(self.slider.value() + 1)
        elif event.key() == Qt.Key_Left:
            self.slider.setValue(self.slider.value() - 1)
        else:
        # Eviter le crash de l'interface dans le cas d'un spam de touche
            try:
                self.keyPressEvent(self, event)
            except TypeError:
                pass

    def sliderUpdate(self):
        """Update the bottom screen slider. Updates data."""
        self.plot(pos=self.Slider.value())

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
        self.tdv_micro = d_micro / c_air
        self.tdv_hydro = d_hydro / c_eau

    def plot(self, pos=0):
        """Plot a video frame, temporal signals and spectorgam on the GUI."""
        self.flightTime() # Calcul du temps de vpl pour les différents capteurs
        # Echantillons de signal correspondant à ces temps
        startEch = int(self.Fs * self.vidStart)
        endEch = int(self.Fs * self.vidEnd)

        # Grandeurs contenues dans le fichier texte
        time = np.asarray(self.data[startEch:endEch + 1, 0])  # Slice des valeurs de signal correspondant à la vidéo
        micro = self.data[startEch:endEch + 1, 1]  # endEch + 1 car le dernier élément n'est pas compris dans le slice
        hydro = self.data[startEch:endEch + 1, 2]

        # Ajustement pour que le temps commence au 0 correspondant à la vidéo
        time = time - time[0]

        # Extraction d'une certaine frame de la vidéo
        self.cvVideo.set(cv2.CAP_PROP_POS_FRAMES, self.Slider.value())
        # lecture de la frame extraite
        ret, self.frame = self.cvVideo.read()
        # temps correspondant à la frame
        currentTime = (self.cvVideo.get(cv2.CAP_PROP_POS_FRAMES)) / self.fps
         # + self.startFrame
        # Tracé de la frame de la vidéo
        self.figVid.clear()
        ax = self.figVid.add_subplot(111)
        ax.imshow(self.frame)
        ax.set_xticks([])
        ax.set_yticks([])
        self.Canvas[0].draw()

        # Allure générale des signaux
        self.figSign.clear()
        ax = self.figSign.add_subplot(111)
        ax.plot(time, hydro)
        ax.plot(time, micro, alpha=.5)
        ax.set_xlim(time[0], time[-1])
        ax.axvline(currentTime + self.tdv_hydro - float(self.WindowSize.text()), color='r')
        ax.axvline(currentTime + self.tdv_hydro + float(self.WindowSize.text()), color='r')
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.fill_between()
        self.Canvas[1].draw()

        # Redéfinition des vecteurs micro et hydro pour tracer seulement une portion de signal
        # 
        micro_min = self.find_nearest(time, 
                currentTime + self.tdv_micro - float(self.WindowSize.text()))
        micro_max = self.find_nearest(time, 
                currentTime + self.tdv_micro + float(self.WindowSize.text()))

        hydro_min = self.find_nearest(time, 
                currentTime + self.tdv_hydro - float(self.WindowSize.text()))
        hydro_max = self.find_nearest(time, 
                currentTime + self.tdv_hydro + float(self.WindowSize.text()))

        # Tracé temporel du microphone
        self.figMicro.clear()
        ax = self.figMicro.add_subplot(111)
        ax.plot(time[micro_min: micro_max], micro[micro_min: micro_max])
        ax.set_xlim(currentTime + self.tdv_micro - float(self.WindowSize.text()),
                currentTime + self.tdv_micro + float(self.WindowSize.text()))
        ax.axvline(currentTime + self.tdv_micro, color='r')
        ax.set_title("Micro")
        ax.set_xlabel("Temps [s]")
        ax.set_ylabel("Pression [Pa]")
        self.Canvas[2].draw()

        # Tracé temporel de l'hydrophone
        self.figTemp.clear()
        ax = self.figTemp.add_subplot(111)
        ax.plot(time[hydro_min: hydro_max], hydro[hydro_min: hydro_max])
        ax.set_xlim(currentTime + self.tdv_hydro - float(self.WindowSize.text()),
                    currentTime + self.tdv_hydro + float(self.WindowSize.text()))
        ax.axvline(currentTime + self.tdv_hydro, color='r')
        ax.set_title("Hydrophone temporel")
        ax.set_xlabel("Temps [s]")
        ax.set_ylabel("Pression [Pa]")
        self.Canvas[3].draw()

        # Tracé du spectrogramme
        self.figSpec.clear()
        ax = self.figSpec.add_subplot(111)
        hydro = hydro / max(hydro)
        
        NFFT = 2048       
        overlap = 0.75
        Pxx, freqs, bins, im = ax.specgram(micro, NFFT=NFFT, Fs=self.Fs,
                    noverlap=NFFT*overlap, cmap='jet')


        # ax.set_yscale("log")
        ax.axvline(currentTime, color='r')
        ax.set_title("Hydrophone spectrogramme")
        ax.set_ylim(0, 30e3)
        ax.set_xlabel("Temps [s]")
        ax.set_ylabel("Fréquence [Hz]")
        ax.set_xlim(currentTime + self.tdv_hydro - float(self.WindowSize.text()), currentTime + self.tdv_hydro + float(self.WindowSize.text()))
        self.Canvas[4].draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = GUI()
    clock.show()
    sys.exit(app.exec_())