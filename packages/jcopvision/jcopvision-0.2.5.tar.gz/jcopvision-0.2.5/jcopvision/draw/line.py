import cv2
import numpy as np
from jcopvision.utils import denormalize_image, parse_color, denormalize_landmark

__all__ = ["draw_single_line"]


def draw_single_line(frame, pt1, pt2, color=-1, thickness=1):
    '''
    Draw a line


    === Input ===
    frame: array
        image / frame to be drawn

    pt1, pt2: (int, int) or (float, float)
        start and end point of the line.

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

    if not isinstance(pt1[0], int):
        pt1 = tuple(denormalize_landmark(frame, pt1).astype(int))
    
    if not isinstance(pt2[0], int):
        pt2 = tuple(denormalize_landmark(frame, pt2).astype(int))        

    cv2.line(frame, pt1, pt2, color, thickness)
    return frame
