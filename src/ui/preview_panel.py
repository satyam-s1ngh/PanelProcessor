from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class PreviewPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("🖼 Live Preview")
        title.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 600)

        layout.addWidget(title)
        layout.addWidget(self.image_label)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.image_label.setText("Failed to load image")
            return

        scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.image_label.setPixmap(scaled)