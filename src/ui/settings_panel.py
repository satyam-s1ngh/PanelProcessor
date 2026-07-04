from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QDoubleSpinBox,
)
from PySide6.QtCore import Qt


class SettingsPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        layout.addWidget(QLabel("Border Thickness"))
        self.border_spinbox = QDoubleSpinBox()

        self.border_spinbox.setRange(0.0, 30.0)
        self.border_spinbox.setSingleStep(0.5)
        self.border_spinbox.setDecimals(1)
        self.border_spinbox.setSuffix(" px")

        layout.addWidget(self.border_spinbox)

        layout.addStretch() 