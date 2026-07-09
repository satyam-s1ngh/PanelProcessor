from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QDoubleSpinBox,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QPushButton, QColorDialog
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QCheckBox



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
        self.border_spinbox = QDoubleSpinBox()
        self.border_spinbox.setRange(0.0, 30.0)
        self.border_spinbox.setSingleStep(0.5)
        self.border_spinbox.setDecimals(1)
        self.border_spinbox.setSuffix(" px")
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
        self.corner_radius.setRange(0, 200)
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

        layout.addWidget(QLabel("Shadow Offset"))

        self.shadow_offset_x = QSpinBox()
        self.shadow_offset_x.setRange(-100, 100)
        self.shadow_offset_x.setValue(0)
        self.shadow_offset_y = QSpinBox()
        self.shadow_offset_y.setRange(-100, 100)
        self.shadow_offset_y.setValue(0)
        layout.addWidget(self.shadow_offset_x)
        layout.addWidget(self.shadow_offset_y)

        layout.addWidget(QLabel("Shadow Opacity"))

        self.shadow_opacity = QSpinBox()
        self.shadow_opacity.setRange(0, 255)
        self.shadow_opacity.setValue(100)
        layout.addWidget(self.shadow_opacity)

        layout.addStretch() 