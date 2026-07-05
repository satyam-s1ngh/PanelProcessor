from pathlib import Path
from PySide6.QtGui import QImage


class Exporter:

    @staticmethod
    def save(image: QImage, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        return image.save(str(output_path))