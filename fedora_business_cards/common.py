###
# fedora-business-cards - for rendering Fedora contributor business cards
# Copyright (C) 2011  Red Hat, Inc.
# Primary maintainer: Ian Weller <iweller@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###

"""
Common functions shared across the code.
"""

from decimal import Decimal
from distutils.sysconfig import get_python_lib
import imp  # Python: Level up for slaying the imp.
from xml.dom import minidom

from fedora_business_cards import __version__

GOLDEN_RATIO = Decimal('1.61803399')
UNITS = ['in', 'mm']
CONVERSIONS = {
        ('in', 'mm'): Decimal('25.4'),
}

for units in CONVERSIONS.keys():
    CONVERSIONS[(units[1], units[0])] = 1 / CONVERSIONS[units]


def convert(value, from_unit, to_unit):
    """
    Convert a value from one unit to another unit.
    """
    if from_unit == to_unit:
        return value
    return value * CONVERSIONS[(from_unit, to_unit)]


def create_blank_svg(height, width, bleed, unit):
    # Check that the unit is valid
    if unit not in UNITS:
        raise KeyError(unit)
    # Import blank SVG XML
    card = minidom.parseString('<svg xmlns="http://www.w3.org/2000/svg"'
                               ' version="1.1"></svg>')
    # Add dimensions to SVG
    svg_element = card.documentElement
    svg_element.setAttribute('height', '%s%s' % (height + (2 * bleed), unit))
    svg_element.setAttribute('width', '%s%s' % (width + (2 * bleed), unit))
    # Generator comment
    generator_comment = card.createComment(
        'Generated by fedora-business-cards/%s' % __version__
    )
    svg_element.appendChild(generator_comment)
    # Return DOM
    return card


def find_node(doc_node, tag_name, attribute_name, attribute_value):
    """
    Gets a specific node from a DOM tree with a certain tag name, attribute
    name, and attribute value.
    """
    # thanks, mizmo
    elements = doc_node.getElementsByTagName(tag_name)
    for element in elements:
        if element.hasAttribute(attribute_name):
            if element.getAttribute(attribute_name) == attribute_value:
                return element


def recursive_import(module, system=False):
    if '.' in module:
        split = module.split('.')
        parent = recursive_import('.'.join(split[:-1]))
        return imp.load_module(split[-1],
                               *imp.find_module(split[-1], parent.__path__))
    else:
        if system:
            return system_import(module)
        else:
            return imp.load_module(module, *imp.find_module(module))


def system_import(module):
    try:
        themodule = imp.load_module(module,
                *imp.find_module(module, [get_python_lib()]))
    except ImportError:
        themodule = imp.load_module(module,
                *imp.find_module(module, [get_python_lib(1)]))
    return themodule
