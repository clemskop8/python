import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Нажми меня!")
        self.label = QLabel("Текст не изменен")

        self.button.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.label.setStyleSheet("font-size: 18px; color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.button.clicked.connect(self.on_button_click)

        self.setWindowTitle("Пример с кнопкой и меткой")
        self.setGeometry(100, 100, 300, 200)

    def on_button_click(self):
        self.label.setText("Кнопка нажата!")
        
        self.button.setStyleSheet("background-color: lightgreen; font-size: 18px; padding: 12px;")
        self.label.setStyleSheet("font-size: 22px; color: blue;")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
