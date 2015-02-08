#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import unittest
import math

import file_utils as utils


MODULE_DIRECTORY = os.path.dirname(__file__)
DENSITIES_CONFIG_FILE = os.path.join(MODULE_DIRECTORY, 'densities.json')
FILENAME_KEY = '{FILENAME}'
DENSITY_KEY = '{DENSITY}'


class DensityOutputConfig:
    def __init__(self, name, scale, sub_dir=None, file_name_pattern=None):
        self.name = name
        self.scale = scale
        self.output_sub_dir = os.path.normpath(sub_dir)
        self.file_name_pattern = file_name_pattern
        if self.file_name_pattern and FILENAME_KEY not in self.file_name_pattern:
            utils.print_warning('Template key +"' + FILENAME_KEY + '" not found in density "' + name + '"')

    def get_output_dir(self, base_output_dir):
        if self.output_sub_dir:
            return os.path.join(base_output_dir, self.output_sub_dir)
        return base_output_dir

    def get_filename(self, filename):
        if self.file_name_pattern:
            file_root, file_ext = os.path.splitext(filename)
            renamed_file = self.file_name_pattern.replace(FILENAME_KEY, file_root).replace(DENSITY_KEY, self.name)
            return renamed_file + file_ext
        return filename


class DensitySize:
    def __init__(self, density_output, width=None, height=None):
        self.output_config = density_output
        self.width = width
        self.height = height

    def __repr__(self):
        return "[DensitySize]\t" + str(self.width) + '\t' + str(self.height) + '\t' + str(self.output_config.name)


class DensityConverter:
    densities = []
    with open(DENSITIES_CONFIG_FILE) as densities_config_file:
        root_json = json.load(densities_config_file)
        densities_json = root_json.get('densities')
        for density in densities_json:
            densities.append(DensityOutputConfig(density.get('name'), density.get('scale'), density.get('sub_dir'),
                                                 density.get('file_name_pattern')))

    @staticmethod
    def get_density_names():
        return [density.name for density in DensityConverter.densities]

    @staticmethod
    def convert(source_value, source_dpi, target_dpi):
        if source_value is None:
            return None
        return int(math.ceil(source_value * target_dpi / float(source_dpi)))

    @staticmethod
    def get_density(density_name):
        for density in DensityConverter.densities:
            if density.name == density_name:
                return density
        raise Exception('No density found named "' + density_name + '"')

    @staticmethod
    def get_density_sizes(width, height, density_name):
        """
        Returns a list of DensitySize objects with converted width and height for each density.
        :param width: int
        :param height: int
        :param density_name: str
        :return: DensitySize
        """
        input_density = DensityConverter.get_density(density_name)
        density_sizes = []
        for output_density in DensityConverter.densities:
            converted_width = DensityConverter.convert(width, input_density.scale, output_density.scale)
            converted_height = DensityConverter.convert(height, input_density.scale, output_density.scale)
            density_size = DensitySize(output_density, converted_width, converted_height)
            density_sizes.append(density_size)
        return density_sizes


class TestDensityConverter(unittest.TestCase):
    def test_get_density_sizes(self):
        density_sizes = DensityConverter.get_density_sizes(64, 96, 'xhdpi')
        self.assertEquals(len(density_sizes), 5)
        self._check_density_size(density_sizes[0], 128, 192)
        self._check_density_size(density_sizes[1], 96, 144)
        self._check_density_size(density_sizes[2], 64, 96)
        self._check_density_size(density_sizes[3], 48, 72)
        self._check_density_size(density_sizes[4], 32, 48)

    def _check_density_size(self, density_size, width, height):
        self.assertEquals(density_size.width, width)
        self.assertEquals(density_size.height, height)

    def test_get_density_names(self):
        self.assertEqual(DensityConverter.get_density_names(), ['xxxhdpi', 'xxhdpi', 'xhdpi', 'hdpi', 'mdpi'])


if __name__ == '__main__':
    unittest.main(exit=False)
