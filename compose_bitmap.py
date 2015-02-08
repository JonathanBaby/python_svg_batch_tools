#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import datetime
import argparse
import subprocess

import code.file_utils as utils


def exec_command(command_args, log_filename):
    with open(log_filename, 'a+') as log_file:
        log_file.seek(0, os.SEEK_END)
        print(' '.join(command_args))
        return subprocess.call(command_args, stdout=log_file, stderr=subprocess.STDOUT)


def overlay(background_file, overlay_file, output_file, width=None, height=None, offset_x=None, offset_y=None):
    log_filename = 'compose_bitmap_imagemagick.log'
    command_args = ['convert', background_file, '(', overlay_file]
    if width or height:
        resize_geometry = str(width) if width else ''
        resize_geometry += ('x' + str(height)) if height else ''
        command_args.extend(['-resize', resize_geometry])
    command_args.extend([')', '-gravity', 'center'])
    if offset_x or offset_y:
        offset_geometry = str(offset_x) if offset_x else '+0'
        offset_geometry += str(offset_y) if offset_y else ''
        command_args.extend(['-geometry', offset_geometry])
    command_args.extend(['-composite', output_file])
    exec_command(command_args, log_filename)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='Overlay a list of bitmaps over a same background.')
    parser.add_argument('--background', dest='BACKGROUND_BITMAP', help='Bitmap to use as background image',
                        required=True)
    parser.add_argument('-i', dest='INPUT_FILE_OR_DIR', help='File or directory with bitmaps to overlay', required=True)
    parser.add_argument('-o', dest='OUTPUT_DIR', help='Output directory for PNG files', required=True)
    parser.add_argument('--width', dest='WIDTH', type=int, help='Width of overlaid bitmap, if resized')
    parser.add_argument('--height', dest='HEIGHT', type=int, help='Height of overlaid bitmap, if resized')
    parser.add_argument('-x', dest='OFFSET_X', type=int, help='Horizontal offset of overlaid bitmaps')
    parser.add_argument('-y', dest='OFFSET_Y', type=int, help='Vertical offset of overlaid bitmaps')
    return parser.parse_args(argv)


def check_command_line_arguments(args):
    args.OUTPUT_DIR = os.path.normpath(args.OUTPUT_DIR)
    if not os.path.exists(args.OUTPUT_DIR):
        os.makedirs(args.OUTPUT_DIR)
    args.INPUT_FILE_OR_DIR = os.path.normpath(args.INPUT_FILE_OR_DIR)
    if not os.path.exists(args.INPUT_FILE_OR_DIR):
        raise Exception('Invalid input file or directory "' + args.INPUT_FILE_OR_DIR + '"')
    args.BACKGROUND_BITMAP = os.path.normpath(args.BACKGROUND_BITMAP)
    if not os.path.exists(args.BACKGROUND_BITMAP):
        raise Exception('Invalid background image "' + args.BACKGROUND_BITMAP + '"')


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)
    check_command_line_arguments(args)
    date_time_start = datetime.datetime.now()
    input_files = sorted(utils.get_file_paths(args.INPUT_FILE_OR_DIR, utils.is_png_file), key=str.lower)
    for input_file in input_files:
        filename, ext = os.path.splitext(os.path.basename(input_file))
        output_path = os.path.join(args.OUTPUT_DIR, filename + '_out' + ext)
        overlay(args.BACKGROUND_BITMAP, input_file, output_path, args.WIDTH, args.HEIGHT, args.OFFSET_X, args.OFFSET_Y)
    utils.print_reporting(date_time_start, datetime.datetime.now(), input_files)


if __name__ == '__main__':
    sys.exit(main())
