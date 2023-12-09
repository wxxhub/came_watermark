from PIL import Image

from watermark.draw import draw_watermark
from watermark.config import Config
import piexif
import exif

RESIZE_WIDTH = 1920


def save_resize(img: Image) -> Image:
    return img.resize((RESIZE_WIDTH, int(RESIZE_WIDTH / img.width * img.height)), Image.Resampling.LANCZOS)


def test_bottom_watermark():
    c = Config()
    c.author = "ValiantBunny"
    img = Image.open('test/data/test_in.jpg')
    exif_info, exif_origin = exif.get_exif_info(img)
    img = draw_watermark('bottom', img, c, exif_info)
    save_resize(img).save("test/test_bottom.jpg", exif=piexif.dump(exif_origin))


def test_bottom_frame():
    c = Config()
    c.author = "ValiantBunny"
    img = Image.open('test/data/test_in.jpg')
    exif_info, exif_origin = exif.get_exif_info(img)
    img = draw_watermark('bottom_frame', img, c, exif_info)
    save_resize(img).save("test/test_bottom_frame.jpg", exif=piexif.dump(exif_origin))


def test_video_use():
    c = Config()
    c.author = "ValiantBunny"
    img = Image.open('test/data/test_in.jpg')
    exif_info, exif_origin = exif.get_exif_info(img)
    img = draw_watermark('video_use', img, c, exif_info)
    save_resize(img).save("test/test_video_use.jpg", exif=piexif.dump(exif_origin))


def test_video_use_2():
    c = Config()
    c.author = "ValiantBunny"
    c.children_watermark = "bottom"
    img = Image.open('test/data/test_in.jpg')
    exif_info, exif_origin = exif.get_exif_info(img)
    img = draw_watermark('video_use', img, c, exif_info)
    save_resize(img).save("test/test_video_use_2.jpg", exif=piexif.dump(exif_origin))

def test_video_use_white_background():
    c = Config()
    c.author = "ValiantBunny"
    c.children_watermark = "bottom"
    c.with_shadow = True
    img = Image.open('test/data/test_in.jpg')
    exif_info, exif_origin = exif.get_exif_info(img)
    img = draw_watermark('video_use_white_background', img, c, exif_info)
    save_resize(img).save("test/test_video_use_video_use_white_background.jpg", exif=piexif.dump(exif_origin))


if __name__ == '__main__':
    test_bottom_watermark()
    test_bottom_frame()
    test_video_use()
    test_video_use_2()
