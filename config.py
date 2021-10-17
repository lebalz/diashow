import os
from typing import Literal, Tuple
IMAGE_SOURCE = 'C:\\Users\\bauz\\Pictures\\2019 - Best Of US'   # von hier werden die Fotos gelesen
IMAGES_OUT = './out'        # hierhin wird die Diashow gespeichert
CLEANUP: bool = True              # soll der output Ordner zuerst gelöscht werden?

# gibt alle N prozessierter Bilder eine Nachricht aus
REPORT_INTERVAL = 20

# width x height
TARGET_DISPLAY: Tuple[int, int] = (2160, 3840)

GAP_HORIZONTAL_PX = 50
GAP_VERTICAL_PX = 50
MAX_SPLITS_VERTICAL = 0
MAX_SPLITS_HORIZONTAL = -1
ALIGN: Literal['start', 'center', 'end', 'space-between'] = 'space-between'

# breite/höhe, falls Bild ein Bild-Verhältnis hat,
# das grösser ist als der Threshold, dann wird es als
# Breitformat gewertet...
LANDSCAPE_RATIO_THRESHOLD = 4 / 5


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
ORDER_BY: Literal['name', 'date'] = 'name'

ORDER_FUNCTIONS = {
    'name': os.path.basename,
    'date': os.path.getmtime
}
