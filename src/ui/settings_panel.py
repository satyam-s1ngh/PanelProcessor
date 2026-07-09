from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSpinBox,
    QCheckBox,
    QWidget,
    QLineEdit,
)
from PySide6.QtCore import Qt, Signal


class BorderThicknessControl(QWidget):
    valueChanged = Signal(float)

    def __init__(self):
        super().__init__()

        self._value = 0.0

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.minus_button = QPushButton("-")
        self.input = QLineEdit("0.0")
        self.plus_button = QPushButton("+")

        self.input.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.minus_button)
        layout.addWidget(self.input)
        layout.addWidget(QLabel("px"))
        layout.addWidget(self.plus_button)

        self.minus_button.clicked.connect(self.decrease)
        self.plus_button.clicked.connect(self.increase)
        self.input.editingFinished.connect(self.apply_text_value)

    def increase(self):
        self.set_border_value(self._value + 0.5, emit=True)

    def decrease(self):
        self.set_border_value(self._value - 0.5, emit=True)

    def apply_text_value(self):
        text = self.input.text().replace("px", "").strip()

        try:
            value = float(text)
        except ValueError:
            self.input.setText(f"{self._value:.1f}")
            return

        value = round(value * 2) / 2
        self.set_border_value(value, emit=True)

    def set_border_value(self, value, emit=False):
        value = max(0.0, min(100.0, float(value)))

        self._value = value
        self.input.setText(f"{self._value:.1f}")

        if emit:
            self.valueChanged.emit(self._value)

    def value(self):
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
        self.border_spinbox = BorderThicknessControl()
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
        self.corner_radius = QSpinBox()
        self.corner_radius.setRange(0, 100)
        self.corner_radius.setSuffix(" px")
        layout.addWidget(self.corner_radius)

        layout.addWidget(QLabel("Shadow"))
        self.shadow_checkbox = QCheckBox("Enable Shadow")
        layout.addWidget(self.shadow_checkbox)

        self.shadow_color_button = QPushButton("Shadow Color")
        layout.addWidget(self.shadow_color_button)

        layout.addWidget(QLabel("Shadow Blur"))
        self.shadow_blur = QSpinBox()
        self.shadow_blur.setRange(0, 100)
        self.shadow_blur.setValue(20)
        layout.addWidget(self.shadow_blur)

        layout.addWidget(QLabel("Shadow Offset X"))
        self.shadow_offset_x = QSpinBox()
        self.shadow_offset_x.setRange(-100, 100)
        self.shadow_offset_x.setValue(0)
        layout.addWidget(self.shadow_offset_x)

        layout.addWidget(QLabel("Shadow Offset Y"))
        self.shadow_offset_y = QSpinBox()
        self.shadow_offset_y.setRange(-100, 100)
        self.shadow_offset_y.setValue(0)
        layout.addWidget(self.shadow_offset_y)

        layout.addWidget(QLabel("Shadow Opacity"))
        self.shadow_opacity = QSpinBox()
        self.shadow_opacity.setRange(0, 255)
        self.shadow_opacity.setValue(100)
        layout.addWidget(self.shadow_opacity)

        layout.addStretch()