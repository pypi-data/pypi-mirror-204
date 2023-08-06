from jcopvision.utils import normalize_image

__all__ = ["enhance_brightness", "enhance_contrast"]


def enhance_brightness(image, gain=10):
    image = normalize_image(image)
    gain /= 255
    new_image = image + gain
    return new_image.clip(0, 1)


def enhance_contrast(image, gain=10):
    image = normalize_image(image)
    gain = 1 + gain / 100
    new_image = image * gain
    return new_image.clip(0, 1)
