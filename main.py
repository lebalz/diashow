from typing import List
from image import Image
import config as conf
from PIL import Image as PilImg
from pathlib import Path
import shutil
from composer import Composer


def out_file(fname: str) -> Path:
    return Path(conf.IMAGES_OUT).joinpath(fname)


idx = 1


def save(to_save: List[PilImg.Image]):
    global idx
    to_save.reverse()
    for im in to_save:
        name = str(idx).zfill(4)
        match conf.OUTPUT_FORMAT:
            case 'JPEG':
                im.save(out_file(f'{name}.jpg'), format='JPEG')
            case 'PNG':
                im.save(out_file(f'{name}.png'), format='PNG')
        idx = idx + 1


if conf.CLEANUP:
    out = Path(conf.IMAGES_OUT)
    shutil.rmtree(out)
    out.mkdir()

paths = sorted(Path(conf.IMAGE_SOURCE).iterdir(), key=conf.ORDER_FUNCTIONS[conf.ORDER_BY])
idx = 1

composer = Composer(conf.TARGET_DISPLAY, margin=(conf.MARGIN_HORIZONTAL_PX, conf.MARGIN_VERTICAL_PX))
zoom_composer = Composer(conf.TARGET_DISPLAY, margin=(conf.MARGIN_HORIZONTAL_PX, conf.MARGIN_VERTICAL_PX))
to_save: List[PilImg.Image] = []

for p in paths:
    img = Image(src=p)
    if not conf.ZOOM_SPLITTED:
        zoom_composer.append(Image(pil=img.zoomed_img(conf.ZOOM_FACTOR, conf.ZOOM_CENTER, conf.TARGET_DISPLAY)))
        current_zoom = zoom_composer.compose(conf.ALIGN)
        zoom_composer.reset()
    else:
        current_zoom = None

    if composer.can_append(img):
        composer.append(img)
    else:
        if conf.ZOOM_SPLITTED:
            for im in composer.images:
                zoom_composer.append(Image(pil=im.zoomed_img(
                    conf.ZOOM_FACTOR, conf.ZOOM_CENTER, composer.split_size())))
            to_save.append(zoom_composer.compose(conf.ALIGN))
            zoom_composer.reset()
        to_save.append(composer.compose(conf.ALIGN))
        composer.reset()
        composer.append(img)
        save(to_save)
        to_save.clear()
    if current_zoom:
        to_save.append(current_zoom)
if composer.length > 0:
    to_save.append(composer.compose(conf.ALIGN))
save(to_save)
