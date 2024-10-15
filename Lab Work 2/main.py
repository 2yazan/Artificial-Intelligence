# Study of the description methodology and development technology of the ART1 (Adaptive Resonance Theory)
#  algorithm using the example of solving a classification problem.

from ART import ART1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QLabel, QPushButton, QTextEdit, QWidget, QMessageBox, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ART1 Algorithm")

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        top_layout.addWidget(self.logs, 1)

        entries_layout = QVBoxLayout()

        self.max_items_edit = QLineEdit()
        self.max_customers_edit = QLineEdit()
        self.total_prototype_vectors_edit = QLineEdit()
        self.beta_edit = QLineEdit()
        self.vigilance_edit = QLineEdit()

        entries_layout.addWidget(QLabel("Max Items:"))
        entries_layout.addWidget(self.max_items_edit)

        entries_layout.addWidget(QLabel("Max Customers:"))
        entries_layout.addWidget(self.max_customers_edit)

        entries_layout.addWidget(QLabel("Total Prototype Vectors:"))
        entries_layout.addWidget(self.total_prototype_vectors_edit)

        entries_layout.addWidget(QLabel("Beta:"))
        entries_layout.addWidget(self.beta_edit)

        entries_layout.addWidget(QLabel("Vigilance:"))
        entries_layout.addWidget(self.vigilance_edit)

        self.get_recommendations_button = QPushButton("Get Recommendations")
        entries_layout.addWidget(self.get_recommendations_button)

        top_layout.addLayout(entries_layout, 1)

        main_layout.addLayout(top_layout)

        self.database_table_widget = QTableWidget()
        main_layout.addWidget(self.database_table_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.get_recommendations_button.clicked.connect(self.get_values)

        self.max_items = 11
        self.max_customers = 10
        self.total_prototype_vectors = 5
        self.beta = 1.0
        self.vigilance = 0.9

        self.max_items_edit.setText(str(self.max_items))
        self.max_customers_edit.setText(str(self.max_customers))
        self.total_prototype_vectors_edit.setText(str(self.total_prototype_vectors))
        self.beta_edit.setText(str(self.beta))
        self.vigilance_edit.setText(str(self.vigilance))

        self.art = ART1()
        self.art.set_debug_values()
        self.art.perform()
        database_table = self.art.get_database()
        self.fill_table(self.database_table_widget, database_table)
        self.show_clusters()

    def setup_art(self):
        self.art = ART1()
        self.art.set_parameters(self.max_items, self.max_customers,
                                self.total_prototype_vectors,
                                self.beta, self.vigilance)
        self.art.set_random_database()
        self.art.perform()
        database_table = self.art.get_database()

        self.fill_table(self.database_table_widget, database_table)
        self.show_clusters()

    def show_clusters(self):
        self.logs.clear()
        self.logs.setPlainText(self.art.get_clusters())

    def fill_table(self, table, data):
        table.setColumnCount(0)
        table.setRowCount(0)

        table.setColumnCount(len(data[0]))
        table.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, len(data[0])):
                table.setItem(i, j, QTableWidgetItem(str(data[i][j])))

        column_width = 30
        for i in range(table.columnCount()):
            table.setColumnWidth(i, column_width)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

    def show_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Warning")
        msg.setText("Please enter the parameters!")
        msg.exec_()

    def is_valid(self, data):
        return not data == ''

    def get_values(self):
        t = self.max_items_edit.text()
        if self.is_valid(t):
            self.max_items = int(t)
        else:
            self.show_warning()
            return

        t = self.max_customers_edit.text()
        if self.is_valid(t):
            self.max_customers = int(t)
        else:
            self.show_warning()
            return

        t = self.total_prototype_vectors_edit.text()
        if self.is_valid(t):
            self.total_prototype_vectors = int(t)
        else:
            self.show_warning()
            return

        t = self.beta_edit.text()
        if self.is_valid(t):
            self.beta = float(t)
        else:
            self.show_warning()
            return

        t = self.vigilance_edit.text()
        if self.is_valid(t):
            self.vigilance = float(t)
        else:
            self.show_warning()
            return

        self.setup_art()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setMinimumSize(720, 720)
    window.show()
    sys.exit(app.exec_())
