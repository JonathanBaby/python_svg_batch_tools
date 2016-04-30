#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import unittest

from ConfigParser import SafeConfigParser


COLOR_NAMES_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'color_names.cfg')


def parse_color_names_config_file():
    color_names_parser = SafeConfigParser()
    color_names_parser.read(COLOR_NAMES_CONFIG_FILE)
    color_names_dict = {}
    for name, value in color_names_parser.items('color_names'):
        color_names_dict[name] = value
    return color_names_dict


COLOR_NAMES_DICT = parse_color_names_config_file()
# TODO: handle two disctinct files, one for CSS standard color names that could be written directly in SVG
# and one for user-defined custom color names, that should be replaced with their HEX or rgb values
# TODO; use a SVG file to allow visualising color and names instead of a config file, and parse it with minidom
# TODO: keep original string for valid colors
# TODO: consider ImageMagick color name handling http://www.imagemagick.org/script/color.php
# TODO: add a method to crop to the 216 "Web Safe Colors"
"""
TODO: handle alpha ?

 def change_color(node, attribute):
        if attribute in node.keys() and (
                self.from_color is None
                or parse_color(node.get(attribute)) == self.from_color):
            node.set(attribute, str(self.to_color))
            opacity_attribute = attribute + "-opacity"
            if self.to_color.alpha is not None and (self.from_color is None
                    or self.from_color.alpha is None
                    or (opacity_attribute in node.keys()
                        and math.round(255 * float(node.get(opacity_attribute)))
                        == self.from_color.alpha)):
                node.set(opacity_attribute, "{0:.6f}".format(self.to_color.alpha / 255))

    for node in execution_context.selected_nodes:
        for subnode in node.iter():
            if self.fill_stroke.fill:
                change_color(subnode, "fill")
            if self.fill_stroke.stroke:
                change_color(subnode, "stroke")
"""


class ColorString:
    """Color class parsing CSS color strings.

- Hexadecimal format with 6 or 3 digits: #FFFFFF, #f0f.
- RGB format with [0-255] values: rgb(255,255,255).
Access RGB integer values through members: color.r, color.g, color.b.
"""
    COLOR_REGEX_HEXADECIMAL_6_DIGITS = re.compile('^#[a-f|A-F|0-9]{6}$')
    COLOR_REGEX_HEXADECIMAL_3_DIGITS = re.compile('^#[a-f|A-F|0-9]{3}$')
    COLOR_REGEX_RGB_INTEGER_CSS = re.compile('^rgb\(\s*[0-9]{1,3}\s*,\s*[0-9]{1,3}\s*,\s*[0-9]{1,3}\s*\)$')

    def __init__(self, color_string):
        self.r = None
        self.g = None
        self.b = None
        if not color_string:
            raise Exception('No or empty color string provided.')
        if color_string in COLOR_NAMES_DICT:
            color_string = COLOR_NAMES_DICT[color_string]
        if color_string.startswith('#'):
            if ColorString.COLOR_REGEX_HEXADECIMAL_6_DIGITS.match(color_string):
                self._parse_hexadecimal_six_digits(color_string)
            elif ColorString.COLOR_REGEX_HEXADECIMAL_3_DIGITS.match(color_string):
                self._parse_hexadecimal_three_digits(color_string)
            else:
                raise ColorStringFormatError(color_string, 'Hexadecimal format requires characters in [0-9] or [a-f].')
        elif ColorString.COLOR_REGEX_RGB_INTEGER_CSS.match(color_string):
            self._parse_rgb_integer_css(color_string)
        else:
            raise ColorStringFormatError(color_string)

    def _parse_hexadecimal_six_digits(self, color_string):
        hex_value = color_string.lstrip('#')
        self.r, self.g, self.b = (int(hex_value[i:i + 2], 16) for i in range(0, 6, 2))

    def _parse_hexadecimal_three_digits(self, color_string):
        hex_value = color_string.lstrip('#')
        self.r, self.g, self.b = (int(hex_value[i:i + 1], 16) * 17 for i in range(0, 3))

    def _parse_rgb_integer_css(self, color_string):
        rgb_values = color_string.lstrip('rgb(').rstrip(')').split(',')
        r, g, b = (int(value.strip()) for value in rgb_values)
        if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
            raise ColorStringFormatError(color_string, 'RGB values should be in range [0, 255].')
        self.r, self.g, self.b = r, g, b

    def __str__(self):
        return '#{:02X}{:02X}{:02X}'.format(self.r, self.g, self.b)


class ColorStringFormatError(Exception):
    """Error class for color string parsing."""

    def __init__(self, color_string, error_message=None):
        message = 'Invalid color string "' + color_string + '". '
        if error_message:
            message += error_message
        else:
            message += 'Accepted formats: "#FF0000", "#f00", "rgb(255, 0, 0)" and CSS color names like "red".'
        super(ColorStringFormatError, self).__init__(message)


class ColorStringTestCase(unittest.TestCase):
    def test_parses_hexadecimal_six_digits(self):
        color = ColorString('#00ff00')
        self.assertEquals((color.r, color.g, color.b), (0, 255, 0))

    def test_parses_hexadecimal_three_digits(self):
        color = ColorString('#0ff')
        self.assertEquals((color.r, color.g, color.b), (0, 255, 255))

    def test_parses_rgb_integer_css(self):
        color = ColorString('rgb(255,255,0)')
        self.assertEquals((color.r, color.g, color.b), (255, 255, 0))

    def test_parses_color_names(self):
        color = ColorString('yellow')
        self.assertEquals((color.r, color.g, color.b), (255, 255, 0))

    def test_raises_ColorStringFormatError_on_non_hexadecimal_value(self):
        with self.assertRaises(ColorStringFormatError):
            ColorString('#gghhii')

    def test_raises_ColorStringFormatError_on_out_of_bounds_RGB_values(self):
        with self.assertRaises(ColorStringFormatError):
            ColorString('rgb(0,255,256)')
        with self.assertRaises(ColorStringFormatError):
            ColorString('rgb(0,255,-1)')

    def test_builds_hexadecimal_from_any_format(self):
        self.assertEquals('#0000FF', str(ColorString('#0000ff')))
        self.assertEquals('#0000FF', str(ColorString('#00f')))
        self.assertEquals('#0000FF', str(ColorString('rgb(0,0,255)')))
        self.assertEquals('#0000FF', str(ColorString('blue')))


if __name__ == '__main__':
    unittest.main(exit=False)
