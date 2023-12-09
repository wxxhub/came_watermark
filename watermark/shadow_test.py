from PIL import Image, ImageDraw

if __name__ == '__main__':
    # 创建一个新的图像

    image = Image.new('RGB', (500, 500), color=(255, 255, 255))

    # 创建画笔

    draw = ImageDraw.Draw(image)

    # 定义框的坐标和颜色范围

    box = (100, 100, 300, 300)  # (left, upper, right, lower)

    colors = [(i, i, i) for i in range(256)]  # 灰度颜色范围

    for i in range[1, 20]:
        print(i)
        px1 = 100 - i
        py1 = 100 - i
        px2 = 300 + i
        py2 = 400 + i
        for x in range(px1, px2+1):
            draw.point((x, py1), fill=(220 + i, 220 + i, 220 + i))
            draw.point((x, py2), fill=(220 + i, 220 + i, 220 + i))

        for y in range(py1, py2+1):
            draw.point((px1, y), fill=(220 + i, 220 + i, 220 + i))
            draw.point((px2, y), fill=(220 + i, 220 + i, 220 + i))

    image.show()
