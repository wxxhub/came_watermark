import argparse
import os.path
from PIL import Image

import exif
from watermark.draw import draw_watermark
from watermark.config import Config
import piexif


def args_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('file', type=str, nargs=1, default="", help="image file")
    parser.add_argument('-f', '--file', type=str, nargs=1, default="", help="image file")
    parser.add_argument('-a', '--author', type=str, default="", help="image author")
    parser.add_argument('-i', '--intput_dir', type=str, default="", help="image input file")
    parser.add_argument('-o', '--output_dir', type=str, default="", help="image output file")
    parser.add_argument('-d', '--draw_type', type=str, default="bottom", help="draw_type ['bottom', 'bottom_frame', "
                                                                        "'video_use']")
    return parser.parse_args()


def add_watermark(config, file, outfile, draw_type):
    img = Image.open(file)

    exif_info, exif_origin = exif.get_exif_info(img)
    if config.author != "":
        exif_info.Copyright = config.author

    if exif_info.Orientation == 3:
        img = img.transpose(Image.ROTATE_180)
    elif exif_info.Orientation == 6:
        img = img.transpose(Image.ROTATE_270)
        t = exif_info.ExifImageWidth
        exif_info.ExifImageWidth = exif_info.ExifImageHeight
        exif_info.ExifImageHeight = t
    elif exif_info.Orientation == 8:
        img = img.transpose(Image.ROTATE_90)
        t = exif_info.ExifImageWidth
        exif_info.ExifImageWidth = exif_info.ExifImageHeight
        exif_info.ExifImageHeight = t

    img = draw_watermark(draw_type, img, config, exif_info)

    if exif_info.Orientation == 3:
        img = img.transpose(Image.ROTATE_180)
    elif exif_info.Orientation == 6:
        img = img.transpose(Image.ROTATE_90)
        t = exif_info.ExifImageWidth
        exif_info.ExifImageWidth = exif_info.ExifImageHeight
        exif_info.ExifImageHeight = t
    elif exif_info.Orientation == 8:
        img = img.transpose(Image.ROTATE_270)
        t = exif_info.ExifImageWidth
        exif_info.ExifImageWidth = exif_info.ExifImageHeight
        exif_info.ExifImageHeight = t
    img.save(outfile, exif=piexif.dump(exif_origin))
    return

def main():
    c = Config()

    # TODO 配置读取
    args = args_parser()
    print(args)

    c.author = args.author
    output_dir = args.output_dir
    draw_type = args.draw_type

    if len(args.file) != 0:
        if output_dir == "":
            output_dir = os.path.abspath(".")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file = args.file[0]
        file_name = os.path.basename(args.file[0])
        print("file_name ", file_name)
        save_file = os.path.join(output_dir, 'm_'+file_name)
        add_watermark(c, file, save_file, draw_type)
        print('save image ', save_file)

        return

    if len(args.intput_dir) != 0:
        files = os.listdir(args.intput_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print("file num:", len(files))
        i = 1
        for f in files:
            file = os.path.join(args.intput_dir, f)
            out_file_name = 'm_' + f
            save_file = os.path.join(output_dir, out_file_name)
            add_watermark(c, file, save_file, draw_type)

            print('save image ', i, save_file)
            i += 1

        return

    return


if __name__ == '__main__':
    main()
