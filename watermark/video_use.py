from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import math
import exif
from .config import Config
from .bottom_frame import BottomFrameWatermark
from .bottom import BottomWatermark
from .watermark import Watermark

WIDTH_8K = 7680
HEIGHT_8K = 4320
PADDING_8K = 200
SHADOW_PADDING = 50


class VideoUseWatermark(Watermark):
    def draw(self, img: Image, config: Config, exif_info: exif.ExifInfo) -> Image:
        im_blur = img.filter(ImageFilter.GaussianBlur(radius=200))
        im_blur = im_blur.resize((WIDTH_8K, HEIGHT_8K), Image.Resampling.LANCZOS)

        # 调整亮度
        enhancer = ImageEnhance.Brightness(im_blur)
        im_blur = enhancer.enhance(0.7)

        # im_blur = Image.new("RGB", (WIDTH_8K, HEIGHT_8K), color='white')

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
            shadow = Image.new("RGBA", (m_img.width + SHADOW_PADDING * 2, m_img.height + SHADOW_PADDING * 2), color=(256, 256, 256, 0))

            shadow_draw = ImageDraw.Draw(shadow)
            opx1 = SHADOW_PADDING
            opy1 = SHADOW_PADDING

            opx2 = SHADOW_PADDING + m_img.width
            opy2 = SHADOW_PADDING + m_img.height
            cd = 100
            for i in range(1, SHADOW_PADDING + 1):
                px1 = opx1 - i
                py1 = opy1 - i

                px2 = opx2 + i
                py2 = opy2 + i

                c = max(cd - i * 2, 0)
                iss = i ** 2
                for x in range(px1, px2 + 1):
                    if x < opx1 or x > opx2:
                        xd = max(opx1 - x, x - opx2)
                        d = int(math.sqrt(xd ** 2 + iss))
                        c2 = max(cd - d * 2, 0)
                        shadow_draw.point((x, py1), fill=(0, 0, 0, c2))
                        shadow_draw.point((x, py2), fill=(0, 0, 0, c2))
                    else:
                        shadow_draw.point((x, py1), fill=(0, 0, 0, c))
                        shadow_draw.point((x, py2), fill=(0, 0, 0, c))

                for y in range(py1, py2 + 1):
                    if y < opy1 or y > opy2:
                        yd = max(opy1 - y, y - opy2)
                        d = int(math.sqrt(yd ** 2 + iss))
                        c2 = max(cd - d * 2, 0)
                        shadow_draw.point((px1, y), fill=(0, 0, 0, c2))
                        shadow_draw.point((px2, y), fill=(0, 0, 0, c2))
                    else:
                        shadow_draw.point((px1, y), fill=(0, 0, 0, c))
                        shadow_draw.point((px2, y), fill=(0, 0, 0, c))
            im_blur.paste(shadow, (left_padding - SHADOW_PADDING, PADDING_8K - SHADOW_PADDING), shadow)

        im_blur.paste(m_img, (left_padding, PADDING_8K))

        return im_blur
