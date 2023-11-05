from PIL import Image

import exif
from .config import Config

from .watermark import Watermark
from .bottom import BottomWatermark
from .bottom_frame import BottomFrameWatermark
from .video_use import VideoUseWatermark


def get_watermark(t) -> Watermark:
    if t == 'bottom':
        return BottomWatermark()
    elif t == 'bottom_frame':
        return BottomFrameWatermark()
    elif t == 'video_use':
        return VideoUseWatermark()
    return BottomWatermark()


def draw_watermark(draw_type, img: Image, config: Config, exif_info: exif.ExifInfo) -> (Image, dict):
    return get_watermark(draw_type).draw(img, config, exif_info)
