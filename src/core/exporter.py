from pathlib import Path

from PySide6.QtGui import QImage, QColor, QPainter


class Exporter:
    @staticmethod
    def normalize_format(selected_format, fallback_suffix):
        selected = (selected_format or "PNG").strip().upper()
        fallback = (fallback_suffix or ".png").lower().replace(".", "")

        if selected == "SAME AS INPUT":
            if fallback not in {"png", "jpg", "jpeg", "webp"}:
                fallback = "png"
            extension = "jpg" if fallback == "jpeg" else fallback

        elif selected in {"JPG", "JPEG"}:
            extension = "jpg"

        elif selected == "WEBP":
            extension = "webp"

        else:
            extension = "png"

        qt_format = "JPEG" if extension == "jpg" else extension.upper()
        return extension, qt_format

    @staticmethod
    def build_output_path(output_path, settings):
        output_path = Path(output_path)

        extension, qt_format = Exporter.normalize_format(
            getattr(settings, "output_format", "PNG"),
            output_path.suffix,
        )

        final_path = output_path.with_suffix(f".{extension}")
        final_path.parent.mkdir(parents=True, exist_ok=True)

        return final_path, qt_format

    @staticmethod
    def flatten_for_jpg(image: QImage, settings) -> QImage:
        if getattr(settings, "background_enabled", False):
            background = QColor(
                getattr(settings, "background_color", "#FFFFFF")
            )
        else:
            background = QColor("#FFFFFF")

        flattened = QImage(
            image.size(),
            QImage.Format_RGB32,
        )

        painter = QPainter(flattened)
        painter.fillRect(
            flattened.rect(),
            background,
        )
        painter.drawImage(
            0,
            0,
            image,
        )
        painter.end()

        return flattened

    @staticmethod
    def save(image: QImage, output_path, settings):
        final_path, qt_format = Exporter.build_output_path(
            output_path,
            settings,
        )

        image_to_save = image
        quality = -1

        if qt_format == "JPEG":
            image_to_save = Exporter.flatten_for_jpg(
                image,
                settings,
            )
            quality = 95

        ok = image_to_save.save(
            str(final_path),
            qt_format,
            quality,
        )

        if not ok:
            raise ValueError(f"Failed to save image: {final_path}")

        return final_path
