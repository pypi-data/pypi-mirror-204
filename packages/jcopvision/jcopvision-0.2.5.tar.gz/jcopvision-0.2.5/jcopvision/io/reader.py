import cv2, re, io, base64
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path, PosixPath
from jcopvision.exception import MediaToArrayError, UnrecognizedMediaType
from jcopvision.draw.imshow import gray_imshow, bgr_imshow, rgb_imshow

__all__ = ["MediaReader"]

SUPPORTED_VIDEO_TYPES = [".mp4", ".avi", ".mov"]
SUPPORTED_IMAGE_TYPES = [".bmp", ".dib", ".jpg", ".jpeg", ".jp2", ".jpe", ".png", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif"]

CONVERT_MAP = {
    "image_grayscale": {
        "rgb": cv2.COLOR_GRAY2RGB,
        "bgr": cv2.COLOR_GRAY2BGR,
        "rgba": cv2.COLOR_GRAY2RGBA,
        "bgra": cv2.COLOR_GRAY2BGRA,
        "gray": None
    },
    "image_rgb": {
        "rgb": None,
        "bgr": cv2.COLOR_RGB2BGR,
        "rgba": cv2.COLOR_RGB2RGBA,
        "bgra": cv2.COLOR_RGB2BGRA,
        "gray": cv2.COLOR_RGB2GRAY
    },
    "image_rgba": {
        "rgb": cv2.COLOR_RGBA2RGB,
        "bgr": cv2.COLOR_RGBA2BGR,
        "rgba": None,
        "bgra": cv2.COLOR_RGBA2BGRA,
        "gray": cv2.COLOR_RGBA2GRAY
    }
}

class MediaReader:
    """
    An all around media reader built on top of opencv.

    === Example Usage ===
    media = MediaReader("video.mp4")
    for frame in media.read():
        # do something
    media.close()

    === Input ===
    source: "webcam" or str or int
        media source.
        - "webcam": access default webcam, or specify the webcam integer id as in opencv.
        - int: webcam integer id as in opencv
        - str: image or video filepath, or rtsp url
    """
    def __init__(self, source="webcam"):
        self.cam = None
        self.image = None
        self._parse_source(source)

    def _parse_source(self, source):
        source = 0 if source == "webcam" else source
        if isinstance(source, PosixPath):
            if not source.is_file():
                raise FileNotFoundError(f"Please check if '{source}' exists")
            if is_video(source):
                self.input_type = "video"
                self.cam = cv2.VideoCapture(source.as_posix())
            elif is_image(source):
                img = plt.imread(source.as_posix())
                self.image = (img * 255).astype(np.uint8)
                self._set_image_type(self.image.ndim)
            else:
                raise UnrecognizedMediaType(f"Supported media\n- Videos: {', '.join(SUPPORTED_VIDEO_TYPES)}\n- Images: {', '.join(SUPPORTED_IMAGE_TYPES)}")
        elif isinstance(source, int) or source.startswith("rtsp://"):
            self.input_type = "camera"
            self.cam = cv2.VideoCapture(source)
        elif isinstance(source, str):
            if "." in source:
                self._parse_source(Path(source))
            elif ("base64" in source) or (len(source) % 4 == 0):
                img_str = re.sub('^data:image/.+;base64,', '', source)
                try:
                    img = Image.open(io.BytesIO(base64.b64decode(img_str)))
                    self.image = np.array(img)
                    self._set_image_type(self.image.ndim)
                except:
                    raise Exception("File type not supported")
            else:
                raise Exception("File type not supported")
        else:
            raise Exception("File type not supported")

        if self.input_type in ['video', "camera"]:
            self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.aspect_ratio = self.width / self.height
            self.frame_count = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
            self.frame_rate = self.cam.get(cv2.CAP_PROP_FPS)
        else:
            h, w = self.image.shape[:2]
            self.aspect_ratio = w / h
            self.height = int(h)
            self.width = int(w)             

    def _set_image_type(self, n_dim):
        if n_dim == 2:
            self.input_type = "image_grayscale"
        elif n_dim == 3:
            h, w, c = self.image.shape
            if c == 3:
                self.input_type = "image_rgb" 
            elif c == 4:
                self.input_type = "image_rgba"

    def read(self, out_channel="rgb"):
        if self.input_type.startswith("image"):
            conversion = CONVERT_MAP[self.input_type][out_channel]
            if conversion is None:
                return self.image
            return cv2.cvtColor(self.image, conversion)
        else:
            def iter_func():
                while True:
                    cam_on, frame = self.cam.read()
                    if cam_on:
                        yield frame[..., ::-1] if out_channel == "rgb" else frame
                    else:
                        break
            return iter_func()

    def show(self):
        if self.input_type in ["video", "webcam"]:
            return None
        elif self.input_type == "image_grayscale":
            return gray_imshow(self.image)
        elif self.input_type in ["image_rgb", "image_rgba"]:
            return rgb_imshow(self.image)

    def capture(self):
        if self.input_type != "image":
            return next(iter(self.read()))

    def stream(self, transform=None):
        """
        to be used with fastapi StreamingResponse
        >> StreamingResponse(media.stream(), media_type='multipart/x-mixed-replace; boundary=frame')
        """
        while True:
            cam_on, frame = self.cam.read()
            if cam_on:
                if transform is not None:
                    frame = transform(frame)
                success, frame = cv2.imencode(".jpg", frame)
                yield b'--frame\r\n' \
                      b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n'
            else:
                break

    def close(self):
        if self.input_type in ['video', "camera"]:
            self.cam.release()

    def to_array(self, out_channel="rgb"):
        if self.input_type == "video":
            frames = [frame for frame in self.read()]
            frames = np.array(frames).transpose(0, 3, 1, 2)
            if out_channel == "rgb":
                frames = frames[:, ::-1, :, :]
            return frames
        else:
            raise MediaToArrayError("Image / webcam stream could not be converted to array. Input should be a video.")

    def to_base64(self):
        if self.input_type in ["video", "webcam"]:
            return None
        elif self.input_type == "image_grayscale":
            img = Image.fromarray(self.image, mode='L')
        else:
            img = Image.fromarray(self.image)

        # Convert PIL Image to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')

        # Encode bytes to base64 string
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def is_video(fpath):
    return Path(fpath).suffix in SUPPORTED_VIDEO_TYPES


def is_image(fpath):
    return Path(fpath).suffix in SUPPORTED_IMAGE_TYPES

