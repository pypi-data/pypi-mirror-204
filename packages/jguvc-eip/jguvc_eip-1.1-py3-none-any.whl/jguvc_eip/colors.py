from typing import Tuple


RGBColor = Tuple[int, int, int]
"""Type for RGB colors, encoded as tuples of three ints in the range 0...255"""

BLACK      : RGBColor = (0, 0, 0)
""" A 3-Tuple of ints representing the color black"""
WHITE      : RGBColor = (255, 255, 255)
""" A 3-Tuple of ints representing the color white"""
RED        : RGBColor = (229, 28, 35)
""" A 3-Tuple of ints representing the color red"""
ORANGE     : RGBColor = (255, 152, 0)
""" A 3-Tuple of ints representing an orange color."""
YELLOW     : RGBColor = (255, 235, 59)
""" A 3-Tuple of ints representing a yellow color."""
GREEN      : RGBColor = (139, 195, 74)
""" A 3-Tuple of ints representing a green color."""
TEAL       : RGBColor = (0, 150, 126)
""" A 3-Tuple of ints representing a teal color."""
SKY        : RGBColor = (104, 137, 255)  # lighter / more shiny blue
""" A 3-Tuple of ints representing a shiny blue color."""
BLUE       : RGBColor = (63, 81, 181)
""" A 3-Tuple of ints representing a darker blue color."""
VIOLET     : RGBColor = (156, 39, 176)
""" A 3-Tuple of ints representing a violet color."""
PINK       : RGBColor = (233, 30, 99)
""" A 3-Tuple of ints representing a pink color."""


# --- helper functions for creating color shades


def shade(col: RGBColor, sh: float) -> RGBColor:
    """
    Creates brighter or darker colors

    :param col: an RGBColor as integer tuple
    :param sh: number between 0.0 and 2.0.
               0...1 creates darker tones (towards black),
               1...2 creates lighter tones (towards white)
               smaller/larger values are clipped
    :return: shaded (lighter/darker) color
    """
    if sh < 0.0:
        sh = 0.0
    elif sh > 2.0:
        sh = 2.0

    if sh <= 1:
        return int(col[0]*sh), int(col[1]*sh), int(col[2]*sh)
    else:
        sh -= 1.0
        return int(col[0] * (1-sh) + 255*sh), int(col[1] * (1-sh) + 255*sh), int(col[2] * (1-sh) + 255*sh)


TupleOf7RGBColors = Tuple[RGBColor, RGBColor, RGBColor, RGBColor, RGBColor, RGBColor, RGBColor]
"""A tuple of seven colors - this is used for the color variations SHADE_OF_X"""


def make_shades(col: RGBColor) -> TupleOf7RGBColors:
    """
    creates ligher and darker shades of colors.
    :param col: base color
    :return: Tuple of seven darker and lighter shades. index 0 is the darkest, index 6 the lightest.
    """
    return shade(col, 0.25), shade(col, 0.5), shade(col, 0.75),\
           col,\
           shade(col, 1.25), shade(col, 1.5), shade(col, 1.75)


SHADES_OF_BLACK      : TupleOf7RGBColors = make_shades(BLACK)
"""seven different shades of black, small index is the darkest, large index is the lightest"""
SHADES_OF_WHITE      : TupleOf7RGBColors = make_shades(WHITE)
"""seven different shades of white, small index is the darkest, large index is the lightest"""
SHADES_OF_RED        : TupleOf7RGBColors = make_shades(RED)
"""seven different shades of red, small index is the darkest, large index is the lightest"""
SHADES_OF_ORANGE     : TupleOf7RGBColors = make_shades(ORANGE)
"""seven different shades of orange, small index is the darkest, large index is the lightest"""
SHADES_OF_YELLOW     : TupleOf7RGBColors = make_shades(YELLOW)
"""seven different shades of yellow, small index is the darkest, large index is the lightest"""
SHADES_OF_GREEN      : TupleOf7RGBColors = make_shades(GREEN)
"""seven different shades of green, small index is the darkest, large index is the lightest"""
SHADES_OF_TEAL       : TupleOf7RGBColors = make_shades(TEAL)
"""seven different shades of teal, small index is the darkest, large index is the lightest"""
SHADES_OF_SKY        : TupleOf7RGBColors = make_shades(SKY)
"""seven different shades of light blue, small index is the darkest, large index is the lightest"""
SHADES_OF_BLUE       : TupleOf7RGBColors = make_shades(BLUE)
"""seven different shades of darker blue, small index is the darkest, large index is the lightest"""
SHADES_OF_VIOLET     : TupleOf7RGBColors = make_shades(VIOLET)
"""seven different shades of violet, small index is the darkest, large index is the lightest"""
SHADES_OF_PINK       : TupleOf7RGBColors = make_shades(PINK)
"""seven different shades of pink, small index is the darkest, large index is the lightest"""

VERY_LIGHT_GRAY      : RGBColor = SHADES_OF_BLACK[6]
VERY_LIGHT_RED       : RGBColor = SHADES_OF_RED[6]
VERY_LIGHT_ORANGE    : RGBColor = SHADES_OF_ORANGE[6]
VERY_LIGHT_YELLOW    : RGBColor = SHADES_OF_YELLOW[6]
VERY_LIGHT_GREEN     : RGBColor = SHADES_OF_GREEN[6]
VERY_LIGHT_TEAL      : RGBColor = SHADES_OF_TEAL[6]
VERY_LIGHT_SKY       : RGBColor = SHADES_OF_SKY[6]
VERY_LIGHT_BLUE      : RGBColor = SHADES_OF_BLUE[6]
VERY_LIGHT_VIOLET    : RGBColor = SHADES_OF_VIOLET[6]
VERY_LIGHT_PINK      : RGBColor = SHADES_OF_PINK[6]

LIGHT_GRAY      : RGBColor = SHADES_OF_BLACK[5]
LIGHT_RED       : RGBColor = SHADES_OF_RED[5]
LIGHT_ORANGE    : RGBColor = SHADES_OF_ORANGE[5]
LIGHT_YELLOW    : RGBColor = SHADES_OF_YELLOW[5]
LIGHT_GREEN     : RGBColor = SHADES_OF_GREEN[5]
LIGHT_TEAL      : RGBColor = SHADES_OF_TEAL[5]
LIGHT_SKY       : RGBColor = SHADES_OF_SKY[5]
LIGHT_BLUE      : RGBColor = SHADES_OF_BLUE[5]
LIGHT_VIOLET    : RGBColor = SHADES_OF_VIOLET[5]
LIGHT_PINK      : RGBColor = SHADES_OF_PINK[5]

SLIGHTLY_LIGHTER_GRAY      : RGBColor = SHADES_OF_BLACK[4]
SLIGHTLY_LIGHTER_RED       : RGBColor = SHADES_OF_RED[4]
SLIGHTLY_LIGHTER_ORANGE    : RGBColor = SHADES_OF_ORANGE[4]
SLIGHTLY_LIGHTER_YELLOW    : RGBColor = SHADES_OF_YELLOW[4]
SLIGHTLY_LIGHTER_GREEN     : RGBColor = SHADES_OF_GREEN[4]
SLIGHTLY_LIGHTER_TEAL      : RGBColor = SHADES_OF_TEAL[4]
SLIGHTLY_LIGHTER_SKY       : RGBColor = SHADES_OF_SKY[4]
SLIGHTLY_LIGHTER_BLUE      : RGBColor = SHADES_OF_BLUE[4]
SLIGHTLY_LIGHTER_VIOLET    : RGBColor = SHADES_OF_VIOLET[4]
SLIGHTLY_LIGHTER_PINK      : RGBColor = SHADES_OF_PINK[4]

VERY_DARK_GRAY      : RGBColor = SHADES_OF_BLACK[0]
VERY_DARK_RED       : RGBColor = SHADES_OF_RED[0]
VERY_DARK_ORANGE    : RGBColor = SHADES_OF_ORANGE[0]
VERY_DARK_YELLOW    : RGBColor = SHADES_OF_YELLOW[0]
VERY_DARK_GREEN     : RGBColor = SHADES_OF_GREEN[0]
VERY_DARK_TEAL      : RGBColor = SHADES_OF_TEAL[0]
VERY_DARK_SKY       : RGBColor = SHADES_OF_SKY[0]
VERY_DARK_BLUE      : RGBColor = SHADES_OF_BLUE[0]
VERY_DARK_VIOLET    : RGBColor = SHADES_OF_VIOLET[0]
VERY_DARK_PINK      : RGBColor = SHADES_OF_PINK[0]

DARK_GRAY      : RGBColor = SHADES_OF_BLACK[1]
DARK_RED       : RGBColor = SHADES_OF_RED[1]
DARK_ORANGE    : RGBColor = SHADES_OF_ORANGE[1]
DARK_YELLOW    : RGBColor = SHADES_OF_YELLOW[1]
DARK_GREEN     : RGBColor = SHADES_OF_GREEN[1]
DARK_TEAL      : RGBColor = SHADES_OF_TEAL[1]
DARK_SKY       : RGBColor = SHADES_OF_SKY[1]
DARK_BLUE      : RGBColor = SHADES_OF_BLUE[1]
DARK_VIOLET    : RGBColor = SHADES_OF_VIOLET[1]
DARK_PINK      : RGBColor = SHADES_OF_PINK[1]

SLIGHTLY_DARKER_GRAY      : RGBColor = SHADES_OF_BLACK[2]
SLIGHTLY_DARKER_RED       : RGBColor = SHADES_OF_RED[2]
SLIGHTLY_DARKER_ORANGE    : RGBColor = SHADES_OF_ORANGE[2]
SLIGHTLY_DARKER_YELLOW    : RGBColor = SHADES_OF_YELLOW[2]
SLIGHTLY_DARKER_GREEN     : RGBColor = SHADES_OF_GREEN[2]
SLIGHTLY_DARKER_TEAL      : RGBColor = SHADES_OF_TEAL[2]
SLIGHTLY_DARKER_SKY       : RGBColor = SHADES_OF_SKY[2]
SLIGHTLY_DARKER_BLUE      : RGBColor = SHADES_OF_BLUE[2]
SLIGHTLY_DARKER_VIOLET    : RGBColor = SHADES_OF_VIOLET[2]
SLIGHTLY_DARKER_PINK      : RGBColor = SHADES_OF_PINK[2]


__all__ = ['RGBColor', 'BLACK', 'WHITE', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'TEAL', 'SKY', 'BLUE', 'VIOLET', 'PINK',
           'TupleOf7RGBColors', 'SHADES_OF_BLACK', 'SHADES_OF_WHITE', 'SHADES_OF_RED', 'SHADES_OF_ORANGE',
           'SHADES_OF_YELLOW', 'SHADES_OF_GREEN', 'SHADES_OF_TEAL', 'SHADES_OF_SKY', 'SHADES_OF_BLUE',
           'SHADES_OF_VIOLET', 'SHADES_OF_PINK', 'VERY_LIGHT_GRAY', 'VERY_LIGHT_RED', 'VERY_LIGHT_ORANGE',
           'VERY_LIGHT_YELLOW', 'VERY_LIGHT_GREEN', 'VERY_LIGHT_TEAL', 'VERY_LIGHT_SKY', 'VERY_LIGHT_BLUE',
           'VERY_LIGHT_VIOLET', 'VERY_LIGHT_PINK', 'LIGHT_GRAY', 'LIGHT_RED', 'LIGHT_ORANGE', 'LIGHT_YELLOW',
           'LIGHT_GREEN', 'LIGHT_TEAL', 'LIGHT_SKY', 'LIGHT_BLUE', 'LIGHT_VIOLET', 'LIGHT_PINK',
           'SLIGHTLY_LIGHTER_GRAY', 'SLIGHTLY_LIGHTER_RED', 'SLIGHTLY_LIGHTER_ORANGE', 'SLIGHTLY_LIGHTER_YELLOW',
           'SLIGHTLY_LIGHTER_GREEN', 'SLIGHTLY_LIGHTER_TEAL', 'SLIGHTLY_LIGHTER_SKY', 'SLIGHTLY_LIGHTER_BLUE',
           'SLIGHTLY_LIGHTER_VIOLET', 'SLIGHTLY_LIGHTER_PINK', 'VERY_DARK_GRAY', 'VERY_DARK_RED', 'VERY_DARK_ORANGE',
           'VERY_DARK_YELLOW', 'VERY_DARK_GREEN', 'VERY_DARK_TEAL', 'VERY_DARK_SKY', 'VERY_DARK_BLUE',
           'VERY_DARK_VIOLET', 'VERY_DARK_PINK', 'DARK_GRAY', 'DARK_RED', 'DARK_ORANGE', 'DARK_YELLOW', 'DARK_GREEN',
           'DARK_TEAL', 'DARK_SKY', 'DARK_BLUE', 'DARK_VIOLET', 'DARK_PINK', 'SLIGHTLY_DARKER_GRAY',
           'SLIGHTLY_DARKER_RED', 'SLIGHTLY_DARKER_ORANGE', 'SLIGHTLY_DARKER_YELLOW', 'SLIGHTLY_DARKER_GREEN',
           'SLIGHTLY_DARKER_TEAL', 'SLIGHTLY_DARKER_SKY', 'SLIGHTLY_DARKER_BLUE', 'SLIGHTLY_DARKER_VIOLET',
           'SLIGHTLY_DARKER_PINK']