#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys


def print_warning(*objs):
    print('WARNING:', *objs, file=sys.stderr)


def is_svg_file(filename):
    return os.path.splitext(filename)[1].lower() == '.svg'


def is_png_file(filename):
    return os.path.splitext(filename)[1].lower() == '.png'


def get_file_paths(file_or_directory, filter_function):
    file_paths = []
    if os.path.isdir(file_or_directory):
        file_names = os.listdir(file_or_directory)
        file_paths = [os.path.join(file_or_directory, fileName) for fileName in list(filter(filter_function, file_names))]
    elif os.path.isfile(file_or_directory) and filter_function(file_or_directory):
        file_paths.append(file_or_directory)
    return file_paths


def print_reporting(date_time_start, date_time_end, svg_files):
    plural = '' if len(svg_files) < 2 else 's'
    print('\n' + str(len(svg_files)) + ' file' + plural + ' handled.')
    print('Time: ' + str(date_time_end - date_time_start) + '\n')
