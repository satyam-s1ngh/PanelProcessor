from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter

from PySide6.QtGui import QImage
from PySide6.QtCore import QByteArray, QBuffer, QIODevice


class ImageProcessor:

    SCALE = 4

    @staticmethod
    def process(image: QImage, settings) -> QImage:
        border = max(0.0, float(settings.border_thickness))
        radius = max(0.0, float(settings.corner_radius))

        shadow_enabled = bool(settings.shadow_enabled)
        shadow_blur = max(0, int(settings.shadow_blur))
        shadow_opacity = max(0, min(255, int(settings.shadow_opacity)))
        shadow_offset_x = int(settings.shadow_offset_x) if shadow_enabled else 0
        shadow_offset_y = int(settings.shadow_offset_y) if shadow_enabled else 0
        shadow_color = getattr(settings, "shadow_color", "#000000")

        border_color = getattr(settings, "border_color", "#000000")

        if (
            border <= 0
            and radius <= 0
            and not shadow_enabled
        ):
            return image.copy()

        pil_image = ImageProcessor.qimage_to_pil(image)
        w, h = pil_image.size

        margin = shadow_blur * 3 + 4 if shadow_enabled else 0

        left = margin + max(0, -shadow_offset_x)
        right = margin + max(0, shadow_offset_x)
        top = margin + max(0, -shadow_offset_y)
        bottom = margin + max(0, shadow_offset_y)

        out_w = int(round(w + border * 2 + left + right))
        out_h = int(round(h + border * 2 + top + bottom))

        s = ImageProcessor.SCALE

        if getattr(settings, "background_enabled", False):
            bg_color = ImageProcessor.color_to_rgba(
                getattr(settings, "background_color", "#ffffff")
            )
        else:
            bg_color = (0, 0, 0, 0)

        canvas = Image.new(
            "RGBA",
            (out_w * s, out_h * s),
            bg_color,
        )

        # ---------- Shadow ----------
        if shadow_enabled and shadow_opacity > 0 and shadow_blur > 0:
            shadow_layer = Image.new(
                "RGBA",
                canvas.size,
                (0, 0, 0, 0),
            )

            draw = ImageDraw.Draw(shadow_layer)

            shadow_rect = [
                int(round((left + shadow_offset_x) * s)),
                int(round((top + shadow_offset_y) * s)),
                int(round((left + shadow_offset_x + w + border * 2) * s)),
                int(round((top + shadow_offset_y + h + border * 2) * s)),
            ]

            r = int(round((radius + border) * s))

            shadow_alpha = min(
                255,
                int(shadow_opacity * 3.2)
            )

            fill = ImageProcessor.hex_to_rgba(
                shadow_color,
                shadow_alpha,
            )

            if radius <= 0:
                draw.rectangle(shadow_rect, fill=fill)
            else:
                draw.rounded_rectangle(
                    shadow_rect,
                    radius=r,
                    fill=fill,
                )

            shadow_layer = shadow_layer.filter(
                ImageFilter.GaussianBlur(
                    radius=shadow_blur * s
                )
            )

            canvas.alpha_composite(shadow_layer)
            canvas.alpha_composite(shadow_layer)

        # ---------- Border ----------
        if border > 0:
            draw = ImageDraw.Draw(canvas)

            border_rect = [
                int(round(left * s)),
                int(round(top * s)),
                int(round((left + w + border * 2) * s)),
                int(round((top + h + border * 2) * s)),
            ]

            r = int(round((radius + border) * s))

            if radius <= 0:
                draw.rectangle(
                    border_rect,
                    fill=ImageProcessor.color_to_rgba(border_color),
                )
            else:
                draw.rounded_rectangle(
                    border_rect,
                    radius=r,
                    fill=ImageProcessor.color_to_rgba(border_color),
                )

        # ---------- Image ----------
        image_x = int(round((left + border) * s))
        image_y = int(round((top + border) * s))

        scaled_image = pil_image.resize(
            (w * s, h * s),
            Image.Resampling.LANCZOS,
        )

        if radius > 0:
            mask = Image.new(
                "L",
                (w * s, h * s),
                0,
            )

            mask_draw = ImageDraw.Draw(mask)

            mask_draw.rounded_rectangle(
                [0, 0, w * s, h * s],
                radius=int(round(radius * s)),
                fill=255,
            )

            canvas.paste(
                scaled_image,
                (image_x, image_y),
                mask,
            )
        else:
            canvas.alpha_composite(
                scaled_image,
                (image_x, image_y),
            )

        canvas = canvas.resize(
            (out_w, out_h),
            Image.Resampling.LANCZOS,
        )

        return ImageProcessor.pil_to_qimage(canvas)

    @staticmethod
    def qimage_to_pil(image: QImage) -> Image.Image:
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, "PNG")

        return Image.open(
            BytesIO(bytes(ba))
        ).convert("RGBA")

    @staticmethod
    def pil_to_qimage(image: Image.Image) -> QImage:
        bio = BytesIO()
        image.save(bio, format="PNG")

        qimage = QImage()
        qimage.loadFromData(bio.getvalue(), "PNG")

        return qimage

    @staticmethod
    def color_to_rgba(color: str):
        if not color:
            color = "#000000"

        c = color.strip()

        if c.lower() == "black":
            return (0, 0, 0, 255)

        if c.lower() == "white":
            return (255, 255, 255, 255)

        if c.startswith("#"):
            c = c[1:]

        if len(c) == 6:
            r = int(c[0:2], 16)
            g = int(c[2:4], 16)
            b = int(c[4:6], 16)
            return (r, g, b, 255)

        return (0, 0, 0, 255)

    @staticmethod
    def hex_to_rgba(color: str, alpha: int):
        r, g, b, _ = ImageProcessor.color_to_rgba(color)
        return (r, g, b, alpha)