from pathlib import Path


SUPPORTED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
)


class FileManager:

    @staticmethod
    def get_images(folder):
        folder = Path(folder)

        images = []

        for file in folder.iterdir():
            if file.suffix.lower() in SUPPORTED_EXTENSIONS:
                images.append(file)

        images.sort()

        return images