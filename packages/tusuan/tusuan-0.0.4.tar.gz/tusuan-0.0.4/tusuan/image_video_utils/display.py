import matplotlib.pyplot as plt
import numpy
from fastcore.basics import flatten
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def show_multi_images_in_matplotlib(images: list[numpy.array], subtitles=None, col_num=3, title=None):
    subtitles = subtitles if subtitles else [None] * len(images)

    if len(images) != len(subtitles):
        raise ValueError(f"len(images): {len(images)} != len(subtitles): {len(subtitles)}")

    row_num = numpy.ceil(len(images) / col_num).astype(int)
    fig, axs = plt.subplots(nrows=row_num, ncols=col_num)  # type: Figure, Axes
    fig.suptitle(title)

    fig.set_size_inches(4 * col_num, 4 * row_num)
    for ax, img, subtitle in zip(flatten(axs), images, subtitles):  # type: Axes
        ax.set_title(subtitle)
        ax.imshow(img)

    plt.show()
