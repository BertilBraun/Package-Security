from __future__ import annotations
from typing import Tuple

boxt = Tuple[int, int, int, int]

def get_center_from_box(box: boxt) -> tuple[int, int]:
    return box[0] + box[2] // 2, box[1] + box[3] // 2