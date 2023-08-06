from random import randint
from matplotlib import colors

__all__ = ["parse_color"]

COLORMAP = [
    (255, 0, 255),
    (0, 255, 0),
    (0, 128, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 128, 255),
    (128, 255, 0),
    (255, 0, 128),
    (128, 255, 255),
    (255, 255, 255),
    (255, 255, 128),
    (255, 128, 0),
    (128, 0, 255),
    (0, 0, 255),
    (0, 255, 128),
    (255, 0, 0)
]


def parse_color(color):
    if isinstance(color, tuple):
        return color
    elif color == -1:
        return tuple(randint(0, 255) for _ in range(3))
    elif isinstance(color, int):
        return COLORMAP[color % len(COLORMAP)]
    elif isinstance(color, str):
        if not color.startswith("#"):
            color = colors._colors_full_map[color]
        color_rgb = colors.to_rgb(color)
        return tuple(int(c * 255) for c in color_rgb)
