from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import math
import exif
from .config import Config
from .bottom_frame import BottomFrameWatermark
from .bottom import BottomWatermark
from .watermark import Watermark

WIDTH_8K = 7680
HEIGHT_8K = 4320
SHADOW_PADDING = 50

class VideoUseWhiteBackgroundWatermark(Watermark):
    def draw(self, img: Image, config: Config, exif_info: exif.ExifInfo) -> Image:
        im_blur = Image.new("RGB", (WIDTH_8K, HEIGHT_8K), color='white')

        m = BottomFrameWatermark()
        m_img = m.draw(img, config, exif_info)

        resize_w = int(HEIGHT_8K / m_img.height * m_img.width)
        resize_h = HEIGHT_8K

        left_padding = int((WIDTH_8K - resize_w) / 2)
        top_padding = 0
        if resize_w > WIDTH_8K:
            # 超出画布
            resize_w = WIDTH_8K
            resize_h = int(WIDTH_8K / m_img.width * m_img.height)
            top_padding = int(HEIGHT_8K-resize_h) / 2

        m_img = m_img.resize((resize_w, resize_h), Image.Resampling.LANCZOS)
        im_blur.paste(m_img, (left_padding, top_padding))

        return im_blur
