import sys

import cv2
import numpy
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


def read_image(image_path, grey: bool = False, to_rgb: bool = False):
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


def get_video_info(video_path):
    """
    获取帧速率、帧数、宽度和高度
    :param video_path: 视频文件地址
    :return: 帧数、宽度、高度和帧速率。如果视频文件无法打开，则返回None。
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频文件是否成功打开
    if not cap.isOpened():
        return None

    # 获取帧速率、帧数、宽度和高度
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # 释放VideoCapture对象
    cap.release()

    # 返回帧数、宽度、高度和帧速率
    return frames_count, fps, height, width


def read_video(video_path, stop: int = sys.maxsize, step: int = 1, to_rgb=False):
    """
    这个函数可以读取视频文件，并返回指定范围内的帧。

    :param video_path: 视频文件路径
    :param start: 要读取的起始帧索引（默认为 0）
    :param stop: 要读取的结束帧索引（默认为 sys.maxsize，即读取所有帧）
    :param step: 读取帧的步长（默认为 1）
    :param to_rgb: 是否转化为RGB图像（默认为 False，保持和cv2返回结果一致）
    :return: 读取成功返回一个代表对应帧所组成的numpy数组，读取失败返回None
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None

    # 结束帧数不应超过总帧数
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    stop = min(frames_count, stop)

    # cap_iter = iter(lambda: cap.read(), null)

    # 按给定的范围读取视频帧
    # 由于视频不能跳帧读取，所以先读取完整的一段，再筛选其中符合特定步长的帧
    video = []
    for i in range(stop):
        # 只选取其中符合特定步长的帧
        if i % step == 0:
            ret, frame = cap.read()
            if ret:
                if to_rgb:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video.append(frame)
        else:
            ret = cap.grab()

        if not ret:
            break

    cap.release()
    return numpy.stack(video, axis=0)
