from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QFileDialog,
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

        # Input Folder
        input_title = QLabel("📁 Input Folder")

        self.input_path = QLabel("No folder selected")
        self.input_path.setWordWrap(True)

        input_button = QPushButton("Browse")
        input_button.clicked.connect(self.select_input_folder)

        # Output Folder
        output_title = QLabel("📁 Output Folder")

        self.output_path = QLabel("No folder selected")
        self.output_path.setWordWrap(True)

        output_button = QPushButton("Browse")
        output_button.clicked.connect(self.select_output_folder)

        left_layout.addWidget(input_title)
        left_layout.addWidget(self.input_path)
        left_layout.addWidget(input_button)

        left_layout.addSpacing(25)

        left_layout.addWidget(output_title)
        left_layout.addWidget(self.output_path)
        left_layout.addWidget(output_button)

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

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder"
        )

        if folder:
            self.input_path.setText(folder)


    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:
            self.output_path.setText(folder)