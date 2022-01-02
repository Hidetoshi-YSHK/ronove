import io
from typing import Optional
from PIL import Image as PillowImage
from PIL import ImageTk

import singleton

class ImageProcessor(singleton.Singleton):
    IMAGE_SIZE = 200
    IMAGE_COLOR_SPACE = "RGB"
    IMAGE_FORMAT = "jpeg"

    def load_and_preprocess(self, file_path) -> Optional[bytes]:
        try:
            img = PillowImage.open(file_path)
            img.thumbnail(size=(self.IMAGE_SIZE, self.IMAGE_SIZE))
            buffer = io.BytesIO()
            img = img.convert(self.IMAGE_COLOR_SPACE)
            img.save(buffer, format=self.IMAGE_FORMAT, quality=60)
            return buffer.getvalue()
        except Exception:
            return None

    def convert_bytes_to_photo_image(
        self, image_data:bytes) -> Optional[ImageTk.PhotoImage]:
        try:
            img = PillowImage.open(io.BytesIO(image_data))
            return ImageTk.PhotoImage(img)
        except Exception:
            return None