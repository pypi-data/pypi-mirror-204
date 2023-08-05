"""
'CHROMAT.swatch.swatches'
copyright (c) 2023 hexbenjamin
full license available at /COPYING
"""

from colorsys import rgb_to_hsv, hsv_to_rgb
import random
from typing import (
    Iterable,
    Literal,
    Optional,
    Tuple,
)

from rich.text import Text

from .props import SwatchProp, SwatchTupleProp
from ..utility import SwatchText, get_contrast, parse_hex

# > CONSTANTS <

SCALES = {
    "rgb": [255, 255, 255],
    "hsv": [360, 100, 100],
    "r": 255,
    "g": 255,
    "b": 255,
    "h": 360,
    "s": 100,
    "v": 100,
}


# > CLASSES <
class Swatch:
    """
    A color swatch object.
    """

    def __init__(
        self,
        color: Tuple[int, int, int] = (255, 255, 255),
        mode: Literal["rgb", "hsv"] = "rgb",
        name: Optional[str] = None,
    ) -> None:
        """
        Initialize a Swatch object from a tuple of ints.

        Parameters
        ----------
        color : Tuple[int, int, int], optional
            Input color values as integers
            default (255, 255, 255)
        mode : Literal["rgb", "hsv"], optional
            Mode for interpreting the input color
            default "rgb"
        name : str, optional
            Optional name for the swatch when used in Palettes
            default "Swatch"
        """
        if mode == "rgb":
            self._init_rgb(color)
        elif mode == "hsv":
            self._init_hsv(color)

        self.hex = f"#{self.r.i:02x}{self.g.i:02x}{self.b.i:02x}"
        self.name = name if name is not None else self.hex
        self.relative_luminance = self.get_relative_luminance()

    def _init_rgb(self, color: Tuple[int, int, int]):
        """
        Calculate HSV values from RGB values and assign all properties.

        Parameters
        ----------
        color : tuple[int, int, int]
            RGB tuple to use for initialization.
        """
        self.rgb = SwatchTupleProp(color, "rgb")
        self.r, self.g, self.b = [
            SwatchProp(c, m)
            for c, m in zip(
                color,
                "rgb",
            )
        ]
        self.hsv = SwatchTupleProp(rgb_to_hsv(*self.rgb.f), "hsv")
        self.h, self.s, self.v = [
            SwatchProp(c, m)
            for c, m in zip(
                self.hsv.f,
                "hsv",
            )
        ]

    def _init_hsv(self, color: Tuple[int, int, int]):
        """
        Calculate RGB values from HSV values and assign all properties.

        Parameters
        ----------
        color : tuple[int, int, int]
            HSV tuple to use for initialization.
        """
        self.hsv = SwatchTupleProp(color, "hsv")
        self.h, self.s, self.v = [
            SwatchProp(c, m)
            for c, m in zip(
                color,
                "hsv",
            )
        ]
        self.rgb = SwatchTupleProp(hsv_to_rgb(*self.hsv.f), "rgb")
        self.r, self.g, self.b = [
            SwatchProp(c, m)
            for c, m in zip(
                self.rgb.f,
                "rgb",
            )
        ]

    def get_relative_luminance(self):
        """
        Get the relative luminance from the Swatch's RGB values.
        """
        r, g, b = [
            x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
            for x in self.rgb.f
        ]

        r *= 0.2126
        g *= 0.7152
        b *= 0.0722

        return r + g + b

    def pick_accent(self) -> "Swatch":
        best = (0, self.__class__())

        for swatch in self.generate_accent_values():
            contrast = get_contrast(self.rel_lum, swatch.rel_lum)

            if contrast > best[0]:
                best = (contrast, swatch)
            if contrast > 4.20:
                self.accent = swatch
                return swatch

        self.accent = best[1]
        return best[1]

    def generate_accent_values(self) -> Iterable["Swatch"]:
        # shuffle range 0-100 for value to test
        values = list(range(0, 101, 2))
        random.shuffle(values)
        for value in values:
            # generate new swatch with 10% swatch's original saturation
            # and a random value from 0-100.
            yield Swatch(
                (
                    self.h.i,
                    self.s.i // 10,
                    value,
                ),
                mode="hsv",
                name=f"{self.name}-accent",
            )

    @classmethod
    def from_hex(cls, hex: str, name: Optional[str] = None) -> "Swatch":
        return cls(parse_hex(hex), mode="rgb", name=name)

    @classmethod
    def from_rgb(
        cls, rgb: Tuple[int, int, int], name: Optional[str] = None
    ) -> "Swatch":
        return cls(rgb, mode="rgb", name=name)

    @classmethod
    def from_hsv(
        cls, hsv: Tuple[int, int, int], name: Optional[str] = None
    ) -> "Swatch":
        return cls(hsv, mode="hsv", name=name)

    @property
    def red(self) -> SwatchProp:
        return self.r

    @property
    def green(self) -> SwatchProp:
        return self.g

    @property
    def blue(self) -> SwatchProp:
        return self.b

    @property
    def hue(self) -> SwatchProp:
        return self.h

    @property
    def saturation(self) -> SwatchProp:
        return self.s

    @property
    def value(self) -> SwatchProp:
        return self.v

    @property
    def rel_lum(self) -> float:
        return self.relative_luminance

    def __repr__(self) -> str:
        return f"Swatch({self.hex})"

    def __str__(self) -> str:
        return self.hex

    def __rich__(self) -> Text:
        return Text.assemble(
            "Swatch('",
            SwatchText(self.hex, self.name),
            "')",
        )
