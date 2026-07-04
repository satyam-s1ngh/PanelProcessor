from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Panel Processor")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # ---------------- LEFT PANEL ---------------- #

        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)

        left_layout.addWidget(QLabel("Input Folder"))
        left_layout.addWidget(QPushButton("Browse"))

        left_layout.addSpacing(20)

        left_layout.addWidget(QLabel("Output Folder"))
        left_layout.addWidget(QPushButton("Browse"))

        left_layout.addStretch()

        # ---------------- CENTER PANEL ---------------- #

        center_panel = QFrame()
        center_panel.setFrameShape(QFrame.StyledPanel)
        center_layout = QVBoxLayout(center_panel)

        title = QLabel("Panel Processor")
        title.setStyleSheet("font-size:22px;font-weight:bold;")

        center_layout.addWidget(title)
        center_layout.addStretch()

        # ---------------- RIGHT PANEL ---------------- #

        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)

        preview = QLabel("Live Preview")
        preview.setStyleSheet("font-size:18px;")

        right_layout.addWidget(preview)
        right_layout.addStretch()

        # ---------------- LAYOUT ---------------- #

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(center_panel, 2)
        main_layout.addWidget(right_panel, 2)