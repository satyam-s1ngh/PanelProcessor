from pathlib import Path
import time

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QApplication,
    QMessageBox,
    QColorDialog,
    QInputDialog,
    QScrollArea,
)

from PySide6.QtGui import QColor

from core.pipeline import Pipeline
from core.file_manager import FileManager
from core.settings import Settings
from core.preset_manager import PresetManager

from ui.left_panel import LeftPanel
from ui.preview_panel import PreviewPanel
from ui.settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.settings.load()

        self.preset_manager = PresetManager()

        self.images = []
        self.current_index = 0
        self.cancel_processing = False

        self.setWindowTitle("Panel Processor")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.left_panel = LeftPanel()
        self.settings_panel = SettingsPanel()
        self.preview_panel = PreviewPanel()

        self.preview_panel.canvas.set_settings(self.settings)

        self.settings_scroll = QScrollArea()
        self.settings_scroll.setWidgetResizable(True)
        self.settings_scroll.setWidget(self.settings_panel)

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.settings_scroll, 2)
        main_layout.addWidget(self.preview_panel, 2)

        self.connect_signals()
        self.apply_settings_to_ui()
        self.refresh_preset_combo()
        self.restore_last_folders()

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

        self.left_panel.process_current_button.clicked.connect(
            self.process_current_image
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

        self.settings_panel.reset_button.clicked.connect(
            self.reset_settings
        )

        self.settings_panel.apply_preset_button.clicked.connect(
            self.apply_selected_preset
        )

        self.settings_panel.save_preset_button.clicked.connect(
            self.save_new_preset
        )

        self.settings_panel.update_preset_button.clicked.connect(
            self.update_selected_preset
        )

        self.settings_panel.delete_preset_button.clicked.connect(
            self.delete_selected_preset
        )

        self.settings_panel.preview_original_checkbox.toggled.connect(
            self.toggle_original_preview
        )

        self.left_panel.cancel_button.clicked.connect(
            self.request_cancel_processing
        )

    def select_input_folder(self):
        current_folder = self.left_panel.input_path.text()

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder",
            current_folder if current_folder else "",
        )

        if not folder:
            return

        self.left_panel.input_path.setText(folder)

        self.settings.last_input_folder = folder
        self.settings.save()

        self.images = FileManager.get_images(folder)
        self.current_index = 0

        if self.images:
            self.update_preview()

    def select_output_folder(self):
        current_folder = self.left_panel.output_path.text()

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            current_folder if current_folder else "",
        )

        if not folder:
            return

        self.left_panel.output_path.setText(folder)

        self.settings.last_output_folder = folder
        self.settings.save()

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
            QMessageBox.warning(
                self,
                "Missing Folder",
                "Please select both input and output folders.",
            )
            return

        if not self.images:
            QMessageBox.warning(
                self,
                "No Images",
                "Please select an input folder with images.",
            )
            return

        total = len(self.images)
        processed = 0
        skipped = 0
        errors = 0

        skip_existing = self.left_panel.skip_existing_checkbox.isChecked()

        self.reset_processing_ui()

        start_time = time.time()

        for index, image_path in enumerate(self.images, start=1):
            if self.cancel_processing:
                self.update_processing_status(
                    index - 1,
                    total,
                    processed,
                    skipped,
                    errors,
                    start_time,
                )

                self.finish_processing_ui("Cancelled")
                QMessageBox.information(
                    self,
                    "Cancelled",
                    "Processing was cancelled.",
                )
                return

            try:
                default_output_path = self.get_default_output_path(
                    output_folder,
                    image_path,
                )

                if skip_existing and default_output_path.exists():
                    skipped += 1

                    self.update_processing_status(
                        index,
                        total,
                        processed,
                        skipped,
                        errors,
                        start_time,
                    )

                    continue

                output_path = self.get_output_path(
                    output_folder,
                    image_path,
                )

                Pipeline.process_one(
                    image_path,
                    output_path,
                    self.settings,
                )

                processed += 1

            except Exception as error:
                errors += 1
                self.log_error(
                    image_path,
                    error,
                )

            self.update_processing_status(
                index,
                total,
                processed,
                skipped,
                errors,
                start_time,
            )

        self.finish_processing_ui("Processing Complete")

        QMessageBox.information(
            self,
            "Done",
            f"Processing Complete!\n\n"
            f"Processed: {processed}\n"
            f"Skipped: {skipped}\n"
            f"Errors: {errors}",
        )

    def process_current_image(self):
        output_folder = self.left_panel.output_path.text()

        if not output_folder:
            QMessageBox.warning(
                self,
                "No Output Folder",
                "Please select an output folder first.",
            )
            return

        if not self.images:
            QMessageBox.warning(
                self,
                "No Image",
                "Please select an input folder with images first.",
            )
            return

        image_path = self.images[self.current_index]

        skip_existing = self.left_panel.skip_existing_checkbox.isChecked()

        try:
            default_output_path = self.get_default_output_path(
                output_folder,
                image_path,
            )

            if skip_existing and default_output_path.exists():
                QMessageBox.information(
                    self,
                    "Skipped",
                    "This image is already processed.",
                )
                return

            output_path = self.get_output_path(
                output_folder,
                image_path,
            )

            Pipeline.process_one(
                image_path,
                output_path,
                self.settings,
            )

            QMessageBox.information(
                self,
                "Done",
                "Current image processed successfully!",
            )

        except Exception as error:
            self.log_error(
                image_path,
                error,
            )

            QMessageBox.warning(
                self,
                "Error",
                f"Failed to process image:\n{error}",
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
        self.settings.last_input_folder = self.left_panel.input_path.text()
        self.settings.last_output_folder = self.left_panel.output_path.text()

        self.settings.save()
        event.accept()
    
    def reset_settings(self):
        self.settings = Settings()

        self.preview_panel.canvas.set_settings(self.settings)

        self.apply_settings_to_ui()

        self.settings.save()

        self.refresh_preview()

    def get_output_path(self, output_folder, image_path):
        output_path = self.get_default_output_path(
            output_folder,
            image_path,
        )

        if not output_path.exists():
            return output_path

        output_folder = Path(output_folder)

        base_name = image_path.stem
        extension = image_path.suffix

        counter = 1

        while output_path.exists():
            output_path = output_folder / f"{base_name}_processed_{counter}{extension}"
            counter += 1

        return output_path
    
    def refresh_preset_combo(self):
        combo = self.settings_panel.preset_combo

        current_text = combo.currentText()

        combo.blockSignals(True)
        combo.clear()

        preset_names = self.preset_manager.get_names()

        if preset_names:
            combo.addItems(preset_names)

            if current_text in preset_names:
                combo.setCurrentText(current_text)

        combo.blockSignals(False)

    def apply_settings_data(self, data):
        if not data:
            return

        for key, value in data.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)

        self.preview_panel.canvas.set_settings(self.settings)

        self.apply_settings_to_ui()
        self.settings.save()
        self.refresh_preview()

    def apply_selected_preset(self):
        name = self.settings_panel.preset_combo.currentText()

        if not name:
            QMessageBox.warning(
                self,
                "No Preset",
                "Please select a preset first.",
            )
            return

        preset_data = self.preset_manager.get_preset(name)

        if not preset_data:
            QMessageBox.warning(
                self,
                "Preset Not Found",
                "This preset could not be found.",
            )
            return

        self.apply_settings_data(preset_data)

    def save_new_preset(self):
        name, ok = QInputDialog.getText(
            self,
            "Save Preset",
            "Enter preset name:",
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        self.preset_manager.save_preset(
            name,
            self.settings.to_dict(),
        )

        self.refresh_preset_combo()
        self.settings_panel.preset_combo.setCurrentText(name)

    def update_selected_preset(self):
        name = self.settings_panel.preset_combo.currentText()

        if not name:
            QMessageBox.warning(
                self,
                "No Preset",
                "Please select a preset to update.",
            )
            return

        confirm = QMessageBox.question(
            self,
            "Update Preset",
            f"Update preset '{name}' with current settings?",
        )

        if confirm != QMessageBox.Yes:
            return

        self.preset_manager.save_preset(
            name,
            self.settings.to_dict(),
        )

        self.refresh_preset_combo()
        self.settings_panel.preset_combo.setCurrentText(name)

    def delete_selected_preset(self):
        name = self.settings_panel.preset_combo.currentText()

        if not name:
            QMessageBox.warning(
                self,
                "No Preset",
                "Please select a preset to delete.",
            )
            return

        confirm = QMessageBox.question(
            self,
            "Delete Preset",
            f"Delete preset '{name}'?",
        )

        if confirm != QMessageBox.Yes:
            return

        self.preset_manager.delete_preset(name)

        self.refresh_preset_combo()
    
    def restore_last_folders(self): 
        input_folder = getattr(
            self.settings,
            "last_input_folder",
            "",
        )

        output_folder = getattr(
            self.settings,
            "last_output_folder",
            "",
        )

        if input_folder and Path(input_folder).exists():
            self.left_panel.input_path.setText(input_folder)

            self.images = FileManager.get_images(input_folder)
            self.current_index = 0

            if self.images:
                self.update_preview()

        if output_folder and Path(output_folder).exists():
            self.left_panel.output_path.setText(output_folder)
    
    def toggle_original_preview(self, enabled):
        self.preview_panel.canvas.set_show_original(enabled)

    def request_cancel_processing(self):
        self.cancel_processing = True
        self.left_panel.processing_status.setText("Cancelling...")

    def reset_processing_ui(self):
        self.cancel_processing = False

        self.left_panel.process_button.setEnabled(False)
        self.left_panel.process_current_button.setEnabled(False)
        self.left_panel.cancel_button.setEnabled(True)

        self.left_panel.progress.setValue(0)
        self.left_panel.error_log.clear()
        self.left_panel.processing_status.setText("Starting...")
        self.left_panel.eta_label.setText("ETA: calculating...")

    def finish_processing_ui(self, message="Done"):
        self.left_panel.process_button.setEnabled(True)
        self.left_panel.process_current_button.setEnabled(True)
        self.left_panel.cancel_button.setEnabled(False)

        self.left_panel.processing_status.setText(message)
        self.left_panel.eta_label.setText("ETA: --")

    def format_seconds(self, seconds):
        seconds = max(0, int(seconds))

        minutes = seconds // 60
        seconds = seconds % 60

        return f"{minutes:02d}:{seconds:02d}"
   
    def update_processing_status(
        self,
        current,
        total,
        processed,
        skipped,
        errors,
        start_time,
    ):
        progress = int(current / total * 100) if total else 0
        self.left_panel.progress.setValue(progress)

        self.left_panel.processing_status.setText(
            f"Processing {current} / {total} | "
            f"Done: {processed} | "
            f"Skipped: {skipped} | "
            f"Errors: {errors}"
        )

        elapsed = time.time() - start_time

        if current > 0:
            average_time = elapsed / current
            remaining_items = total - current
            eta = average_time * remaining_items

            self.left_panel.eta_label.setText(
                f"ETA: {self.format_seconds(eta)}"
            )

        QApplication.processEvents()

    def log_error(self, image_path, error):
        self.left_panel.error_log.appendPlainText(
            f"{image_path.name} -> {error}"
        )

    def get_default_output_path(self, output_folder, image_path):
        output_folder = Path(output_folder)

        base_name = image_path.stem
        extension = image_path.suffix

        return output_folder / f"{base_name}_processed{extension}"