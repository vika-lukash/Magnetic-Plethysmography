from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox,  QPushButton, QWidget, QComboBox, QGridLayout, QLabel, QFileDialog
import matplotlib.pyplot as plt


class PlotWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUI()


    def setupUI(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        refreshButton = QPushButton("Выбрать")
        refreshButton.clicked.connect(self.choose_directory)
        refreshButton.setMaximumWidth(150)
        refreshButton.setMinimumWidth(150)
        self.layout.addWidget(refreshButton, 5, 0)

        self.image = QLabel()
        self.layout.addWidget(self.image, 0, 0, 5, 1)


    def choose_directory(self):
        input_dir = QFileDialog.getOpenFileName()
        port1 = []
        port2 = []

        absPath = input_dir[0].split("/")

        path = absPath[-2] + "/" + absPath[-1]

        with open(path, "r") as file:
            for line in file:
                port1.append(int(line.split(" ")[0]))
                port2.append(int(line.split(" ")[1]))

        print("U1 = ", port1)
        print("U2 = ", port2)

        plt.figure()
        plt.subplot(211)
        plt.plot(range(len(port1)), port1)
        plt.title("Напряжение порт 1")

        plt.subplot(212)
        plt.title("Ток")
        plt.plot(range(len(port2)), port2)
        plt.tight_layout()
        plt.savefig("Напряжение порт 2")

        self.image.setPixmap(QPixmap("plot.png"))

