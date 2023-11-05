from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

from .config import Config
from .watermark import Watermark
import exif

ElementHeight = 500
ElementPadding = 200
ElementRealHeight = ElementHeight + ElementPadding * 2
ElementCenter = ElementRealHeight / 2

FONT_PADDING = 10
FONT_SIZE = int(ElementHeight / 2) - FONT_PADDING
FONT = ImageFont.truetype('fonts/SourceHanSansCN-Light.otf', FONT_SIZE)
BOLD_FONT = ImageFont.truetype('fonts/SourceHanSansCN-Bold.otf', FONT_SIZE)

ExifPadding = 200


def make_exif_image(exif_info: exif.ExifInfo):
    focal_length = str(exif_info.FocalLengthIn35mmFilm) + 'mm'
    f_number = 'F' + str([exif_info.FNumber, int(exif_info.FNumber)][int(exif_info.FNumber) == exif_info.FNumber])
    exposure_time = str(exif_info.ExposureTime.real)
    iso = 'ISO' + str(exif_info.ISOSpeedRatings)
    shot_param = '  '.join((focal_length, f_number, exposure_time, iso))
    original_date_time = datetime.strftime(parse_datetime(exif_info.DateTimeOriginal), '%Y-%m-%d %H:%M')

    l1 = BOLD_FONT.getlength(exif_info.Model)
    l2 = FONT.getlength(original_date_time)
    max_l = int(max(l1, l2)) + ElementPadding * 2
    left_img = Image.new('RGB', (max_l, ElementRealHeight), color='white')
    left_img_draw = ImageDraw.Draw(left_img)
    left_img_draw.text((ElementPadding, ElementCenter - BOLD_FONT.getsize(exif_info.Model)[1]), exif_info.Model,
                       font=BOLD_FONT, fill='black')
    left_img_draw.text(
        (ElementPadding, ElementPadding + ElementHeight + FONT_PADDING - FONT.getsize(original_date_time)[1]),
        original_date_time, font=FONT, fill='gray')

    # debug line
    # left_img_draw.line((0, ElementPadding, max_l, ElementPadding), fill='gray', width=5)  # top line
    # left_img_draw.line((0, ElementCenter, max_l, ElementCenter), fill='gray', width=10)  # center line
    # left_img_draw.line((0, ElementPadding + ElementHeight, max_l, ElementPadding + ElementHeight), fill='gray', width=5)  # bottom line
    # left_img_draw.line((ElementPadding, 0, ElementPadding, ElementRealHeight), fill='gray', width=5)
    # left_img.show("left")
    # print("left")

    user = "BY " + exif_info.Copyright
    l1 = BOLD_FONT.getlength(shot_param)
    l2 = FONT.getlength(user)
    max_l = int(max(l1, l2)) + ElementPadding * 2
    right_img = Image.new('RGB', (max_l, ElementRealHeight), color='white')
    right_img_draw = ImageDraw.Draw(right_img)
    right_img_draw.text((ElementPadding, ElementCenter - BOLD_FONT.getsize(shot_param)[1]), shot_param, font=BOLD_FONT,
                        fill='black')
    right_img_draw.text(
        (ElementPadding, ElementPadding + ElementHeight + FONT_PADDING - FONT.getsize(user)[1]),
        user, font=FONT, fill='gray')

    # debug line
    # right_img_draw.line((0, ElementPadding, max_l, ElementPadding), fill='gray', width=5)  # top line
    # right_img_draw.line((0, ElementCenter, max_l, ElementCenter), fill='gray', width=10)  # center line
    # right_img_draw.line((0, ElementPadding + ElementHeight, max_l, ElementPadding + ElementHeight), fill='gray',
    #                     width=5)  # bottom line
    # right_img_draw.line((ElementPadding, 0, ElementPadding, ElementRealHeight), fill='gray', width=5)
    # right_img.show("right")
    # print('right')

    logo = get_logo(exif_info)

    if exif_info.ExifImageWidth > exif_info.ExifImageHeight:
        w = int((left_img.width + logo.width + right_img.width) * 2)
    else:
        w = int((left_img.width + logo.width + right_img.width) * 1.5)
    if w < exif_info.ExifImageWidth:
        w = exif_info.ExifImageWidth

    exif_h = ElementRealHeight + ElementPadding * 2
    exif_img = Image.new('RGB', (w, exif_h), color='white')
    exif_img.paste(left_img, (ElementPadding, ElementPadding))
    exif_img.paste(logo, (w - logo.width - right_img.width - ElementPadding, ElementPadding))
    exif_img.paste(right_img, (w - right_img.width - ElementPadding, ElementPadding))
    exif_draw = ImageDraw.Draw(exif_img)

    ## 分割线
    l_x = w - right_img.width - ElementPadding
    exif_draw.line(
        (l_x, ElementPadding, l_x, exif_h - ElementPadding),
        fill='gray', width=20)

    resize_height = int((exif_info.ExifImageWidth / w) * exif_h)
    return exif_img.resize((exif_info.ExifImageWidth, resize_height), Image.Resampling.LANCZOS)


def parse_datetime(datetime_string):
    return datetime.strptime(datetime_string, '%Y:%m:%d %H:%M:%S')


def get_logo(exif_info: exif.ExifInfo):
    if exif_info.Make == 'SONY':
        logo = Image.open("logos/sony.png")
    elif exif_info.Make == 'NIKON':
        logo = Image.open("logos/nikon1.png")
    elif exif_info.Make == 'Canon':
        logo = Image.open("logos/canon.png")
    elif exif_info.Make == 'FUJIFILM':
        logo = Image.open("logos/fujifilm.png")
    elif exif_info.Make == 'Panasonic':
        logo = Image.open("logos/lumix.png.png")
    else:
        logo = Image.open("logos/sony.png")

    # 让图标大点，所以使用ElementPadding
    resize_width = int(ElementRealHeight / logo.height * logo.width)
    logo = logo.resize((resize_width, ElementRealHeight), Image.Resampling.LANCZOS)

    padding_logo = Image.new('RGB', (logo.width + ElementPadding * 2, ElementRealHeight), color='white')
    padding_logo.paste(logo, (ElementPadding, 0))
    return padding_logo


class BottomWatermark(Watermark):
    def draw(self, img: Image, config: Config, exif_info: exif.ExifInfo) -> Image:
        if config.author != "":
            exif_info.Copyright = config.author

        exif_img = make_exif_image(exif_info)

        result_img = Image.new('RGB', (img.width, img.height + exif_img.height), color='white')
        result_img.paste(img, (0, 0))
        result_img.paste(exif_img, (0, img.height))
        return result_img
