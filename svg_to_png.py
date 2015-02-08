#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import sys
import os
import datetime
import argparse
import subprocess

import code.file_utils as utils
from code.density_converter import DensityConverter


def exec_command(command_args, log_filename):
    with open(log_filename, 'a+') as log_file:
        log_file.seek(0, os.SEEK_END)
        print(' '.join(command_args))
        return subprocess.call(command_args, stdout=log_file, stderr=subprocess.STDOUT)


def check_command_path(paths_to_check, args=None):
    for path in paths_to_check:
        print('Looking for ' + path + ' ... ', end='')
        command_args = [path]
        if args:
            command_args.extend(args)
        try:
            output = subprocess.check_output(command_args, stderr=subprocess.STDOUT)
            print('yes')
        except (subprocess.CalledProcessError, OSError):
            print('no')
            continue
        return path, output
    return None, None


class SvgToPngRenderer:
    def __init__(self):
        self.command_path = None
        self.about = None
        self.initialized = False
        self.available = False

    def initialize(self):
        pass

    def is_available(self):
        if not self.initialized:
            self.initialize()
        return self.available

    def render(self, svg_file, png_file, width=None, height=None):
        pass

    def __repr__(self):
        return '[SvgToPngRenderer]\nPath: ' + self.command_path + '\n' + self.about


class SvgToPngImageMagickRenderer(SvgToPngRenderer):
    """ Render (rasterize) SVG files to PNG, using ImageMagick command line.

    Constructor looks for ImageMagick 'convert' command line tool - build should have SVG support.
    To install ImageMagick on MacOS:
    1. Install "Homebrew" (alias "brew" - http://brew.sh ):
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    2. Install ImageMagick:
        brew install imagemagick --with-librsvg
    Or with Mac Ports:
        sudo port install ImageMagick +rsvg
    """

    def initialize(self):
        if not self.initialized:
            paths_to_check = ['convert']
            (self.command_path, self.about) = check_command_path(paths_to_check, args=['-version'])
            if self.command_path:
                self.available = True
                if sys.platform == 'darwin' and 'rsvg' not in self.about:
                    utils.print_warning('Installed version of ImageMagick is missing RSVG module for proper rendering.\
                        \nTo properly re-install ImageMagick:\
                        \n\tbrew remove imagemagick\
                        \n\tbrew install imagemagick --with-librsvg\n')
            else:
                if sys.platform == 'darwin':
                    utils.print_warning('ImageMagick can be installed with "Homebrew", open source package manager for OS X.\
                        \nTo install Homebrew:\
                        \n\t/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"\
                        \nTo install ImageMagick:\
                        \n\tbrew install imagemagick --with-librsvg\n')
            self.initialized = True

    def render(self, svg_file, png_file, width=None, height=None):
        """ Render (rasterize) SVG files to PNG, using ImageMagick command line.

        By default, ImageMagick rasters vector images to their given canvas resolution using default density (72 dpi).
        To scale and raster image with proper sampling, we need to compute the raster density.
        Formula: raster_density = raster_width / original_width * original_density
        See: http://www.imagemagick.org/script/command-line-options.php#density

        Using a fixed high density value would be a performance issue with originally large images.
        Not specifying density would lower image quality when up-scaling.
        Because of float number approximations, we can't rely on density to raster image to the exact desired size. So, to
        ensure pixel perfect output, we 1) use a 'density factor' to increase sampling quality, 2) resize the raster image
        to the expected resolution.

        To get the image original size and density, we use ImageMagick 'percent escapes' attributes with 'info:' output.
        See: http://www.imagemagick.org/script/escape.php

        Interesting thread about selecting ImageMagick SVG renderer:
        http://www.imagemagick.org/discourse-server/viewtopic.php?f=1&t=26837
        """
        density_factor = 2
        log_filename = 'imagemagick.log'
        if width or height:
            info_percent_escapes = '%w %h %[resolution.x] %[resolution.y]'
            info_command_args = [self.command_path, svg_file, '-format', info_percent_escapes, 'info:']
            try:
                info = subprocess.check_output(info_command_args)
            except subprocess.CalledProcessError, err:
                utils.print_warning('Error calling:\n\t' + ' '.join(info_command_args) + '\n' + str(err) + '\n')
                return
            original_width, original_height, original_density_x, original_density_y = info.split()
            density = ''
            geometry = ''
            if width:
                density_x = int(math.ceil(width / float(original_width) * float(original_density_x)) * density_factor)
                density = str(density_x)
                geometry = str(width)
            if height:
                ratio = height / float(original_height)
                if not width:
                    density_x = int(math.ceil(ratio * float(original_density_x)) * density_factor)
                    density = str(density_x)
                density_y = int(math.ceil(ratio * float(original_density_y)) * density_factor)
                density += 'x' + str(density_y)
                geometry += 'x' + str(height)
            command_args = [self.command_path, '-density', density, '-resize', geometry, '-background', 'none',
                            svg_file, png_file]
        else:
            command_args = [self.command_path, '-background', 'none', svg_file, png_file]
        exec_command(command_args, log_filename)


class SvgToPngInkscapeRenderer(SvgToPngRenderer):
    """ Render (rasterize) SVG files to PNG, using Inkscape command line.

    Constructor looks for Inkscape application in default MacOS, Windows and Linux paths.
    """

    def initialize(self):
        if not self.initialized:
            paths_to_check = [
                '/Applications/Inkscape.app/Contents/Resources/bin/inkscape',
                'C:\\Program Files (x86)\\Inkscape',
                'inkscape']
            (self.command_path, self.about) = check_command_path(paths_to_check, args=['--version'])
            if self.command_path:
                self.available = True
            self.initialized = True

    def render(self, svg_file, png_file, width=None, height=None):
        """ Render (rasterize) SVG files to PNG, using ImageMagick command line.

        If no width nor height is provided, Inkscape will export using its default density (90 dpi).
        See: https://inkscape.org/doc/inkscape-man.html
        And: http://tavmjong.free.fr/INKSCAPE/MANUAL/html/CommandLine.html

        Note: Inkscape provides many export options and a complete shell to manipulate SVG. You can, for instance, select a
        specific SVG elements to export with its ID or to use it as a mask to raster the rest of the image.
        """
        log_filename = 'inkscape.log'
        command_args = [self.command_path, '--without-gui', svg_file, '--export-png', png_file]
        if width:
            command_args.extend(['-w', str(width)])
        if height:
            command_args.extend(['-h', str(height)])
        exec_command(command_args, log_filename)


def get_renderer(renderer_name=None):
    selected_renderer = None
    if renderer_name:
        if renderer_name == 'inkscape':
            selected_renderer = SvgToPngInkscapeRenderer()
        elif renderer_name == 'imagemagick':
            selected_renderer = SvgToPngImageMagickRenderer()
        else:
            raise Exception('Unknown renderer ' + renderer_name)
    else:
        for renderer in [SvgToPngImageMagickRenderer(), SvgToPngInkscapeRenderer()]:
            if renderer.is_available():
                selected_renderer = renderer
                break
    if not selected_renderer or not selected_renderer.is_available():
        raise Exception('No available renderer.')
    return selected_renderer


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='Render SVG files to PNG with specified size, using pixels or Android DIP.')
    parser.add_argument('-i', dest='INPUT_FILE_OR_DIR', default='', help='Input SVG files or directory')
    parser.add_argument('-o', dest='OUTPUT_DIR', default='', help='Ouput directory for PNG files')
    parser.add_argument('--width', dest='WIDTH', type=int, help='Output width, in pixels')
    parser.add_argument('--height', dest='HEIGHT', type=int, help='Output height, in pixels')
    parser.add_argument('--renderer', dest='RENDERER', choices=['inkscape', 'imagemagick'],
                        help='Force renderer to use')
    parser.add_argument('--density', dest='DENSITY_LABEL',
                        choices=DensityConverter.get_density_names(),
                        help='Specifies density corresponding to the given size, and generates ALL the other densities\
                        directly from the SVG source (intented to check potential quality increase).')
    return parser.parse_args(argv)


def check_command_line_arguments(args):
    if args.INPUT_FILE_OR_DIR is not None:
        args.INPUT_FILE_OR_DIR = os.path.normpath(args.INPUT_FILE_OR_DIR)
        if not os.path.exists(args.INPUT_FILE_OR_DIR):
            raise Exception('Invalid input file or directory "' + args.INPUT_FILE_OR_DIR + '"')
    args.OUTPUT_DIR = os.path.normpath(args.OUTPUT_DIR)
    if not os.path.exists(args.OUTPUT_DIR):
        os.makedirs(args.OUTPUT_DIR)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)
    check_command_line_arguments(args)
    date_time_start = datetime.datetime.now()

    renderer = get_renderer(args.RENDERER)
    print('\nSelected ' + str(renderer))

    input_svg_files = sorted(utils.get_file_paths(args.INPUT_FILE_OR_DIR, utils.is_svg_file), key=str.lower)
    if args.DENSITY_LABEL is not None:
        density_sizes = DensityConverter.get_density_sizes(args.WIDTH, args.HEIGHT, args.DENSITY_LABEL)
        for density_size in density_sizes:
            print(density_size)
        for density_size in density_sizes:
            print('\nHandling density "' + density_size.output_config.name + '"\n')
            output_dir = density_size.output_config.get_output_dir(args.OUTPUT_DIR)
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)
            for svg_file in input_svg_files:
                png_filename = density_size.output_config.get_filename(
                    os.path.splitext(os.path.basename(svg_file))[0] + '.png')
                png_file = os.path.join(output_dir, png_filename)
                renderer.render(svg_file, png_file, density_size.width, density_size.height)
    else:
        for svg_file in input_svg_files:
            png_file = os.path.join(args.OUTPUT_DIR, os.path.splitext(os.path.basename(svg_file))[0] + '.png')
            renderer.render(svg_file, png_file, args.WIDTH, args.HEIGHT)

    utils.print_reporting(date_time_start, datetime.datetime.now(), input_svg_files)


if __name__ == '__main__':
    sys.exit(main())
