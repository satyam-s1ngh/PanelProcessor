import os
from core.settings import Settings
from ui.settings_panel import SettingsPanel
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
        
        self.settings = Settings()
        self.images = []
        self.current_index = 0

        self.setWindowTitle("Panel Processor")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

       # Create panels

        self.left_panel = LeftPanel()
        self.preview_panel = PreviewPanel()

        # Temporary center panel (Settings placeholder)

        self.settings_panel = SettingsPanel()

        # Main layout

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.settings_panel, 2)
        main_layout.addWidget(self.preview_panel, 2)

        # Connect buttons

        self.left_panel.input_button.clicked.connect(self.select_input_folder)
        self.preview_panel.navigation.previous_button.clicked.connect(
            self.previous_image
            )

        self.preview_panel.navigation.next_button.clicked.connect(
            self.next_image
        )
        self.left_panel.output_button.clicked.connect(self.select_output_folder)

        self.settings_panel.border_spinbox.valueChanged.connect(self.update_border_value)
        

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

        self.images = []

        for file in sorted(os.listdir(folder)):
            if file.lower().endswith(supported):
                self.images.append(os.path.join(folder, file))

        self.current_index = 0

        if self.images:
            self.update_preview()


    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:
            self.left_panel.output_path.setText(folder)

    def update_preview(self):
        if not self.images:
            return

        self.preview_panel.show_image(
            self.images[self.current_index]
        )

        self.preview_panel.navigation.counter.setText(
            f"{self.current_index + 1} / {len(self.images)}"
        )

    def previous_image(self):
        if not self.images:
            return

        if self.current_index > 0:
            self.current_index -= 1
            self.update_preview()

    def next_image(self):
        if not self.images:
            return

        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.update_preview()

    def update_border_value(self, value):
        self.settings.border_thickness = value
        self.preview_panel.canvas.set_border_thickness(
            self.settings.border_thickness
        )