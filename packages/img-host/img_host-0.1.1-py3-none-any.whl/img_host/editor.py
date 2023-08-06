from io import BytesIO

from PIL import Image


class ImageEditor:
    def __init__(self, image: bytes, ratio: float):
        self._img = Image.open(BytesIO(image))
        self._ratio = ratio

    @property
    def image(self) -> bytes:
        io = BytesIO()
        self._img.save(io, "PNG")
        return io.getvalue()

    def crop(self):
        width = self._img.width
        height = self._img.height
        left_edge = (width - self.crop_width) / 2
        right_edge = width - left_edge
        box = int(left_edge), 0, int(right_edge), height
        self._img = self._img.crop(box)

    @property
    def crop_width(self) -> float:
        value = self._img.height * self._ratio
        if self._img.width < value:
            raise PhotoTooNarrow
        return value


class PhotoTooNarrow(ValueError):
    def __str__(self) -> str:
        return "Image is too narrow."
