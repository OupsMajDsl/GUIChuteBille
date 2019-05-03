import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QLabel, QCheckBox, QComboBox,
                            QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox,
<<<<<<< HEAD
                            QSpacerItem, QFrame, QSlider)
=======
                            QSpacerItem, QFrame, QSlider, QLineEdit)
>>>>>>> 2bdc20a6af37c348185332444f6ed6e9ac2fa088
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class GUI(QDialog):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Ploc")
        self.pathVid = "/media/mathieu/Nouveau nom/videos_bille/{}.avi"
        self.pathTxt = "/media/mathieu/Nouveau nom/mesures_acous/{}.txt"

        self.filename = "mes_cam_bille1_1"

        self.Objets()
        self.display()

    def Objets(self):
        self.filename = QLineEdit("Entrez le nom de la mesure à charger")
        self.load = QPushButton("Charger")
        self.load.clicked.connect(self.loadFiles)

        self.figSpec = Figure(figsize=(8, 4), dpi=100)
        self.figTemp = Figure(figsize=(8, 4), dpi=100)
        self.figMicro = Figure(figsize=(8, 4), dpi=100)
        self.figSign = Figure(figsize=(15, 3), dpi=100)

        self.canvasSpec = FigureCanvas(self.figSpec)
        self.canvasTemp = FigureCanvas(self.figTemp)
        self.canvasMicro = FigureCanvas(self.figMicro)
        self.canvasSign = FigureCanvas(self.figSign)

        # self.toolbarSpec = NavigationToolbar(self.canvasSpec, self)
        self.Slider = QSlider(Qt.Horizontal)

    def display(self):
        MainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.video, 0, 0)
        grid.addWidget(self.canvasSpec, 1, 0)
        grid.addWidget(self.canvasTemp, 0, 1)
        grid.addWidget(self.canvasMicro, 1, 1)

        HLayout = QHBoxLayout()
        HLayout.addWidget(self.filename)
        HLayout.addWidget(self.load)
        MainLayout.addLayout(HLayout)
        MainLayout.addLayout(grid)
        MainLayout.addWidget(self.canvasSign)
        MainLayout.addWidget(self.Slider)
        self.setLayout(MainLayout)

<<<<<<< HEAD
    def testVideo(self):
        path = "/media/mathieu/Nouveau nom/videos_bille/{}.avi".format(self.filename)
        self.cvVideo = cv2.VideoCapture(path)
=======

    def loadFiles(self):
        filename = self.filename.text()
        self.cvVideo = cv2.VideoCapture(self.pathVid.format(filename))
        self.data = np.loadtxt(self.pathTxt.format(filename))

        self.plot()


    def plot(self):
        time = self.data[:, 0]
        micro = self.data[:, 1]
        hydro = self.data[:, 2]

        ax = self.figSign.add_subplot(111)
        ax.plot(time, hydro)

    def testVideo(self):
>>>>>>> 2bdc20a6af37c348185332444f6ed6e9ac2fa088
        length = int(self.cvVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cvVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cvVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        rate = int(self.cvVideo.get(cv2.CAP_PROP_POS_FRAMES))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = GUI()
    clock.show()
    sys.exit(app.exec_())
