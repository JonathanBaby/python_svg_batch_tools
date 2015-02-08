#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from xml.dom.minidom import parse


def split_xml_attribute_properties(value):
    return value.rstrip(';').split(';')


def set_attribute_inner_property(xml_element, attribute_name, property_name, property_value):
    """ Sets or updates an XML attribute inner property.

Typically for attribute with multiple properties like:
'<element attribute="property_a:value_a;property_b:value_b"/>'
"""
    updated_property_string = property_name + ':' + property_value
    if xml_element.attributes.get(attribute_name) is None:
        xml_element.setAttribute(attribute_name, updated_property_string)
    else:
        attribute_value = xml_element.attributes[attribute_name].value
        updated_value = ''
        found_property = False
        for property_string in split_xml_attribute_properties(attribute_value):
            p_name, p_value = property_string.split(':')
            if p_name == property_name:
                updated_value = attribute_value.replace(p_name + ':' + p_value, updated_property_string)
                found_property = True
                break
        if not found_property:
            updated_value = attribute_value.rstrip(';') + ';' + updated_property_string
        xml_element.setAttribute(attribute_name, updated_value)


class SvgStyleProperty:
    """ Style property of a SVG element.

A property could either be an attribute of the SVG element, or an inner value of its "style" attribute.
The property will match both forms. When applying the property to an element, it will either keep its form and update it
if already defined or add new properties to its "style" attribute.
Form A: '<element property="value"/>'
Form B: '<element style="property:value"/>'
"""
    # TODO: provide an option to choose between :
    # - forcing inline 'style' attribute
    # - keep original format (either independent attributes or inline style)
    # - <style> tag embedding CSS
    # - external CSS file
    # TODO: add tests for SvgStyleProperty class

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name + ':' + self.value

    def match_element(self, svg_element):
        """ Checks if the rule matches the given element style properties.
        Property set to 'none' will match elements where it is not found. """
        property_attribute = svg_element.attributes.get(self.name)
        if property_attribute is not None:
            return property_attribute.value.lower() == self.value.lower()
        found_property = False
        style_attribute = svg_element.attributes.get('style')
        if style_attribute is not None:
            found_property, matched = self._match_attribute_value(style_attribute.value)
            if matched:
                return True
        if not found_property and self.value == 'none':
            return True
        return False

    def _match_attribute_value(self, value):
        """ Returns a tuple with two booleans: (found, matched) """
        for property_string in split_xml_attribute_properties(value):
            property_name, property_value = property_string.split(':')
            if property_name == self.name:
                return True, property_value.lower() == self.value.lower()
        return False, False

    def apply_to_element(self, svg_element):
        property_attribute = svg_element.attributes.get(self.name)
        if property_attribute is not None:
            svg_element.setAttribute(self.name, self.value)
        else:
            set_attribute_inner_property(svg_element, 'style', self.name, self.value)


class SvgStyleRule:
    """ Rule class to match an XML element with its "style" attribute properties.
"""
    STYLABLE_SVG_ELEMENTS = ['circle', 'ellipse', 'line', 'polyline', 'polygon', 'path']

    def __init__(self, properties_to_set=None, properties_to_match=None, name=None):
        self.properties_to_set = properties_to_set
        self.properties_to_match = properties_to_match
        self.name = name

    def __repr__(self):
        return '"' + str(self.name) + '" with properties to match: ' + str(self.properties_to_match)

    def load_from_json(self, rule_json):
        set_string = rule_json.get('set')
        if set_string is not None:
            self.properties_to_set = SvgStyleRule.parse_style_properties(set_string)
        else:
            raise Exception('Invalid JSON file. Rule should have at least a "set" property.')
        match_string = rule_json.get('match')
        if match_string is not None:
            self.properties_to_match = SvgStyleRule.parse_style_properties(match_string)
        name_string = rule_json.get('name')
        if name_string is not None:
            self.name = name_string

    @staticmethod
    def parse_style_properties(value):
        style_properties = []
        for property_string in split_xml_attribute_properties(value):
            name, value = property_string.split(':')
            style_properties.append(SvgStyleProperty(name, value))
        return style_properties

    def match_element(self, svg_element):
        if self.properties_to_match:
            for property_to_match in self.properties_to_match:
                if not property_to_match.match_element(svg_element):
                    return False
        return True

    def apply_to_element(self, svg_element):
        for property_to_set in self.properties_to_set:
            property_to_set.apply_to_element(svg_element)

    def apply_to_document(self, svg_dom):
        applied = False
        for primitiveTag in SvgStyleRule.STYLABLE_SVG_ELEMENTS:
            svg_elements = svg_dom.getElementsByTagName(primitiveTag)
            for svgElement in svg_elements:
                if self.match_element(svgElement):
                    self.apply_to_element(svgElement)
                    applied = True
        return applied


class SvgStyleRulesManager:
    """ Manager of a list of SVG style rules, loaded from a JSON file.

Style rules JSON format:
[
{
    "match":"property_a:value_a",
    "set":"property_b:value_b; property_c:value_c",
    "name":"Comment for Rule 1"
},
{
    "match":"fill:#00ffff",
    "set":"fill:#ff00ff;stroke:#00ff00;stroke-opacity:1;stroke-width:25;",
    "name":"Comment for Rule 2"
}
]
"""

    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def load_rules_from_json(self, rules_json_file_path):
        with open(rules_json_file_path) as json_file:
            rules_json = json.load(json_file)
        for rule_json in rules_json:
            rule = SvgStyleRule()
            rule.load_from_json(rule_json)
            self.rules.append(rule)

    def apply_rules_to_svg_file(self, svg_input_file, svg_output_file):
        svg_dom = parse(svg_input_file)
        for rule in self.rules:
            applied = rule.apply_to_document(svg_dom)
            if applied:
                print ' applied ' + str(rule)
        with open(svg_output_file, 'w') as output_file:
            output_file.write(svg_dom.toprettyxml().encode('utf-8'))
