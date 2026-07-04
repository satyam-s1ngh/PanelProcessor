from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF
from core.image_processor import ImageProcessor


class ImageCanvas(QWidget):
    def __init__(self):
        super().__init__()

        self.pixmap = None
        self.image = None
        self.setMinimumSize(600, 600)
        self.border_thickness = 0.0
        self.settings = None

    def set_image(self, image_path):
        self.image = QImage(image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.update()

    def set_border_thickness(self, value: float):
        self.border_thickness = value
        self.update()

    def set_settings(self, settings):
        self.settings = settings
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.darkGray)

        if self.image is None or self.image.isNull():
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter, "No Image Loaded")
            return

        processed = ImageProcessor.process(
            self.image,
            self.settings,
        )

        self.pixmap = QPixmap.fromImage(processed)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        img_w = self.pixmap.width()
        img_h = self.pixmap.height()

        canvas_w = self.width()
        canvas_h = self.height()

        scale = min(canvas_w / img_w, canvas_h / img_h)

        border = max(0.0, self.border_thickness)

        margin = 20

        scale = min(
            (canvas_w - margin * 2) / img_w,
            (canvas_h - margin * 2) / img_h,
        )

        draw_w = int(img_w * scale)
        draw_h = int(img_h * scale)

        outer_w = draw_w + (border * 2)
        outer_h = draw_h + (border * 2)

        outer_x = (canvas_w - outer_w) / 2
        outer_y = (canvas_h - outer_h) / 2

        # Draw border/background
        if border > 0:
            painter.fillRect(
                QRectF(
                  outer_x,
                  outer_y,
                  outer_w,
                  outer_h,
                ),
                Qt.black,
             )

        # Draw image inside border
        target = QRectF(
            outer_x + border,
            outer_y + border,
            draw_w,
            draw_h,
        )

        painter.drawPixmap(target, self.pixmap, self.pixmap.rect())