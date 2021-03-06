from typing import List, Literal, Tuple
from image import Image
from PIL import Image as PilImg
from functools import reduce
import config as conf

Align = Literal['vertical', 'horizontal']


class Composer():
    def __init__(self, size: Tuple[int, int], margin: Tuple[int, int]):
        self.images: List[Image] = []
        self.size = size
        self._margin = margin
        self.image_slots = 1

    @property
    def image_slots(self):
        return self.__image_slots

    @property
    def images_expand_fully(self) -> bool:
        return all(im.expands_full_size for im in self.images)

    @image_slots.setter
    def image_slots(self, slots: int):
        self.__image_slots = slots
        if self.length == 0:
            return
        box = self.split_size(slots)
        for im in self.images:
            im.box = box

    @property
    def length(self) -> int:
        return len(self.images)

    @property
    def margin(self):
        if self.is_landscape:
            return self._margin[0]
        return self._margin[1]

    def split_size(self, item_length: int = -1) -> Tuple[int, int]:
        if item_length < 0:
            item_length = self.length
        if item_length < 2:
            return self.size

        margin_sz = (item_length - 1) * self.margin
        if self.is_landscape:
            x = self.size[0]
            y = (self.size[1] - margin_sz) / item_length
            return (x, int(y))
        x = (self.size[0] - margin_sz) / item_length
        y = self.size[1]
        return (int(x), y)

    @property
    def boxes(self) -> List[Tuple[int, int]]:
        if self.length == 0:
            return [self.size]
        sizes = list(map(lambda im: im.resized_size, self.images))
        used = 0
        bx: List[Tuple[int, int]] = []
        for sz in sizes:
            if self.is_landscape:
                # x = (self.size[0] - sz[0]) / 2
                bx.append((int(0), used))
                used += sz[1] + self.margin
            else:
                # y = (self.size[1] - sz[1]) / 2
                bx.append((used, int(0)))
                used += sz[0] + self.margin
        return bx

    @property
    def is_landscape(self) -> None | bool:
        if self.length == 0:
            return None
        return self.images[0].is_landscape

    @property
    def orientation(self):
        if self.length == 0:
            return None
        return self.images[0].orientation

    @property
    def used_height_by_images(self) -> int:
        return reduce(lambda res, img: res + img.resized_size[1], self.images, 0)

    @property
    def used_width_by_images(self) -> int:
        return reduce(lambda res, img: res + img.resized_size[0], self.images, 0)

    @property
    def used_space_by_images(self) -> Tuple[int, int]:
        if self.length == 0:
            return (0, 0)
        return (self.used_width_by_images, self.used_height_by_images)

    @property
    def used_space(self) -> Tuple[int, int]:
        '''including margins
        '''
        if self.length == 0:
            return (0, 0)
        img = self.used_space_by_images
        if self.is_landscape:
            return (img[0], img[1] + (self.length - 1) * self.margin)
        return (img[0] + (self.length - 1) * self.margin, img[1])

    @property
    def available_space(self) -> Tuple[int, int]:
        '''total available space, where margins do count too
        '''
        if self.length == 0:
            return self.size
        used = self.used_space
        return (self.size[0] - used[0], self.size[1] - used[1])

    def append(self, item: Image):
        self.images.append(item)
        self.image_slots = self.length

    def can_append(self, item: Image):
        if self.length == 0:
            return True
        try:
            if self.orientation == item.orientation:
                if self.is_landscape:
                    if conf.MAX_SPLITS_HORIZONTAL >= 0 and self.length > conf.MAX_SPLITS_HORIZONTAL:
                        return False
                else:
                    if conf.MAX_SPLITS_VERTICAL >= 0 and self.length > conf.MAX_SPLITS_VERTICAL:
                        return False

                if self.length < 2:
                    return True
                if not self.images_expand_fully:
                    return False
                # try inserting another image
                self.image_slots = self.length + 1
                if not self.images_expand_fully:
                    return False
                item.box = self.split_size(self.image_slots)
                return item.expands_full_size
            return False
        finally:
            # make sure to revert...
            if self.image_slots != self.length:
                self.image_slots = self.length

    def compose(self, align: Literal['start', 'center', 'end', 'space-between'] = 'start'):
        self.images = sorted(self.images, key=lambda im: im.entropy, reverse=True)
        comp_img = PilImg.new('RGB', self.size)
        if self.length == 0:
            return comp_img
        self.image_slots = self.length
        available = self.available_space
        left_over = (available[0] / self.length, available[1] / self.length)
        shift: Tuple[int, int] = (0, 0)
        for idx, box in enumerate(self.boxes):
            match align:
                case 'center':
                    factor = 0.5 if idx == 0 else 1
                case 'end':
                    factor = 1
                case 'space-between':
                    factor = 0 if idx == 0 else 1 + (1 / (self.length - 1))
                case _:
                    factor = 0
            if self.length == 1:
                shift = (shift[0] + int(factor * left_over[0]), shift[1] + int(factor * left_over[1]))
            elif self.is_landscape:
                shift = (0, shift[1] + int(factor * left_over[1]))
            else:
                shift = (shift[0] + int(factor * left_over[0]), 0)

            box = (box[0] + shift[0], box[1] + shift[1])
            img = self.images[idx].resized_img()
            comp_img.paste(img, box)

        return comp_img

    def reset(self):
        self.images.clear()
        self.image_slots = 0
