import sys

from pathlib import Path
from core.pipeline import Pipeline
from core.settings import Settings
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtWidgets import QColorDialog


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    # Temporary pipeline test (remove later)

    test_input = Path("assets/test.png")
    test_output = Path("output/test_output.png")

    if test_input.exists():
        Pipeline.process_one(
            test_input,
            test_output,
            Settings(),
        )
        
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()