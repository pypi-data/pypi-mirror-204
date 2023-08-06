import cv2
import einops
import numpy


def write_image(image: numpy.ndarray, filename: str, rgb_to_bgr=False) -> None:
    """
    将图像写入文件。
    :param image: numpy.array, 输入图像。
    :param filename: str, 输出文件名。
    :param rgb_to_bgr: False
    :return: 默认False。
    """
    if rgb_to_bgr:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)

    print(filename, "written")


def write_video(video: numpy.ndarray, filename: str, fps: int = 30, rgb_to_bgr=False) -> None:
    """
    将cv2读取的维度格式FHWC（frame_count, height, width, channel_count）视频帧写入文件。
    如果缺少channel_count维度，则会repeat补上。
    函数接受一个视频帧、一个输出文件名和一个视频帧率（默认为30帧/秒），

    使用OpenCV的VideoWriter函数创建视频写入对象，然后逐帧将视频写入文件。
    最后，释放视频写入对象。注意，为了使写入的视频具有更好的兼容性，我们选择了MP4编码格式。

    :param video: numpy.array, 输入视频帧。
    :param filename: str, 输出文件名。
    :param fps: int, 输出视频帧率。
    :param rgb_to_bgr: 默认False。
    :return: None
    """
    video = numpy.array(video, dtype=numpy.uint16)
    if video.ndim == 4:
        frame_count, height, width, channel_count = video.shape
    elif video.ndim == 3:
        video = einops.repeat(video, "f h w -> f h w c", c=3)
        frame_count, height, width, channel_count = video.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 定义输出视频编码格式
    writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))  # 创建视频写入对象

    for frame in video:
        if rgb_to_bgr:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame)  # 逐帧写入视频

    writer.release()  # 释放视频写入对象

    print(filename, "written")
