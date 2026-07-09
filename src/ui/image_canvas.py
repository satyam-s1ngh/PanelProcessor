from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF

from core.image_processor import ImageProcessor


class ImageCanvas(QWidget):
    def __init__(self):
        super().__init__()

        self.image = None
        self.settings = None

        self.cached_pixmap = None
        self.cached_key = None

        self.setMinimumSize(600, 600)

    def set_image(self, image_path):
        self.image = QImage(image_path)

        self.cached_pixmap = None
        self.cached_key = None

        self.update()

    def set_settings(self, settings):
        self.settings = settings

        # Do not process here.
        # Processing will happen once inside paintEvent and then be cached.
        self.update()

    def get_settings_key(self):
        if self.settings is None:
            return None

        return (
            float(getattr(self.settings, "border_thickness", 0.0)),
            str(getattr(self.settings, "border_color", "#000000")),
            float(getattr(self.settings, "corner_radius", 0.0)),

            bool(getattr(self.settings, "shadow_enabled", False)),
            int(getattr(self.settings, "shadow_blur", 0)),
            int(getattr(self.settings, "shadow_opacity", 0)),
            int(getattr(self.settings, "shadow_offset_x", 0)),
            int(getattr(self.settings, "shadow_offset_y", 0)),
            str(getattr(self.settings, "shadow_color", "#000000")),

            bool(getattr(self.settings, "background_enabled", False)),
            str(getattr(self.settings, "background_color", "#ffffff")),
        )

    def get_processed_pixmap(self):
        if self.image is None or self.image.isNull():
            return None

        key = (
            self.image.cacheKey(),
            self.get_settings_key(),
        )

        if self.cached_pixmap is not None and self.cached_key == key:
            return self.cached_pixmap

        if self.settings is None:
            processed = self.image
        else:
            processed = ImageProcessor.process(
                self.image,
                self.settings,
            )

        self.cached_pixmap = QPixmap.fromImage(processed)
        self.cached_key = key

        return self.cached_pixmap

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            Qt.darkGray,
        )

        if self.image is None or self.image.isNull():
            painter.setPen(Qt.white)
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "No Image Loaded",
            )
            return

        pixmap = self.get_processed_pixmap()

        if pixmap is None or pixmap.isNull():
            return

        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True,
        )

        img_w = pixmap.width()
        img_h = pixmap.height()

        canvas_w = self.width()
        canvas_h = self.height()

        margin = 20

        available_w = max(1, canvas_w - margin * 2)
        available_h = max(1, canvas_h - margin * 2)

        scale = min(
            available_w / img_w,
            available_h / img_h,
        )

        draw_w = int(img_w * scale)
        draw_h = int(img_h * scale)

        draw_x = (canvas_w - draw_w) / 2
        draw_y = (canvas_h - draw_h) / 2

        target = QRectF(
            draw_x,
            draw_y,
            draw_w,
            draw_h,
        )

        painter.drawPixmap(
            target,
            pixmap,
            pixmap.rect(),
        )