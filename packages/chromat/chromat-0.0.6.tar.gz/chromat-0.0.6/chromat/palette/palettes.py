"""
'CHROMAT.palette.palettes'
copyright (c) 2023 hexbenjamin
full license available at /COPYING
"""

from typing import Iterable

from ..swatch import Swatch


class Palette:
    def __init__(self, *swatches: Swatch) -> None:
        self.swatches = swatches

    def __iter__(self) -> Iterable[Swatch]:
        return iter(self.swatches)
