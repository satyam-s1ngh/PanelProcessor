from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from core.file_manager import FileManager
from PySide6.QtWidgets import QProgressBar


class LeftPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        # Input Folder
        layout.addWidget(QLabel("📁 Input Folder"))

        self.input_path = QLabel("No folder selected")
        self.input_path.setWordWrap(True)

        self.input_button = QPushButton("Browse")

        layout.addWidget(self.input_path)
        layout.addWidget(self.input_button)

        layout.addSpacing(25)

        # Output Folder
        layout.addWidget(QLabel("📁 Output Folder"))

        self.output_path = QLabel("No folder selected")
        self.output_path.setWordWrap(True)

        self.output_button = QPushButton("Browse")
        layout.addWidget(self.output_path)
        layout.addWidget(self.output_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.process_current_button = QPushButton("▶ Process Current Image")
        layout.addWidget(self.process_current_button)

        self.process_button = QPushButton("▶ Process Images")
        layout.addWidget(self.process_button)

        layout.addStretch()