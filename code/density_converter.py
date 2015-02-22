#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import unittest
import math


class DensityOutputConfig:
    FILENAME_KEY = '{FILENAME}'
    DENSITY_KEY = '{DENSITY}'

    def __init__(self, name, scale, output_sub_dir=None, file_name_pattern=None):
        self.name = name
        self.scale = scale
        self.output_sub_dir = output_sub_dir
        self.file_name_pattern = file_name_pattern

    @classmethod
    def from_json(cls, density_json):
        name = density_json.get('name')
        if not name:
            raise ConfigFileFormatError('Missing required "name" parameter.\nJSON ' + json.dumps(density_json))
        scale = density_json.get('scale')
        if not scale:
            raise ConfigFileFormatError('Missing required "scale" parameter.\nJSON ' + json.dumps(density_json))
        output_sub_dir = density_json.get('sub_dir')
        file_name_pattern = density_json.get('file_name_pattern')
        if file_name_pattern and DensityOutputConfig.FILENAME_KEY not in file_name_pattern:
            raise ConfigFileFormatError('Missing required "' + DensityOutputConfig.FILENAME_KEY
                                        + '" template in "file_name_pattern" property. Fix or remove property.'
                                        + '\nJSON: ' + json.dumps(density_json))
        return cls(name, scale, output_sub_dir, file_name_pattern)

    def get_output_dir(self, base_output_dir):
        if self.output_sub_dir:
            return os.path.join(base_output_dir, self.output_sub_dir)
        return base_output_dir

    def get_filename(self, filename):
        if self.file_name_pattern:
            file_root, file_ext = os.path.splitext(filename)
            renamed_file = self.file_name_pattern.replace(DensityOutputConfig.FILENAME_KEY, file_root).replace(
                DensityOutputConfig.DENSITY_KEY, self.name)
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
    def __init__(self, json_config_file):
        self.densities = []
        with open(json_config_file) as densities_config_file:
            root_json = json.load(densities_config_file)
            densities_json = root_json.get('densities')
            for density_json in densities_json:
                self.densities.append(DensityOutputConfig.from_json(density_json))

    def get_density_names(self):
        return [density.name for density in self.densities]

    @staticmethod
    def convert(source_value, source_dpi, target_dpi):
        if source_value is None:
            return None
        return int(math.ceil(source_value * target_dpi / float(source_dpi)))

    def get_density(self, density_name):
        for density in self.densities:
            if density.name == density_name:
                return density
        raise UnknownDensityError(density_name, self.get_density_names())

    def get_density_sizes(self, width, height, density_name):
        """
        Returns a list of DensitySize objects with converted width and height for each density.
        :param width: int
        :param height: int
        :param density_name: str
        :return: DensitySize
        """
        input_density = self.get_density(density_name)
        density_sizes = []
        for output_density in self.densities:
            converted_width = DensityConverter.convert(width, input_density.scale, output_density.scale)
            converted_height = DensityConverter.convert(height, input_density.scale, output_density.scale)
            density_size = DensitySize(output_density, converted_width, converted_height)
            density_sizes.append(density_size)
        return density_sizes


class UnknownDensityError(Exception):
    """Error class for unknown density provided to DensityConverter."""

    def __init__(self, density_name, densities):
        message = 'Unknown density "' + density_name + '". Should be in ' + str(densities)
        super(UnknownDensityError, self).__init__(message)


class ConfigFileFormatError(Exception):
    """Error class for densities JSON config file parsing."""

    def __init__(self, message):
        super(ConfigFileFormatError, self).__init__(message)


class DensityConverterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_converter = DensityConverter('../tests/densities_test.json')

    def test_computes_all_density_sizes_from_a_specific_one(self):
        density_sizes = self.test_converter.get_density_sizes(10, 20, 'titi')
        self.assertEquals(len(density_sizes), 4)
        self._check_density_size(density_sizes[0], 05, 10)
        self._check_density_size(density_sizes[1], 10, 20)
        self._check_density_size(density_sizes[2], 15, 30)
        self._check_density_size(density_sizes[3], 20, 40)

    def _check_density_size(self, density_size, width, height):
        self.assertEquals(density_size.width, width)
        self.assertEquals(density_size.height, height)

    def test_returns_all_density_names_listed_in_config_file(self):
        self.assertEqual(self.test_converter.get_density_names(), ['toto', 'titi', 'tata', 'tutu'])

    def test_raises_UnknownDensityError_if_density_name_not_in_config_file(self):
        with self.assertRaises(UnknownDensityError):
            self.test_converter.get_density_sizes(10, 20, 'fake_test_density')


class DensityOutputConfigTestCase(unittest.TestCase):
    def test_raises_ConfigFileFormatError_if_required_parameter_missing(self):
        density_json = json.loads('{"name": "toto"}')
        with self.assertRaises(ConfigFileFormatError):
            DensityOutputConfig.from_json(density_json)

    def test_raises_ConfigFileFormatError_if_no_FILENAME_key_in_provided_pattern(self):
        density_json = json.loads('{"name": "toto"}')
        with self.assertRaises(ConfigFileFormatError):
            DensityOutputConfig.from_json(density_json)

    def test_parses_json_with_minimal_required_parameters_only(self):
        density_json = json.loads('{"name": "toto", "scale": 4}')
        config = DensityOutputConfig.from_json(density_json)
        self.assertEqual('toto', config.name)
        self.assertEqual(4, config.scale)

    def test_formats_filename_from_pattern_with_template_keys(self):
        density_json = json.loads('{"name": "toto", "scale": 4, "file_name_pattern": "ti_{FILENAME}_{DENSITY}_ti"}')
        config = DensityOutputConfig.from_json(density_json)
        self.assertEqual('ti_tutu_toto_ti.png', config.get_filename('tutu.png'))

    def test_keeps_original_filename_if_no_pattern_provided(self):
        density_json = json.loads('{"name": "toto", "scale": 4}')
        config = DensityOutputConfig.from_json(density_json)
        self.assertEqual('tutu.png', config.get_filename('tutu.png'))


if __name__ == '__main__':
    unittest.main(exit=False)
