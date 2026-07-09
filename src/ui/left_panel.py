from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QProgressBar,
    QCheckBox,
    QPlainTextEdit,
)
from PySide6.QtCore import Qt


class LeftPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("Folders")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.input_button = QPushButton("Select Input Folder")
        layout.addWidget(self.input_button)

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Input folder path")
        layout.addWidget(self.input_path)

        self.output_button = QPushButton("Select Output Folder")
        layout.addWidget(self.output_button)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output folder path")
        layout.addWidget(self.output_path)

        layout.addWidget(QLabel("Processing"))

        self.skip_existing_checkbox = QCheckBox("Skip Already Processed Files")
        layout.addWidget(self.skip_existing_checkbox)

        self.process_current_button = QPushButton("Process Current Image")
        layout.addWidget(self.process_current_button)

        self.process_button = QPushButton("Process All")
        layout.addWidget(self.process_button)

        self.cancel_button = QPushButton("Cancel Processing")
        self.cancel_button.setEnabled(False)
        layout.addWidget(self.cancel_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.processing_status = QLabel("Ready")
        self.processing_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.processing_status)

        self.eta_label = QLabel("ETA: --")
        self.eta_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.eta_label)

        layout.addWidget(QLabel("Error Log"))

        self.error_log = QPlainTextEdit()
        self.error_log.setReadOnly(True)
        self.error_log.setPlaceholderText("Failed images will appear here...")
        layout.addWidget(self.error_log)

        layout.addStretch()