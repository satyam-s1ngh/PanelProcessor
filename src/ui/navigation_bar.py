from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class NavigationBar(QFrame):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.previous_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")

        self.counter = QLabel("0 / 0")
        self.counter.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.previous_button)
        layout.addStretch()
        layout.addWidget(self.counter)
        layout.addStretch()
        layout.addWidget(self.next_button)