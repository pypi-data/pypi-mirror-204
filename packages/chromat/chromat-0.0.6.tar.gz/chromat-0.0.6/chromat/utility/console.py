"""
'CHROMAT.utility.console'
copyright (c) 2023 hex benjamin
full license available at /COPYING
"""
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install as rich_traceback_install

chromat_theme = Theme(
    {"body": "#B9B8BA", "heading": "#EEEEEE"},
    inherit=False,
)

CONSOLE = Console(theme=chromat_theme, tab_size=4)

rich_traceback_install()


class SwatchText(Text):
    def __init__(self, swatch_hex: str, swatch_name: str = "Swatch"):
        super().__init__(swatch_name, style=f"bold {swatch_hex}")
