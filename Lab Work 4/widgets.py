from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QListWidget, QListWidgetItem

class PixelGridButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setStyleSheet("background-color: white;")
        self.state = False
        self.clicked.connect(self.click_button)

    def click_button(self):
        self.state = not self.state
        self.setStyleSheet(f"background-color: {'black' if self.state else 'white'};")

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.setStyleSheet(f"background-color: {'black' if self.state else 'white'};")

class PixelGrid(QWidget):
    def __init__(self, x_size, y_size):
        super().__init__()
        self.buttons = []
        layout = QGridLayout()
        for i in range(y_size):
            row = []
            for j in range(x_size):
                button = PixelGridButton()
                row.append(button)
                layout.addWidget(button, i, j)
            self.buttons.append(row)
        self.setLayout(layout)

    def get_grid(self):
        return [1 if button.get_state() else 0 for row in self.buttons for button in row]

    def set_grid(self, grid):
        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
                button.set_state(bool(grid[i][j]))

class KeyValueList(QListWidget):
    def __init__(self):
        super().__init__()

    def clear_list(self):
        self.clear()

    def add_element(self, key, value):
        self.addItem(QListWidgetItem(f'{key}: {value}'))