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
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Synchronisation Audio/vidéo pour la chute de billes")

        # Chemin des différents fichiers à charger
        self.pathVid = "/media/mathieu/Nouveau nom/videos_bille/{}.avi"
        self.pathTxt = "/media/mathieu/Nouveau nom/mesures_acous/{}.txt"
        self.pathCih = "/media/mathieu/Nouveau nom/mesures_acous/{}.cih"

        self.length = 2000

        # Fonction à appeler dans l'initialisation
        self.Objets()
        self.display()

    def Objets(self):
        self.filename = QLineEdit("mes_haut3_bille2_1")
        self.load = QPushButton("Charger")
        self.load.clicked.connect(self.loadFiles)
        self.WindowSize = QLineEdit("30e-3")

        # Création des objets figure
            # Spectrogramme de l'hydrophone
        self.figSpec = Figure(figsize=(8, 4), dpi=100)
            # Allure temporelle de l'hydrohpone
        self.figTemp = Figure(figsize=(8, 4), dpi=100)
            # Allure temporelle du microphone
        self.figMicro = Figure(figsize=(8, 4), dpi=100)
            # Allure globale du signal pour savoir où on se place
        self.figSign = Figure(figsize=(19, 3), dpi=100)
            # Figure contenant l'image de la vidéo
        self.figVid = Figure(figsize=(8, 4), dpi=100)

        # Création des canvas contenant les figures
        self.canvasSpec = FigureCanvas(self.figSpec)
        self.canvasTemp = FigureCanvas(self.figTemp)
        self.canvasMicro = FigureCanvas(self.figMicro)
        self.canvasSign = FigureCanvas(self.figSign)
        self.canvasVid = FigureCanvas(self.figVid)

        # self.toolbarSpec = NavigationToolbar(self.canvasSpec, self)
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setMinimum(0)
        self.Slider.setMaximum(self.length)
        self.Slider.setTickInterval(1)
        self.Slider.setValue(0)
        self.Slider.valueChanged.connect(self.SliderUpdate)

    def display(self):
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


# mes_haut3_bille2_1
    def loadFiles(self):
        filename = self.filename.text()
        self.cvVideo = cv2.VideoCapture(self.pathVid.format(filename))
        self.data = np.loadtxt(self.pathTxt.format(filename))
        self.plot()
        with open(self.pathCih) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Record Rate(fps) :'):
                    fps = int(line.split(' : ')[1])
                if line.startswith('Start Frame :'):
                    startFrame = int(line.split(' : ')[1])

    def SliderUpdate(self):
        print(str(self.Slider.value()))
        self.plot(pos=self.Slider.value())

    def plot(self, pos=0):
        MidFen = pos / self.length
        time = self.data[:, 0]
        micro = self.data[:, 1]
        hydro = self.data[:, 2]

        # Allure générale des signaux
        self.figSign.clear()
        ax = self.figSign.add_subplot(111)
        ax.plot(time, hydro)
        ax.axvline(MidFen - float(self.WindowSize.text()), color='r')
        ax.axvline(MidFen + float(self.WindowSize.text()), color='r')
        ax.fill_between()
        self.canvasSign.draw()

        # Tracé temporel du microphone
        self.figMicro.clear()
        ax = self.figMicro.add_subplot(111)
        ax.plot(time, micro)
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.set_title("Micro")
        self.canvasMicro.draw()

        # Tracé temporel de l'hydrophone
        self.figTemp.clear()
        ax = self.figTemp.add_subplot(111)
        ax.plot(time, hydro)
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.set_title("Hydrophone temporel")
        self.canvasTemp.draw()

        self.figSpec.clear()
        ax = self.figSpec.add_subplot(111)
        fs = len(time) / max(time)
        f, t, spectrogram = sig.spectrogram(hydro, fs)
        ax.pcolormesh(t, f, spectrogram, cmap='Greens')
        ax.set_xlim(MidFen - float(self.WindowSize.text()), MidFen + float(self.WindowSize.text()))
        ax.set_title("Hydrophone spectrogramme")
        ax.set_ylim(0, 30e3)
        self.canvasSpec.draw()

        self.figVid.clear()

        # Extraction d'une certaine frame de la vidéo
        fps = self.cvVideo.get(cv2.CAP_PROP_FPS)
        self.length = self.cvVideo.get(cv2.CAP_PROP_FRAME_COUNT)
        self.cvVideo.set(cv2.CAP_PROP_POS_FRAMES, self.Slider.value())
        ret, self.frame = self.cvVideo.read()

        ax = self.figVid.add_subplot(111)
        ax.imshow(self.frame)
        self.canvasVid.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = GUI()
    clock.show()
    sys.exit(app.exec_())
