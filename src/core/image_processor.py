from PySide6.QtGui import (
    QImage,
    QPainter,
    QColor,
    QPainterPath,
)

from PySide6.QtCore import (
    Qt,
    QRectF,
)
from PySide6.QtCore import QTimer


class ImageProcessor:

    @staticmethod
    def process(image: QImage, settings) -> QImage:

        border = max(0.0, float(settings.border_thickness))
        radius = max(0.0, float(settings.corner_radius))

        shadow_enabled = settings.shadow_enabled

        blur = float(settings.shadow_blur) if shadow_enabled else 0.0

        offset_x = float(settings.shadow_offset_x) if shadow_enabled else 0.0
        offset_y = float(settings.shadow_offset_y) if shadow_enabled else 0.0

        margin = blur * 2 + border + 2

        left = margin + max(0.0, -offset_x)
        top = margin + max(0.0, -offset_y)

        right = margin + max(0.0, offset_x)
        bottom = margin + max(0.0, offset_y)

        width = int(
            image.width()
            + border * 2
            + left
            + right
        )

        height = int(
            image.height()
            + border * 2
            + top
            + bottom
        )

        result = QImage(
            width,
            height,
            QImage.Format_ARGB32_Premultiplied,
        )

        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing,True)
        painter.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True,
        )

        origin_x = left
        origin_y = top

        if shadow_enabled:
            ImageProcessor.draw_shadow(
                painter,
                image,
                border,
                radius,
                settings,
                origin_x,
                origin_y,
            )

        ImageProcessor.draw_border(
            painter,
            image,
            border,
            radius,
            settings,
            origin_x,
            origin_y,
        )

        ImageProcessor.draw_image(
            painter,
            image,
            border,
            radius,
            origin_x,
            origin_y,
        )

        painter.end()

        return result
    
    @staticmethod
    def draw_shadow(
        painter,
        image,
        border,
        radius,
        settings,
        origin_x,
        origin_y,
    ):

        blur = int(settings.shadow_blur)

        color = QColor(settings.shadow_color)

        outer = QPainterPath()

        inner = QPainterPath()

        for i in range(1, blur * 2 + 1):

            import math

            spread = i

            sigma = blur * 0.55

            alpha = int(
                settings.shadow_opacity *
                math.exp(-(spread ** 2) / (2 * sigma ** 2))
)

            alpha = max(0, min(alpha, 255))

            color.setAlpha(alpha)

            rect = QRectF(
                origin_x + settings.shadow_offset_x - spread,
                origin_y + settings.shadow_offset_y - spread,
                image.width() + border * 2 + spread * 2,
                image.height() + border * 2 + spread * 2,
            )

            outer.clear()

            if radius <= 0:
                outer.addRect(rect)
            else:
                outer.addRoundedRect(
                    rect,
                    radius + border + spread,
                    radius + border + spread,
                )

            inner.clear()

            inner_rect = QRectF(
                origin_x + settings.shadow_offset_x,
                origin_y + settings.shadow_offset_y,
                image.width() + border * 2,
                image.height() + border * 2,
            )

            if radius <= 0:
                inner.addRect(inner_rect)
            else:
                inner.addRoundedRect(
                    inner_rect,
                    radius + border,
                    radius + border,
                )

            painter.fillPath(
                outer.subtracted(inner),
                color,
            )

    @staticmethod
    def draw_border(
        painter,
        image,
        border,
        radius,
        settings,
        origin_x,
        origin_y,
    ):
        if border <= 0:
            return

        x = round(origin_x * 2) / 2
        y = round(origin_y * 2) / 2

        w = round((image.width() + border * 2) * 2) / 2
        h = round((image.height() + border * 2) * 2) / 2

        border_rect = QRectF(
            x,
            y,
            w,
            h,
        )
        path = QPainterPath()

        if radius <= 0:
            path.addRect(border_rect)
        else:
            path.addRoundedRect(
                border_rect,
                radius + border,
                radius + border,
            )

        painter.fillPath(
            path,
            QColor(settings.border_color),
        )

    @staticmethod
    def draw_image(
        painter,
        image,
        border,
        radius,
        origin_x,
        origin_y,
    ):

        image_rect = QRectF(
            origin_x + border,
            origin_y + border,
            image.width(),
            image.height(),
        )

        clip = QPainterPath()

        if radius <= 0:
            clip.addRect(image_rect)
        else:
            clip.addRoundedRect(
                image_rect,
                radius,
                radius,
            )

        painter.save()

        painter.setClipPath(clip)

        painter.drawImage(
            image_rect,
            image,
        )

        painter.restore()
