from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

from ui.image_canvas import ImageCanvas
from ui.navigation_bar import NavigationBar


class PreviewPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🖼 Live Preview")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Image Canvas
        self.canvas = ImageCanvas()
        layout.addWidget(self.canvas)

        # Navigation Bar
        self.navigation = NavigationBar()
        layout.addWidget(self.navigation)

    def show_image(self, image_path):
        self.canvas.set_image(image_path)
        