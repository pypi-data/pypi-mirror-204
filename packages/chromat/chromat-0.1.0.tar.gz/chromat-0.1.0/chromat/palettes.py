from typing import List, Optional

from rich.panel import Panel
from rich.text import Text

from .swatches import Swatch


class Palette:
    def __init__(self, swatches: List[Swatch], focus: int = 0) -> None:
        self.swatches = swatches
        self.focus = self.swatches[focus]

    def map(
        self,
        source: Swatch = None,
    ) -> None:
        shifts = [
            (source.hue - self.focus.hue),
            (source.saturation - self.focus.saturation),
            (source.luminance - self.focus.luminance),
        ]

        for sw in self.swatches:
            self.apply_shifts(swatch=sw, shifts=shifts)

    def apply_shifts(self, swatch: Swatch, shifts: List[Optional[int]]):
        for sh, mode in zip(shifts, ["hue", "saturation", "luminance"]):
            if sh is not None:
                new = getattr(swatch, mode) + sh
                if mode == "hue":
                    new = (new + 360) % 360
                else:
                    new = 0 if new < 0 else new
                    new = 100 if new > 100 else new
                setattr(swatch, mode, new)

    def __len__(self):
        return len(self.swatches)

    def __getitem__(self, index):
        return self.swatches[index]

    def __iter__(self):
        return iter(self.swatches)

    def __repr__(self):
        return str(self.swatches)
