import piexif
from PIL import Image
from PIL.ExifTags import TAGS


class ExifInfo:
    Copyright = ""
    Model = ""
    Make = ""
    ExifImageWidth: int
    ExifImageHeight:int
    FocalLength = 0
    FNumber:float
    ExposureTime = ""
    DateTimeOriginal = ""
    ISOSpeedRatings = ""
    Orientation = ""
    FocalLengthIn35mmFilm = ""


def get_exif_info(img: Image) -> (ExifInfo, dict):
    info = img._getexif()
    exif_dict = piexif.load(img.info['exif'])

    _infos = {}
    for k, v in info.items():
        decoded_attr = TAGS.get(k, k)
        _infos[decoded_attr] = v

    exifInfo = ExifInfo()
    exifInfo.__dict__.update(_infos)
    exifInfo.ExifImageWidth = img.width
    exifInfo.ExifImageHeight = img.height
    return exifInfo, exif_dict
