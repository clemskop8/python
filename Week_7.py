import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QMenuBar, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import QFile, QTextStream

class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Новая заметка")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def get_text(self):
        return self.text_edit.toPlainText()

    def set_text(self, text):
        self.text_edit.setPlainText(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для заметок")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Файл")

        new_action = QAction("Новая заметка", self)
        new_action.triggered.connect(self.new_note)

        save_action = QAction("Сохранить заметку", self)
        save_action.triggered.connect(self.save_note)

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)

        self.note_window = None

    def new_note(self):
        if self.note_window is None or not self.note_window.isVisible():
            self.note_window = NoteWindow()
            self.note_window.show()

    def save_note(self):
        if self.note_window is None:
            return
        
        text = self.note_window.get_text()
        
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить заметку", "", "Text Files (*.txt);;All Files (*)")
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
