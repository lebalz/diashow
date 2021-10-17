from typing import Literal, Tuple
from PIL import Image as PilImg
from pathlib import Path


class Image:
    def __init__(self, src: Path | None = None, pil: PilImg.Image | None = None) -> None:
        if src is None and pil is None:
            raise Exception('Either src or pil must be given!')
        if src is not None:
            self.source = src
            self.img = PilImg.open(src)
        elif pil is not None:
            self.source = None
            self.img = pil
        self.box = (self.img.width, self.img.height)
        self.resized_size = (self.img.width, self.img.height)
        self.expands_full_size: bool = True

    @property
    def ratio(self) -> float:
        '''image ratio height / width
        '''
        return self.img.height / self.img.width

    @property
    def box(self):
        return self.__box

    @box.setter
    def box(self, box: Tuple[int, int]):
        self.__box = box
        self.expands_full_size = True
        if self.is_landscape:
            w = self.box[0]
            h = int(self.ratio * self.box[0])
            if h > self.box[1]:
                h = self.box[1]
                w = int(self.box[1] / self.ratio)
                self.expands_full_size = False
        else:
            w = int(self.box[1] / self.ratio)
            h = self.box[1]
            if w > self.box[0]:
                self.expands_full_size = False
                w = self.box[0]
                h = int(self.box[0] * self.ratio)
        self.resized_size = (w, h)

    @property
    def is_landscape(self):
        return self.img.width > self.img.height

    @property
    def size(self):
        if self.is_landscape:
            return self.resized_size[1]
        return self.resized_size[0]

    @property
    def raw_size(self):
        return (self.img.width, self.img.height)

    @property
    def orientation(self) -> Literal['landscape', 'portrait']:
        if self.is_landscape:
            return 'landscape'
        return 'portrait'

    def resized_img(self):
        return self.img.resize(self.resized_size, resample=PilImg.BICUBIC)

    def zoomed_img(self, zoom: float, zoom_center: Tuple[float, float], size: Tuple[int, int]):
        target_ratio = size[1] / size[0]
        w, h = self.img.size
        x = int(w * zoom_center[0])
        y = int(h * zoom_center[1])
        zoom2 = zoom * 2
        if x - w / zoom2 < 0:
            x = w / zoom2
        elif x + w / zoom2 > w:
            x = w - w / zoom2
        left = int(x - w / zoom2)
        right = int(x + w / zoom2)
        w_new = right - left
        h_new = w_new * target_ratio
        h_top = h_new * zoom_center[1]
        h_bottom = h_new - h_top
        top = int(max(y - h_top, 0))
        bottom = int(min(y + h_bottom, h))
        return self.img.crop((left, top, right, bottom))
