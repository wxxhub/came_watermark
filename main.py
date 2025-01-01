import argparse
import os.path
from PIL import Image

import exif
from watermark.draw import draw_watermark
from watermark.config import Config
import piexif
from concurrent.futures import ThreadPoolExecutor


def args_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('file', type=str, nargs=1, default="", help="image file")
    parser.add_argument('-f', '--file', type=str, nargs=1, default="", help="image file")
    parser.add_argument('-a', '--author', type=str, default="", help="image author")
    parser.add_argument('-i', '--intput_dir', type=str, default="", help="image input file")
    parser.add_argument('-o', '--output_dir', type=str, default="", help="image output file")
    parser.add_argument('-d', '--draw_type', type=str, default="bottom", help="draw_type ['bottom', 'bottom_frame', "
                                                                              "'video_use']")
    parser.add_argument('-s', '--with_shadow', type=bool, default=False, help="image with shadow")
    parser.add_argument('-c', '--children', type=str, default="", help="children type")
    parser.add_argument('-t', '--thread', type=str, default="", help="children type")
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


def process(f, intput_dir, output_dir, config, draw_type):
    support_file_type = ['jpg', 'jpeg', 'png', 'raw', "JPG", "JPEG", "PNG"]

    support = False
    for s in support_file_type:
        if s in f:
            support = True
            break

    if not support:
        return "不支持的文件类型:" + f

    file = os.path.join(intput_dir, f)
    # out_file_name = 'm_' + f
    out_file_name = f
    save_file = os.path.join(output_dir, out_file_name)
    add_watermark(config, file, save_file, draw_type)

    return 'save image ' + save_file


def main():
    c = Config()

    # TODO 配置读取
    args = args_parser()
    print(args)

    c.author = args.author
    output_dir = args.output_dir
    draw_type = args.draw_type
    c.with_shadow = args.with_shadow
    c.children_watermark = args.children

    if len(args.file) != 0:
        if output_dir == "":
            output_dir = os.path.abspath(".")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file = args.file[0]
        file_name = os.path.basename(args.file[0])
        print("file_name ", file_name)
        save_file = os.path.join(output_dir, file_name)
        add_watermark(c, file, save_file, draw_type)
        print('save image ', save_file)

        return

    if len(args.intput_dir) != 0:
        files = os.listdir(args.intput_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print("file num:", len(files))
        sum = len(files)
        i = 1
        futures = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for f in files:
                futures.append(executor.submit(process, f, args.intput_dir, args.output_dir, c, draw_type))

            for f in futures:
                print(f.result())
                print("进度:", i, "/", sum)
                i += 1
        return

    return


if __name__ == '__main__':
    main()
