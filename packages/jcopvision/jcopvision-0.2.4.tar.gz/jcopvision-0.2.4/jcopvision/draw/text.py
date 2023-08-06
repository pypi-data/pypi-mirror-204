import cv2
from jcopvision.utils import denormalize_image, parse_color, denormalize_landmark

__all__ = ["add_text"]


def add_text(frame, text, position=(0.05, 0.1), size=1, thickness=2, color=-1, font=cv2.FONT_HERSHEY_DUPLEX, line_type=cv2.LINE_AA):
    '''
    Add text


    === Input ===
    frame: array
        image / frame to be drawn

    text: str
        text to display in image

    position: (int, int) or (float, float)
        bottom left of the text position
        If float, it would be denormalized with the frame size
        If int, it represents the pixel location

    size: int
        font scale factor (multiplied to font base size)

    thickness: int
        Text thickness in px        

    color: int or (int, int, int) or str
        The color of the bounding box
        If int, it would be map to default colormap using jcopvision.utils.parse_color. Use -1 for random color.
        If (int, int, int), color in BGR format
        If str, it will be parsed such in matplotlib colors. Hex code is also accepted

    font: cv2.FONT
        opencv font

    line_type: cv2.LINE
        opencv line type    


    === Return ===
    frame: array
        annotated image / frame
    '''
    frame = frame.copy()
    frame = denormalize_image(frame)

    color = parse_color(color)

    if not isinstance(position[0], int):
        position = tuple(denormalize_landmark(frame, position).astype(int))
    
    frame = cv2.putText(frame, text, position, font, size, color, thickness, line_type)    
    return frame
