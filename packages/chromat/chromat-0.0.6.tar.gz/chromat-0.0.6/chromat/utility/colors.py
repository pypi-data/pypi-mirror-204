"""
'CHROMAT.utility.colors'
copyright (c) 2023 hex benjamin
full license available at /COPYING
"""
import re

from typing import Tuple


# > CONSTANTS <
HEX_PATTERN = re.compile(r"^([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$")


# > FUNCTIONS <
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


def get_contrast(
    lum1: float,
    lum2: float,
    min_ratio: float = 4.5,
) -> float:
    """
    Calculate the contrast ratio between two swatches.

    Parameters
    ----------
    swatch1 : Swatch
        First swatch to compare.
    swatch2 : Swatch
        Second swatch to compare.
    min_ratio : float, optional
        Ratio to use for determining contrast.
        default 4.5

    Returns
    -------
    float
        Contrast ratio between the two swatches, 1.0-21.0.
    """
    lums = [lum1, lum2]
    return (max(lums) + 0.05) / (min(lums) + 0.05)
