import os
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
)

from ui.left_panel import LeftPanel
from ui.preview_panel import PreviewPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Panel Processor")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

       # Create panels

        self.left_panel = LeftPanel()
        self.preview_panel = PreviewPanel()

        # Temporary center panel (Settings placeholder)

        center_panel = QWidget()

        # Main layout

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(center_panel, 2)
        main_layout.addWidget(self.preview_panel, 2)

        # Connect buttons

        self.left_panel.input_button.clicked.connect(self.select_input_folder)
        self.left_panel.output_button.clicked.connect(self.select_output_folder)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder"
        )

        if not folder:
            return

        self.left_panel.input_path.setText(folder)

        supported = (
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        )

        images = [
            file for file in os.listdir(folder)
            if file.lower().endswith(supported)
        ]

        if images:
            first_image = os.path.join(folder, images[0])
            self.preview_panel.show_image(first_image)


    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:
            self.left_panel.output_path.setText(folder)