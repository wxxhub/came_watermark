from PIL import Image, ImageFilter, ImageEnhance

import exif
from .config import Config
from .bottom_frame import BottomFrameWatermark
from .bottom import BottomWatermark
from .watermark import Watermark

WIDTH_8K = 7680
HEIGHT_8K = 4320
PADDING_8K = 200
SHADOW_PADDING = 100


class VideoUseWatermark(Watermark):
    def draw(self, img: Image, config: Config, exif_info: exif.ExifInfo) -> Image:
        im_blur = img.filter(ImageFilter.GaussianBlur(radius=200))
        im_blur = im_blur.resize((WIDTH_8K, HEIGHT_8K), Image.Resampling.LANCZOS)

        # 调整亮度
        enhancer = ImageEnhance.Brightness(im_blur)
        im_blur = enhancer.enhance(0.7)

        if config.children_watermark == 'bottom':
            m = BottomWatermark()
        else:
            m = BottomFrameWatermark()

        m_img = m.draw(img, config, exif_info)

        resize_h = HEIGHT_8K - PADDING_8K * 2
        resize_w = int(resize_h / m_img.height * m_img.width)
        left_padding = int((WIDTH_8K - resize_w) / 2)

        m_img = m_img.resize((resize_w, resize_h), Image.Resampling.LANCZOS)
        if config.children_watermark == 'bottom':
            shadow = Image.new("L", (m_img.width + SHADOW_PADDING * 2, m_img.height + SHADOW_PADDING * 2), color=25)
            im_blur.paste(shadow, (left_padding - SHADOW_PADDING, PADDING_8K - SHADOW_PADDING), shadow)

        im_blur.paste(m_img, (left_padding, PADDING_8K))

        return im_blur
