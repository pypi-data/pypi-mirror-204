import sys

import cv2
import numpy


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
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 释放VideoCapture对象
    cap.release()

    # 返回帧数、宽度、高度和帧速率
    return frames_count, width, height, fps


def read_video(video_path, stop: int = sys.maxsize, step: int = 1, to_rgb=True):
    """
    这个函数可以读取视频文件，并返回指定范围内的帧。

    :param video_path: 视频文件路径
    :param start: 要读取的起始帧索引（默认为 0）
    :param stop: 要读取的结束帧索引（默认为 sys.maxsize，即读取所有帧）
    :param step: 读取帧的步长（默认为 1）
    :return: 读取成功返回一个代表对应帧所组成的numpy数组，读取失败返回None
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None

    # 结束帧数不应超过总帧数

    frames_count, width, height, fps = get_video_info(video_path)
    stop = min(frames_count, stop)

    # cap_iter = iter(lambda: cap.read(), null)

    # 按给定的范围读取视频帧
    # 由于视频不能跳帧读取，所以先读取完整的一段，再筛选其中符合特定步长的帧
    video = []
    for i in range(0, stop):
        ret, frame = cap.read()
        if ret:
            if to_rgb:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video.append(frame)
        else:
            break

    # 只选取其中符合特定步长的帧
    video = video[slice(0, stop, step)]
    cap.release()

    return numpy.stack(video, axis=0), fps
