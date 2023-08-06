import cv2
from PIL import Image


def get_image_info(image_path):
    """
    要获取图像的尺寸，最快的方式是使用Pillow库中的Image类，而不是使用OpenCV。

    :param image_path: 图像路径
    :return:  width, height
    """
    with Image.open(image_path) as img:
        # 获取图像尺寸
        width, height = img.size

    return height, width


def read_image(image_path, grey: bool = False, to_rgb: bool = True):
    """
    读取图像函数

    :param image_path: 图像路径
    :param grey: 是否将图像转换为灰度图像，默认为False
    :param to_rgb: 是否将图像转换为RGB格式，默认为True
    :return: 读取到的图像数组
    """
    if grey:
        # 读取灰度图像
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        # 读取彩色图像
        image = cv2.imread(image_path)
        if to_rgb:
            # 将BGR格式转换为RGB格式
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image
