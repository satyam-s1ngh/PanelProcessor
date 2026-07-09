import os
from PySide6.QtWidgets import QColorDialog
from pathlib import Path
from core.pipeline import Pipeline
from core.file_manager import FileManager
from core.settings import Settings
from ui.settings_panel import SettingsPanel
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QApplication,
    QMessageBox,
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
        self.preview_panel.canvas.set_settings(self.settings)

        # Temporary center panel (Settings placeholder)

        self.settings_panel = SettingsPanel()

        # Main layout

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.settings_panel, 2)
        main_layout.addWidget(self.preview_panel, 2)

        # Connect buttons

        self.settings_panel.background_checkbox.toggled.connect(
            self.update_background_enabled
        )

        self.settings_panel.background_color_button.clicked.connect(
            self.choose_background_color
        )

        self.left_panel.input_button.clicked.connect(self.select_input_folder)
        self.preview_panel.navigation.previous_button.clicked.connect(
            self.previous_image
            )

        self.preview_panel.navigation.next_button.clicked.connect(
            self.next_image
        )
        self.left_panel.output_button.clicked.connect(self.select_output_folder)

        self.settings_panel.border_spinbox.valueChanged.connect(self.update_border_value)
        self.left_panel.process_button.clicked.connect(
            self.process_images
        )

        self.settings_panel.custom_color_button.clicked.connect(
            self.choose_border_color
        )

        self.settings_panel.corner_radius.valueChanged.connect(
        self.update_corner_radius
        )

        self.settings_panel.shadow_checkbox.toggled.connect(
        self.update_shadow
        )

        self.settings_panel.shadow_color_button.clicked.connect(
            self.choose_shadow_color
        )

        self.settings_panel.shadow_blur.valueChanged.connect(
            self.update_shadow_blur
        )

        self.settings_panel.shadow_offset_x.valueChanged.connect(
            self.update_shadow_offset_x
        )

        self.settings_panel.shadow_offset_y.valueChanged.connect(
            self.update_shadow_offset_y
        )

        self.settings_panel.shadow_opacity.valueChanged.connect(
            self.update_shadow_opacity
        )
                        
    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder"
        )

        if not folder:
            return

        self.left_panel.input_path.setText(folder)

        self.images = FileManager.get_images(folder)

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
            str(self.images[self.current_index])
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

        self.settings_panel.border_color.currentTextChanged.connect(
        self.update_border_color
        )

        self.preview_panel.canvas.set_settings(self.settings)
        self.preview_panel.canvas.update()

    def update_border_color(self, color):
        self.settings.border_color = color.lower()
        self.preview_panel.canvas.update()

    def process_images(self):
        input_folder = self.left_panel.input_path.text()
        output_folder = self.left_panel.output_path.text()

        if not input_folder or not output_folder:
            return

        total = len(self.images)

        self.left_panel.process_button.setEnabled(False)

        for index, image_path in enumerate(self.images, start=1):
            output_path = Path(output_folder) / image_path.name

            Pipeline.process_one(
                image_path,
                output_path,
                self.settings,
            )

            progress = int(index / total * 100)

            self.left_panel.progress.setValue(progress)

            QApplication.processEvents()

        from PySide6.QtWidgets import QMessageBox

        self.left_panel.process_button.setEnabled(True)

        QMessageBox.information(
            self,
            "Done",
            "Processing Complete!"
        )

    def choose_border_color(self):

        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.border_color = color.name()

        self.settings_panel.custom_color_button.setText(
            f"Border Color: {color.name().upper()}"
        )

        self.settings_panel.custom_color_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
            }}
            """
        )
        self.preview_panel.canvas.update()

    def update_border_color(self, color):
        if color == "Custom":
            return

        self.settings.border_color = color.lower()
        self.preview_panel.canvas.update()

    def update_corner_radius(self, value):
        self.settings.corner_radius = value
        self.preview_panel.canvas.update()

    def choose_shadow_color(self):

        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.shadow_color = color.name()

        self.settings_panel.shadow_color_button.setText(
            f"Shadow Color: {color.name().upper()}"
        )

        self.settings_panel.shadow_color_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
            }}
            """
        )

        self.preview_panel.canvas.update()    
    
    def update_shadow(self, enabled):
        self.settings.shadow_enabled = enabled
        self.preview_panel.canvas.update()

    def update_shadow_blur(self, value):
        self.settings.shadow_blur = value
        self.preview_panel.canvas.update()

    def update_shadow_offset_x(self, value):
        self.settings.shadow_offset_x = value
        self.preview_panel.canvas.update()

    def update_shadow_offset_y(self, value):
        self.settings.shadow_offset_y = value
        self.preview_panel.canvas.update()

    def update_shadow_opacity(self, value):
        self.settings.shadow_opacity = value
        self.preview_panel.canvas.update()

    def update_background_enabled(self, enabled):
        self.settings.background_enabled = enabled
        self.preview_panel.canvas.update()


    def choose_background_color(self):
        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.background_color = color.name()

        self.settings_panel.background_color_button.setText(
            f"Background Color: {color.name().upper()}"
        )

        self.settings_panel.background_color_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
            }}
            """
        )

        self.preview_panel.canvas.update()