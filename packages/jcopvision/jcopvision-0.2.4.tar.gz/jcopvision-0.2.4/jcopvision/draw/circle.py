import cv2
import numpy as np
from jcopvision.utils import denormalize_image, parse_color, denormalize_landmark

__all__ = ["draw_single_circle"]


def draw_single_circle(frame, center, radius, color=-1, thickness=1):
    '''
    Draw a circle


    === Input ===
    frame: array
        image / frame to be drawn

    center: (int, int) or (float, float)
        location to draw the circle.

    color: int or (int, int, int) or str
        The color of the bounding box
        If int, it would be map to default colormap using jcopvision.utils.parse_color. Use -1 for random color.
        If (int, int, int), color in BGR format
        If str, it will be parsed such in matplotlib colors. Hex code is also accepted

    thickness: int
        The circle and text thickness


    === Return ===
    frame: array
        annotated image / frame
    '''
    frame = frame.copy()
    frame = denormalize_image(frame)

    color = parse_color(color)

    if not isinstance(center[0], int):
        center = tuple(denormalize_landmark(frame, center).astype(int))    

    cv2.circle(frame, center, radius, color, thickness)
    return frame
