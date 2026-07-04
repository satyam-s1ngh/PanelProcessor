from PySide6.QtGui import QImage


class ImageProcessor:

    @staticmethod
    def process(image: QImage, settings) -> QImage:
        result = image.copy()

        # Future:
        # Border
        # Shadow
        # Rounded Corners

        return result