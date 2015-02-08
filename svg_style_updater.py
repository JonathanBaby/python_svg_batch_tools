#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import datetime
import argparse

from code.color_string import ColorString
from code.svg_style_rule import SvgStyleRulesManager, SvgStyleRule, SvgStyleProperty
import code.file_utils as utils


def update_svg_files(svg_files, rules_manager, output_dir):
    output_svg_files = []
    for input_svg_file in svg_files:
        print 'processing ' + input_svg_file
        output_svg_file = os.path.join(output_dir, os.path.basename(input_svg_file))
        rules_manager.apply_rules_to_svg_file(input_svg_file, output_svg_file)
        output_svg_files.append(output_svg_file)
    return output_svg_files


def get_svg_style_rules_manager(args):
    rules_manager = SvgStyleRulesManager()
    if args.RULES_FILE is not None:
        rules_manager.load_rules_from_json(args.RULES_FILE)
    elif args.COLOR_TO_APPLY is not None:
        property_to_set = SvgStyleProperty('fill', str(args.COLOR_TO_APPLY))
        rule_name = '[command line rule] apply color ' + str(args.COLOR_TO_APPLY)
        property_to_match = None
        if args.COLOR_TO_MATCH is not None:
            property_to_match = SvgStyleProperty('fill', str(args.COLOR_TO_MATCH))
            rule_name += ' to replace ' + str(args.COLOR_TO_MATCH)
        rule = SvgStyleRule([property_to_set], [property_to_match] if property_to_match else None, rule_name)
        print 'Build rule from command line: ' + str(rule)
        rules_manager.add_rule(rule)
    return rules_manager


def check_command_line_arguments(args):
    if not (args.RULES_FILE or args.COLOR_TO_APPLY):
        raise Exception('No style specified. Specify either a color with --color or a JSON rules file with --rules.')
    if args.RULES_FILE and args.COLOR_TO_APPLY:
        raise Exception('Incompatible arguments. Option --color and --rules are exclusive.')
    if args.INPUT_DIR is not None:
        args.INPUT_DIR = os.path.normpath(args.INPUT_DIR)
        if not os.path.isdir(args.INPUT_DIR):
            raise Exception('Invalid input directory "' + args.INPUT_DIR + '"')
    args.OUTPUT_DIR = os.path.normpath(args.OUTPUT_DIR)
    if not os.path.exists(args.OUTPUT_DIR):
        os.makedirs(args.OUTPUT_DIR)
    print 'INPUT_DIR: ' + args.INPUT_DIR
    print 'OUTPUT_DIR: ' + args.OUTPUT_DIR + '\n'


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Updates SVG files color and other style attributes. \
Color to apply can be specified directly from command line. Detailed style "match/set" rules can be specified with a \
JSON file (kinda CSS-like).')
    parser.add_argument('-i', dest='INPUT_DIR', default='', help='Directory with SVGs to "style"')
    parser.add_argument('-o', dest='OUTPUT_DIR', default='svg_output', help='Directory for updated SVGs')
    parser.add_argument('--color', dest='COLOR_TO_APPLY', type=ColorString, help='Color to apply')
    parser.add_argument('--match', dest='COLOR_TO_MATCH', type=ColorString, default=None, help='Color to match (all if \
none specified)')
    parser.add_argument('--rules', dest='RULES_FILE', help='JSON rules file')
    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)
    check_command_line_arguments(args)
    date_time_start = datetime.datetime.now()
    rules_manager = get_svg_style_rules_manager(args)
    # TODO: use glob to improve flexibility : https://docs.python.org/2/library/glob.html#module-glob
    # and os.path.exist : https://docs.python.org/2/library/os.path.html#os.path.expandvars
    input_svg_files = sorted(utils.get_file_paths(args.INPUT_DIR, utils.is_svg_file))
    output_svg_files = update_svg_files(input_svg_files, rules_manager, args.OUTPUT_DIR)
    utils.print_reporting(date_time_start, datetime.datetime.now(), output_svg_files)


if __name__ == '__main__':
    sys.exit(main())
