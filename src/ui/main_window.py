from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QApplication,
    QMessageBox,
    QColorDialog,
)

from PySide6.QtGui import QColor

from core.pipeline import Pipeline
from core.file_manager import FileManager
from core.settings import Settings

from ui.left_panel import LeftPanel
from ui.preview_panel import PreviewPanel
from ui.settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.settings.load()

        self.images = []
        self.current_index = 0

        self.setWindowTitle("Panel Processor")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.left_panel = LeftPanel()
        self.settings_panel = SettingsPanel()
        self.preview_panel = PreviewPanel()

        self.preview_panel.canvas.set_settings(self.settings)

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.settings_panel, 2)
        main_layout.addWidget(self.preview_panel, 2)

        self.connect_signals()
        self.apply_settings_to_ui()

    def connect_signals(self):
        self.left_panel.input_button.clicked.connect(
            self.select_input_folder
        )

        self.left_panel.output_button.clicked.connect(
            self.select_output_folder
        )

        self.left_panel.process_button.clicked.connect(
            self.process_images
        )

        self.preview_panel.navigation.previous_button.clicked.connect(
            self.previous_image
        )

        self.preview_panel.navigation.next_button.clicked.connect(
            self.next_image
        )

        self.settings_panel.border_spinbox.valueChanged.connect(
            self.update_border_value
        )

        self.settings_panel.custom_color_button.clicked.connect(
            self.choose_border_color
        )

        self.settings_panel.border_color.currentTextChanged.connect(
            self.update_border_color
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

        self.settings_panel.background_checkbox.toggled.connect(
            self.update_background_enabled
        )

        self.settings_panel.background_color_button.clicked.connect(
            self.choose_background_color
        )

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder",
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
            "Select Output Folder",
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
        self.settings.border_thickness = float(value)
        self.refresh_preview()

    def update_border_color(self, color):
        if color == "Custom":
            return

        self.settings.border_color = color.lower()
        self.refresh_preview()

    def choose_border_color(self):
        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.border_color = color.name()

        self.settings_panel.border_color.blockSignals(True)
        self.settings_panel.border_color.setCurrentText("Custom")
        self.settings_panel.border_color.blockSignals(False)

        self.update_color_button(
            self.settings_panel.custom_color_button,
            "Border Color",
            color.name(),
        )

        self.refresh_preview()

    def update_corner_radius(self, value):
        self.settings.corner_radius = int(value)
        self.refresh_preview()

    def update_shadow(self, enabled):
        self.settings.shadow_enabled = bool(enabled)
        self.refresh_preview()

    def choose_shadow_color(self):
        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.shadow_color = color.name()

        self.update_color_button(
            self.settings_panel.shadow_color_button,
            "Shadow Color",
            color.name(),
        )

        self.refresh_preview()

    def update_shadow_blur(self, value):
        self.settings.shadow_blur = int(value)
        self.refresh_preview()

    def update_shadow_offset_x(self, value):
        self.settings.shadow_offset_x = int(value)
        self.refresh_preview()

    def update_shadow_offset_y(self, value):
        self.settings.shadow_offset_y = int(value)
        self.refresh_preview()

    def update_shadow_opacity(self, value):
        self.settings.shadow_opacity = int(value)
        self.refresh_preview()

    def update_background_enabled(self, enabled):
        self.settings.background_enabled = bool(enabled)
        self.refresh_preview()

    def choose_background_color(self):
        color = QColorDialog.getColor()

        if not color.isValid():
            return

        self.settings.background_color = color.name()

        self.update_color_button(
            self.settings_panel.background_color_button,
            "Background Color",
            color.name(),
        )

        self.refresh_preview()

    def process_images(self):
        input_folder = self.left_panel.input_path.text()
        output_folder = self.left_panel.output_path.text()

        if not input_folder or not output_folder:
            return

        if not self.images:
            QMessageBox.warning(
                self,
                "No Images",
                "Please select an input folder with images.",
            )
            return

        total = len(self.images)

        self.left_panel.process_button.setEnabled(False)
        self.left_panel.progress.setValue(0)

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

        self.left_panel.process_button.setEnabled(True)

        QMessageBox.information(
            self,
            "Done",
            "Processing Complete!",
        )

    def apply_settings_to_ui(self):
        panel = self.settings_panel

        widgets = [
            panel.border_spinbox,
            panel.border_color,
            panel.custom_color_button,
            panel.corner_radius,
            panel.shadow_checkbox,
            panel.shadow_blur,
            panel.shadow_offset_x,
            panel.shadow_offset_y,
            panel.shadow_opacity,
            panel.shadow_color_button,
            panel.background_checkbox,
            panel.background_color_button,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        try:
            panel.border_spinbox.set_border_value(
                float(self.settings.border_thickness)
            )

            border_color = str(self.settings.border_color)

            if border_color.lower() == "black":
                panel.border_color.setCurrentText("Black")
            elif border_color.lower() == "white":
                panel.border_color.setCurrentText("White")
            else:
                panel.border_color.setCurrentText("Custom")

            self.update_color_button(
                panel.custom_color_button,
                "Border Color",
                self.settings.border_color,
            )

            panel.corner_radius.setValue(
                int(self.settings.corner_radius)
            )

            panel.shadow_checkbox.setChecked(
                bool(self.settings.shadow_enabled)
            )

            panel.shadow_blur.setValue(
                int(self.settings.shadow_blur)
            )

            panel.shadow_offset_x.setValue(
                int(self.settings.shadow_offset_x)
            )

            panel.shadow_offset_y.setValue(
                int(self.settings.shadow_offset_y)
            )

            panel.shadow_opacity.setValue(
                int(self.settings.shadow_opacity)
            )

            self.update_color_button(
                panel.shadow_color_button,
                "Shadow Color",
                self.settings.shadow_color,
            )

            panel.background_checkbox.setChecked(
                bool(self.settings.background_enabled)
            )

            self.update_color_button(
                panel.background_color_button,
                "Background Color",
                self.settings.background_color,
            )

        finally:
            for widget in widgets:
                widget.blockSignals(False)

        self.refresh_preview()

    def update_color_button(self, button, label, color_value):
        color = QColor(str(color_value))

        if not color.isValid():
            color = QColor("#000000")

        hex_color = color.name().upper()

        brightness = (
            color.red() * 0.299
            + color.green() * 0.587
            + color.blue() * 0.114
        )

        text_color = "#000000" if brightness > 160 else "#FFFFFF"

        button.setText(
            f"{label}: {hex_color}"
        )

        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {hex_color};
                color: {text_color};
            }}
            """
        )

    def refresh_preview(self):
        self.preview_panel.canvas.set_settings(self.settings)
        self.preview_panel.canvas.update()

    def closeEvent(self, event):
        self.settings.save()
        event.accept()