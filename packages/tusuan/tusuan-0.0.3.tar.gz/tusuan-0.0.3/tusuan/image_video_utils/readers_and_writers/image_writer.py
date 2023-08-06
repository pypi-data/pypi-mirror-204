import cv2
import numpy


def write_image(image: numpy.ndarray, filename: str, to_bgr=True) -> None:
    """
    将图像写入文件。
    :param image: numpy.array, 输入图像。
    :param filename: str, 输出文件名。
    :return: None
    """
    if to_bgr:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)
