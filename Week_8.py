import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Минималистичный видеоплеер")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)
        
        self.file_path_label = QLabel("Путь к файлу: Нет файла", self)

        self.play_button = QPushButton("Воспроизвести", self)
        self.pause_button = QPushButton("Пауза", self)
        self.stop_button = QPushButton("Стоп", self)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 100)
        
        layout.addWidget(self.video_widget)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(QLabel("Громкость"))
        layout.addWidget(self.volume_slider)
        layout.addWidget(QLabel("Позиция"))
        layout.addWidget(self.position_slider)

        central_widget.setLayout(layout)

        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)

        self.volume_slider.valueChanged.connect(self.set_volume)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.media_player.positionChanged.connect(self.update_position_slider)

        self.media_player.mediaStatusChanged.connect(self.check_media_status)

        self.show()

    def play_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть видео файл", "", "Видео файлы (*.mp4 *.avi *.mov)")
        if file_path:
            self.file_path_label.setText(f"Путь к файлу: {file_path}")
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()

    def set_volume(self):
        volume = self.volume_slider.value()
        self.media_player.setVolume(volume)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position_slider(self, position):
        self.position_slider.setValue(position)

    def check_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.stop_video()

def main():
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
