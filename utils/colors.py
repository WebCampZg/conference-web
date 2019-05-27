"""
Util functions for handling colors.
"""
import re

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def relative_luminance(color):
    """
    https://www.w3.org/TR/WCAG/#dfn-relative-luminance
    """
    RsRGB = color[0] / 255
    GsRGB = color[1] / 255
    BsRGB = color[2] / 255

    R = RsRGB / 12.92 if RsRGB <= 0.03928 else ((RsRGB + 0.055) / 1.055) ** 2.4
    G = GsRGB / 12.92 if GsRGB <= 0.03928 else ((GsRGB + 0.055) / 1.055) ** 2.4
    B = BsRGB / 12.92 if BsRGB <= 0.03928 else ((BsRGB + 0.055) / 1.055) ** 2.4

    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(color1, color2):
    """
    https://www.w3.org/TR/WCAG/#dfn-contrast-ratio
    """
    l2, l1 = sorted([
        relative_luminance(color1),
        relative_luminance(color2)
    ])

    return (l1 + 0.05) / (l2 + 0.05)


def get_text_color(bg_color):
    """
    Returns the color to use for text given a background color.
    """
    contrast_black = contrast_ratio(bg_color, BLACK)
    contrast_white = contrast_ratio(bg_color, WHITE)

    return BLACK if contrast_black > contrast_white else WHITE


def valid_hex_color_code(string):
    return re.match("^#[0-9A-F]{6}$", string, re.IGNORECASE)


def color_from_hex(hex_color):
    """
    Converts a color hex string into a (R, G, B) tuple.
    """
    if not valid_hex_color_code(hex_color):
        raise ValueError("Not a valid hex color: {}".format(hex_color))

    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    return (r, g, b)


def color_to_hex(color):
    """
    Converts a (R, G, B) tuple into a hex color string.
    """
    return "#" + "".join('{:02X}'.format(x) for x in color)
