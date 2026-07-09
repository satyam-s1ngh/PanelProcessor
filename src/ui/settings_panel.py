from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QCheckBox,
    QWidget,
    QLineEdit,
)
from PySide6.QtCore import Qt, Signal


class NumberControl(QWidget):
    valueChanged = Signal(float)

    def __init__(
        self,
        minimum=0,
        maximum=100,
        step=1,
        decimals=0,
        suffix="",
        default=0,
    ):
        super().__init__()

        self.minimum = float(minimum)
        self.maximum = float(maximum)
        self.step = float(step)
        self.decimals = int(decimals)
        self.suffix = suffix
        self._value = float(default)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.minus_button = QPushButton("-")
        self.input = QLineEdit()
        self.plus_button = QPushButton("+")

        self.input.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.minus_button)
        layout.addWidget(self.input)

        if self.suffix:
            layout.addWidget(QLabel(self.suffix))

        layout.addWidget(self.plus_button)

        self.minus_button.clicked.connect(self.decrease)
        self.plus_button.clicked.connect(self.increase)
        self.input.editingFinished.connect(self.apply_text_value)

        self.setValue(self._value)

    def increase(self):
        self.setValue(
            self._value + self.step,
            emit=True,
        )

    def decrease(self):
        self.setValue(
            self._value - self.step,
            emit=True,
        )

    def apply_text_value(self):
        text = self.input.text()
        text = text.replace(self.suffix, "").strip()

        try:
            value = float(text)
        except ValueError:
            self.update_text()
            return

        value = round(value / self.step) * self.step

        self.setValue(
            value,
            emit=True,
        )

    def setValue(self, value, emit=False):
        value = max(
            self.minimum,
            min(
                self.maximum,
                float(value),
            ),
        )

        self._value = value
        self.update_text()

        if emit:
            self.valueChanged.emit(self._value)

    def value(self):
        return self._value

    def update_text(self):
        if self.decimals == 0:
            self.input.setText(
                str(int(round(self._value)))
            )
        else:
            self.input.setText(
                f"{self._value:.{self.decimals}f}"
            )

    def set_border_value(self, value):
        self.setValue(
            float(value),
            emit=False,
        )

    def border_value(self):
        return self._value


class SettingsPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.background_checkbox = QCheckBox("Use Background Color")
        layout.addWidget(self.background_checkbox)

        self.background_color_button = QPushButton("Background Color: #FFFFFF")
        layout.addWidget(self.background_color_button)

        layout.addWidget(QLabel("Border Thickness"))
        self.border_spinbox = NumberControl(
            minimum=0,
            maximum=100,
            step=0.5,
            decimals=1,
            suffix="px",
            default=0,
        )
        layout.addWidget(self.border_spinbox)

        layout.addWidget(QLabel("Border Color"))
        self.border_color = QComboBox()

        self.custom_color_button = QPushButton("Custom Color")
        layout.addWidget(self.custom_color_button)

        self.border_color.addItems([
            "Black",
            "White",
            "Custom",
        ])
        layout.addWidget(self.border_color)

        layout.addWidget(QLabel("Corner Radius"))
        self.corner_radius = NumberControl(
            minimum=0,
            maximum=100,
            step=1,
            decimals=0,
            suffix="px",
            default=0,
        )
        layout.addWidget(self.corner_radius)

        layout.addWidget(QLabel("Shadow"))
        self.shadow_checkbox = QCheckBox("Enable Shadow")
        layout.addWidget(self.shadow_checkbox)

        self.shadow_color_button = QPushButton("Shadow Color")
        layout.addWidget(self.shadow_color_button)

        layout.addWidget(QLabel("Shadow Blur"))
        self.shadow_blur = NumberControl(
            minimum=0,
            maximum=100,
            step=1,
            decimals=0,
            default=20,
        )
        layout.addWidget(self.shadow_blur)

        layout.addWidget(QLabel("Shadow Offset X"))
        self.shadow_offset_x = NumberControl(
            minimum=-100,
            maximum=100,
            step=1,
            decimals=0,
            default=0,
        )
        layout.addWidget(self.shadow_offset_x)

        layout.addWidget(QLabel("Shadow Offset Y"))
        self.shadow_offset_y = NumberControl(
            minimum=-100,
            maximum=100,
            step=1,
            decimals=0,
            default=0,
        )
        layout.addWidget(self.shadow_offset_y)

        layout.addWidget(QLabel("Shadow Opacity"))
        self.shadow_opacity = NumberControl(
            minimum=0,
            maximum=255,
            step=1,
            decimals=0,
            default=100,
        )
        layout.addWidget(self.shadow_opacity)

        self.reset_button = QPushButton("Reset Settings")
        layout.addWidget(self.reset_button)

        layout.addWidget(QLabel("Custom Presets"))

        self.preset_combo = QComboBox()
        layout.addWidget(self.preset_combo)

        self.apply_preset_button = QPushButton("Apply Preset")
        layout.addWidget(self.apply_preset_button)

        self.save_preset_button = QPushButton("Save New Preset")
        layout.addWidget(self.save_preset_button)

        self.update_preset_button = QPushButton("Update Selected Preset")
        layout.addWidget(self.update_preset_button)

        self.delete_preset_button = QPushButton("Delete Selected Preset")
        layout.addWidget(self.delete_preset_button)
        
        layout.addStretch()