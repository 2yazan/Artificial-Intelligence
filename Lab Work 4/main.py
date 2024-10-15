# Development and research of training algorithms for artificial neural networks.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from widgets import PixelGrid, KeyValueList
import numpy as np
from model import Model

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pattern Recognition")
        self.model = Model()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.grid = PixelGrid(7, 7)
        self.recognize_button = QPushButton('Recognize')
        self.recognize_button.clicked.connect(self.test_command)
        left_layout.addWidget(self.grid)
        left_layout.addWidget(self.recognize_button)

        self.result_list = KeyValueList()

        right_layout = QVBoxLayout()
        self.p_label = QLabel('Standard of training')
        self.e_label = QLabel('Number of eras')
        self.p_tbox = QLineEdit()
        self.e_tbox = QLineEdit()
        self.train_button = QPushButton('Teach')
        self.train_button.clicked.connect(self.train_command)

        right_layout.addWidget(self.p_label)
        right_layout.addWidget(self.p_tbox)
        right_layout.addWidget(self.e_label)
        right_layout.addWidget(self.e_tbox)
        right_layout.addWidget(self.train_button)
        right_layout.addStretch(1)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.result_list)
        main_layout.addLayout(right_layout)

    def train_command(self):
        self.model.train(int(self.e_tbox.text()), float(self.p_tbox.text()))

    def test_command(self):
        class_label_list = ['/', '-', '*', '+', '%', 'root']
        result = self.model.test(np.array(self.grid.get_grid()))
        self.result_list.clear_list()
        for i, j in zip(class_label_list, result):
            self.result_list.add_element(i, round(j, 3))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())