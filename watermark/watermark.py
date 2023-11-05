from abc import ABC, abstractmethod

from PIL import Image
from .config import Config
import exif


class Watermark:
    @abstractmethod
    def draw(self, img: Image, config: Config, exif_info: exif.ExifInfo) -> Image:
        return
