from typing import Literal, Tuple, Union


# > CONSTANTS <
SCALES = {
    "r": 255,
    "g": 255,
    "b": 255,
    "h": 360,
    "s": 100,
    "v": 100,
    "rgb": (255, 255, 255),
    "hsv": (360, 100, 100),
}


# > CLASSES <
class SwatchProp:
    """
    Property class for Swatch's R/G/B/H/S/V values.
    """

    def __init__(
        self,
        value: Union[int, float],
        mode: Literal["r", "g", "b", "h", "s", "v"],
    ) -> None:
        """
        Initialize a SwatchProp object from an int or float.

        Parameters
        ----------
        value : Union[int, float]
            Input value. Will auto-convert to the unselected mode.
        mode : Literal["r", "g", "b", "h", "s", "v"]
            Mode to use for the property. This selection determines the
            scaling for int/float conversion.
        """
        self._value = value
        self._scale = SCALES[mode]

    @property
    def integer(self) -> int:
        if isinstance(self._value, float):
            return int(self._value * self._scale)
        return self._value

    @property
    def float(self) -> float:
        if isinstance(self._value, int):
            return self._value / self._scale
        return self._value

    @property
    def i(self):
        return self.integer

    @property
    def f(self):
        return self.float


class SwatchTupleProp:
    """
    Property class for Swatch's RGB/HSV tuples.
    """

    def __init__(
        self,
        value: Union[Tuple[int, int, int], Tuple[float, float, float]],
        mode: Literal["rgb", "hsv"],
    ) -> None:
        """
        Initialize a SwatchProp object from a tuple of ints or floats.

        Parameters
        ----------
        value : Union[Tuple[int, int, int], Tuple[float, float, float]]
            Input values. Will auto-convert to the unselected mode.
        mode : Literal["rgb", "hsv"]
            Mode to use for the property. This selection determines the
            scaling for int/float conversion.
        """
        self._values = value
        self._scales = SCALES[mode]

    def __repr__(self):
        return f"SwatchTupleProp({self.i}, {self.f})"

    @property
    def integer(self) -> Tuple[int, int, int]:
        if all(isinstance(v, float) for v in self._values):
            return tuple(
                [
                    int(c * s)
                    for c, s in zip(
                        self._values,
                        self._scales,
                    )
                ]
            )
        else:
            return tuple([c for c in self._values])

    @property
    def float(self) -> Tuple[float, float, float]:
        if all(isinstance(v, int) for v in self._values):
            return tuple(
                [
                    c / s
                    for c, s in zip(
                        self._values,
                        self._scales,
                    )
                ]
            )
        return tuple(self._values)

    @property
    def i(self):
        return self.integer

    @property
    def f(self):
        return self.float
