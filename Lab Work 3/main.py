# using the ant colony algorithm for solving the traveling salesman problem.

import sys
import pyqtgraph as pg
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QGridLayout, QSizePolicy
from ant import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ant algorithm")
        self.setMinimumSize(1100, 650)
        self.aa = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        parameters = [
            ("Number of algorithm iterations", "iterationsEdit", "100"),
            ("Number of ants", "antsEdit", "10"),
            ("Number of elite ants", "eliteAntsEdit", "2"),
            ("Number of graph vertices", "nEdit", "10"),
            ("Pheromone weight", "alphaEdit", "1"),
            ("Heuristic coefficient", "betaEdit", "1"),
            ("Evaporation coefficient", "rhoEdit", "0.9"),
        ]

        for label_text, edit_name, default_value in parameters:
            label = QLabel(label_text)
            line_edit = QLineEdit(default_value)
            setattr(self, edit_name, line_edit)
            left_layout.addWidget(label)
            left_layout.addWidget(line_edit)

        self.setParametersButton = QPushButton("Set parameters")
        self.setParametersButton.clicked.connect(self.getParameters)
        left_layout.addWidget(self.setParametersButton)
        left_layout.addStretch(1)

        self.graphLayout = QVBoxLayout()
        self.win = pg.GraphicsLayoutWidget(show=True)
        pg.setConfigOptions(antialias=True)
        self.graphLayout.addWidget(self.win)

        top_layout.addLayout(left_layout, 1)
        top_layout.addLayout(self.graphLayout, 2)

        self.table = QTableWidget()
        self.table.setMinimumHeight(300)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        self.posx = []
        self.posy = []
        self.getParameters()

    def showPlot(self):
        self.win.clear()
        pos = []
        r = int(self.nEdit.text())
        angle = 0
        delta = 360 / r
        v = self.aa.getPh()
        self.posx = []
        self.posy = []
        for i in range(r):
            self.posx.append(r * math.cos(angle))
            self.posy.append(r * math.sin(angle))
            angle += delta
            pass

        self.win.addPlot(x=self.posx, y=self.posy, symbolBrush=(255, 0, 0), symbolPen='w')

    def fillTable(self):
        self.table.clear()

        ph = self.aa.getPh()

        self.table.setColumnCount(4)
        self.table.setRowCount(len(ph))

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.setColumnWidth(0, 100)

        self.table.setHorizontalHeaderLabels(["From", "To", "Cost", "Pheromones"])

        costs = self.aa.getDistances()
        pos = 0
        for currentPh in ph:
            self.table.setItem(pos, 0, QTableWidgetItem("{}".format(currentPh[0])))
            self.table.setItem(pos, 1, QTableWidgetItem("{}".format(currentPh[1])))
            self.table.setItem(pos, 2, QTableWidgetItem("{}".format(costs[currentPh[0]][currentPh[1]])))
            self.table.setItem(pos, 3, QTableWidgetItem("{}".format(round(currentPh[2], 4))))
            pos += 1

    def getParameters(self):
        n = int(self.nEdit.text())
        iterations = int(self.iterationsEdit.text())
        antsCount = int(self.antsEdit.text())
        eliteAntsCount = int(self.eliteAntsEdit.text())
        alpha = float(self.alphaEdit.text())
        beta = float(self.betaEdit.text())
        rho = float(self.rhoEdit.text())
        self.aa = AntAlgorithm(n, iterations, antsCount, eliteAntsCount, alpha, beta, rho)
        self.aa.perform()
        self.showPlot()
        self.fillTable()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
