from PySide6.QtGui import QImage

from core.image_processor import ImageProcessor
from core.exporter import Exporter


class Pipeline:
    @staticmethod
    def process_one(input_path, output_path, settings):
        image = QImage(str(input_path))

        if image.isNull():
            raise ValueError(f"Could not load image: {input_path}")

        processed = ImageProcessor.process(
            image,
            settings,
        )

        return Exporter.save(
            processed,
            output_path,
            settings,
        )
