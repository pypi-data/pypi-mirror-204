import cv2
import rpack
import numpy as np
from a_cv_imwrite_imread_plus import open_image_in_cv, save_cv_image
from create_empty_image import create_new_image
from a_cv2_easy_resize import add_easy_resize_to_cv2
from a_cv_imwrite_imread_plus import add_imwrite_plus_imread_plus_to_cv2

add_imwrite_plus_imread_plus_to_cv2()
add_easy_resize_to_cv2()


def create_collage_v2(
    lst: list | tuple,
    maxwidth: int = 1080,
    heightdiv: int = 6,
    widthdiv: int = 2,
    background: tuple = (0, 0, 0),
    save_path: str | None = None,
) -> np.array:
    """
    Creates a collage of images from a list or tuple.

    Args:
        lst (list|tuple): A list or tuple of images - allowed: [file paths, base64, bytes, PIL, urls, np.array].
        maxwidth (int, optional): The maximum width of the collage. Defaults to 1080.
        heightdiv (int, optional): The height division factor. Defaults to 6.
        widthdiv (int, optional): The width division factor. Defaults to 2.
        background (tuple, optional): The background color of the collage. Defaults to (0, 0, 0).
        save_path (str|None, optional): The file path to save the collage. Defaults to None.

    Returns:
        np.array: A NumPy array representing the collage image.
    """
    images = [open_image_in_cv(file, channels_in_output=4) for file in lst]

    images = [
        cv2.easy_resize_image(
            pic,
            width=maxwidth // widthdiv,
            height=None,
            percent=None,
            interpolation=cv2.INTER_AREA,
        )
        if pic.shape[1] > maxwidth // widthdiv
        else pic
        for pic in images
    ]

    images = [
        cv2.easy_resize_image(
            pic,
            width=None,
            height=maxwidth // heightdiv,
            percent=None,
            interpolation=cv2.INTER_AREA,
        )
        for pic in images
    ]

    sizes = [s.shape[:-1][::-1] for s in images]
    positions = rpack.pack(sizes, max_width=maxwidth, max_height=None)
    imsize = rpack.bbox_size(sizes, positions)
    collage = create_new_image(
        width=imsize[1] + 10000, height=imsize[0] + 10000, color=background
    )
    collage = open_image_in_cv(collage, channels_in_output=4)

    ally = []
    allx = []
    for image, size, position in zip(images, sizes, positions):
        y1, x1 = position[1], position[0]
        y2, x2 = y1 + size[1], x1 + size[0]
        ally.extend([y1, y2])
        allx.extend([x1, x2])
        collage[y1:y2, x1:x2, :] = image
    minx = min(allx)
    maxx = max(allx)
    miny = min(ally)
    maxy = max(ally)
    collage = collage[miny:maxy, minx:maxx]
    collage = cv2.easy_resize_image(
        collage, width=maxwidth, height=None, percent=None, interpolation=cv2.INTER_AREA
    )
    if save_path:
        save_cv_image(save_path, collage)

    return collage
