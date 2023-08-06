import re

from typing import Literal, Tuple, Union

from rich.text import Text

from colour import Color


# > CONSTANTS <
HEX_PATTERN = re.compile(r"^([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$")
MODES = ["hsl", "rgb"]
RGB_SCALES = (255, 255, 255)
HSL_SCALES = (360, 100, 100)
LETTERS = {
    "r": "red",
    "g": "green",
    "b": "blue",
    "h": "hue",
    "s": "saturation",
    "v": "value",
}


# > CLASSES <
class ColorTuple:
    """
    A class to represent a color tuple, with int and float conversions handy.
    """

    def __init__(
        self,
        values: Tuple[Union[int, float]],
        mode: Literal["rgb", "hsl"],
    ) -> None:
        """
        Initializes an instance of the class with the given values and mode.

        Args:
            values (Tuple[Union[int, float]]): A tuple of numeric values to be
                used to represent a color. Must be of the same type.
            mode (Literal["rgb", "hsl"]): The color mode to be used for the
                values. Must be either "rgb" or "hsl".

        Returns:
            None
        """
        self.update_mode(mode)

        verify_tuple_types(values, self._mode)
        self._values = values

    def update_mode(self, mode: Literal["rgb", "hsl"]):
        """
        Update the current mode of the object.
        This mode is used for scaling between int and float, as well as by the
            Swatch class.

        Args:
            mode (Literal["rgb", "hsl"]): The new mode to set the object to.

        Returns:
            None
        """
        self._mode = mode
        self._scales = eval(f"{mode.upper()}_SCALES")

    @property
    def integer(self) -> int:
        return tuple(
            [
                int(v * s) if isinstance(v, float) else v
                for v, s in zip(self._values, self._scales)
            ]
        )

    @property
    def float(self) -> float:
        return tuple(
            [
                v / s if isinstance(v, int) else v
                for v, s in zip(self._values, self._scales)
            ]
        )


class Swatch:
    def __init__(
        self,
        color: Union[
            str,
            Tuple[int, int, int],
            Tuple[float, float, float],
        ] = "#FFFFFF",
        mode: Literal["rgb", "hsl"] = "rgb",
    ) -> None:
        """
        Initialize a new Color object with the given color and mode.

        Args:
            color (str or Tuple[int, int, int] or Tuple[float, float, float]):
                The color to use, in one of the following formats:
                    - A string representing a hex color code, e.g. "#FF0000"
                        for red.
                    - A tuple of integers representing an RGB color, e.g.
                        (255, 0, 0) for red.
                    - A tuple of floats representing an HSL color, e.g.
                        (0.0, 1.0, 0.5) for red.
            mode (Literal["rgb", "hsl"]): The color mode to use, either "rgb"
                (default) or "hsl".

        Returns:
            None.
        """
        if isinstance(color, str):
            color = parse_hex(color)
            self._mode = "rgb"
        else:
            self._mode = mode

        self._color = Color()

        self.update(ColorTuple(color, mode=self._mode))

    def update(self, value: ColorTuple) -> None:
        mode = value._mode
        setattr(self._color, mode, value.float)
        self.relative_luminance = self.rel_lum
        self.make_accent()

    def get_relative_luminance(self, rgb: Tuple[float]) -> float:
        """
        Get the relative luminance from the Swatch's RGB values.
        """
        r, g, b = [
            x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb
        ]

        r *= 0.2126
        g *= 0.7152
        b *= 0.0722

        return r + g + b

    def make_accent(self) -> None:
        start = self._color
        end = Color("#000") if self.rel_lum > 0.5 else Color("#FFF")

        grad = list(start.range_to(end, steps=16))
        best = [end, 0]

        for s in grad:
            lums = [self.rel_lum, self.get_relative_luminance(s.rgb)]
            contrast = (max(lums) + 0.05) / (min(lums) + 0.05)
            if contrast >= 5:
                self._accent = s
                self._accent_contrast = contrast
                return
            elif contrast > best[1]:
                best = [s, contrast]

        self._accent = best[0]
        self._accent_contrast = best[1]
        return

    def __repr__(self) -> str:
        return self.hex_u

    def __str__(self) -> str:
        return self.hex_u

    def __eq__(self, other: "Swatch") -> bool:
        return self.rgb == other.rgb

    def __rich__(self) -> Text:
        return Text(self.hex_u, style=f"reverse {self.hex_u}")

    # > HEX PROPERTIES
    @property
    def hex_l(self) -> str:
        return self._color.hex_l

    @property
    def hex_u(self) -> str:
        return self._color.hex_l.upper()

    @property
    def hex(self) -> str:
        return self._color.hex_l.strip("#")

    # > ACCENT PROPERTIES
    @property
    def rel_lum(self) -> float:
        return self.get_relative_luminance(self._color.rgb)

    @property
    def accent(self) -> Tuple[Color, float]:
        return self._accent

    # > RGB PROPERTIES
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return ColorTuple(self._color.rgb, mode="rgb").integer

    @rgb.setter
    def rgb(self, value: Tuple[int, int, int]) -> None:
        self.update(ColorTuple(value, mode="rgb"))

    @property
    def red(self) -> int:
        return self.rgb[0]

    @red.setter
    def red(self, value: int) -> None:
        value = (value, self.green, self.blue)
        self.update(ColorTuple(value, mode="rgb"))

    @property
    def green(self) -> int:
        return self.rgb[1]

    @green.setter
    def green(self, value: int) -> None:
        value = (self.red, value, self.blue)
        self.update(ColorTuple(value, mode="rgb"))

    @property
    def blue(self) -> int:
        return self.rgb[2]

    @blue.setter
    def blue(self, value: int) -> None:
        value = (self.red, self.green, value)
        self.update(ColorTuple(value, mode="rgb"))

    # > HSL PROPERTIES
    @property
    def hsl(self) -> Tuple[int, int, int]:
        return ColorTuple(self._color.hsl, mode="hsl").integer

    @hsl.setter
    def hsl(self, value: Tuple[int, int, int]) -> None:
        self.update(ColorTuple(value, mode="hsl"))

    @property
    def hue(self) -> int:
        return self.hsl[0]

    @hue.setter
    def hue(self, value: int) -> None:
        value = (value, self.saturation, self.luminance)
        self.update(ColorTuple(value, mode="hsl"))

    @property
    def saturation(self) -> int:
        return self.hsl[1]

    @saturation.setter
    def saturation(self, value: int) -> None:
        value = (self.hue, value, self.luminance)
        self.update(ColorTuple(value, mode="hsl"))

    @property
    def luminance(self) -> int:
        return self.hsl[2]

    @luminance.setter
    def luminance(self, value: int) -> None:
        value = (self.hue, self.saturation, value)
        self.update(ColorTuple(value, mode="hsl"))


# > FUNCTIONS <
def verify_tuple_types(t: Tuple, mode: Literal["rgb", "hsl"]) -> None:
    if not all(isinstance(v, int) or isinstance(v, float) for v in t):
        raise TypeError("Value must be a 3-tuple of all integers or floats.")


def parse_hex(hex_string: str) -> Tuple[int, int, int]:
    """
    Parse a hex color string into a tuple of three integers.
    """
    hex_string = hex_string.strip("#")
    match = HEX_PATTERN.match(hex_string)
    if match is None:
        raise ValueError(
            " ".join(
                [
                    f"Invalid hex color: '{hex_string}'.",
                    "Must be in the format '(#)RRGGBB'.",
                ]
            )
        )
    red, green, blue = [int(c, 16) for c in match.groups()]
    return (red, green, blue)
