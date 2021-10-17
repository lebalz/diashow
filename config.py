import os
from typing import Literal, Tuple
IMAGE_SOURCE = './images'   # von hier werden die Fotos gelesen
IMAGES_OUT = './out'        # hierhin wird die Diashow gespeichert
CLEANUP: bool = True              # soll der output Ordner zuerst gelöscht werden?

# width x height
TARGET_DISPLAY: Tuple[int, int] = (2160, 3840)

MARGIN_HORIZONTAL_PX = 50
MARGIN_VERTICAL_PX = 50
ALIGN: Literal['start', 'center', 'end', 'space-between'] = 'center'


ZOOM_FACTOR = 1.8
ZOOM_CENTER: Tuple[float, float] = (0.5, 0.7)

# True: zoomt Bild in seiner Hälfte -> ergibt ein zoomtes Bild
# False: zoomt Bild auf ganzem Bildschirm
ZOOM_SPLITTED: bool = False

OUTPUT_FORMAT: Literal['JPEG', 'PNG'] = 'JPEG'

# 1 = schlechteste Qualität
# 95 = beste JPEG Qualität
OUTPUT_QUALITY: int = 95

# Sortierung der Bilder beim Einlesen
ORDER_BY: Literal['name', 'date'] = 'date'

ORDER_FUNCTIONS = {
    'name': os.path.basename,
    'date': os.path.getmtime
}
