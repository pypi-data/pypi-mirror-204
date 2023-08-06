#
# File:    ./tests/unit/test_load.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-07-07 15:36:46 +0200
# Project: vutils-yaml: Working with YAML format
#
# SPDX-License-Identifier: MIT
#
"""
Test :mod:`vutils.yaml.load` module.

:const YAML_STREAM: The auxiliary YAML data stream
:const YAML_STREAM_NAME: The name of the auxiliary YAML data stream

.. |load_yaml| replace:: :func:`~vutils.yaml.load.load_yaml`
"""

from vutils.testing.testcase import TestCase

from vutils.yaml.load import load_yaml
from vutils.yaml.utils import (
    BoolType,
    BytesType,
    DateTimeType,
    DateType,
    DictType,
    FloatType,
    IntType,
    ListType,
    NullType,
    SetType,
    StrType,
    getloc,
)

YAML_STREAM = r"""
---
- null
- yes
- 1
- 3.14
- abc
- !!binary AA==
- []
- !!set
    ? a
    ? b
    ? c
- {}
- 2008-07-07
- 2008-07-07 13:15:22.489 +02:00
- !!omap
    - a: 1
    - b: 2
    - c: 3
- !!pairs
    - a: 1
    - b: 2
    - c: 3
"""
YAML_STREAM_NAME = "<unicode string>"


class LoadYamlTestCase(TestCase):
    """Test case for |load_yaml|."""

    __slots__ = ()

    def check_location(self, obj, name, line, column):
        """
        Check whether the object location matches the expectation.

        :param obj: The object
        :param name: The expected location name
        :param line: The expected location line
        :param column: The expected location column
        """
        loc = getloc(obj)
        self.assertEqual(loc.path, name)
        self.assertEqual(loc.line, line)
        self.assertEqual(loc.column, column)

    def do_test_data_are_annotated(self, obj, klass, line, column=3):
        """
        Check the data annotation.

        :param obj: The data object
        :param klass: The expected type of the data object
        :param line: The expected line of the data location
        :param column: The expected column of the data location
        """
        self.assertIsInstance(obj, klass)
        self.check_location(obj, YAML_STREAM_NAME, line, column)

    def test_loaded_data_are_annotated(self):
        """Test whether loaded data are properly annotated."""
        data = load_yaml(YAML_STREAM)

        self.do_test_data_are_annotated(data[0], NullType, 3)
        self.do_test_data_are_annotated(data[1], BoolType, 4)
        self.do_test_data_are_annotated(data[2], IntType, 5)
        self.do_test_data_are_annotated(data[3], FloatType, 6)
        self.do_test_data_are_annotated(data[4], StrType, 7)
        self.do_test_data_are_annotated(data[5], BytesType, 8)
        self.do_test_data_are_annotated(data[6], ListType, 9)
        self.do_test_data_are_annotated(data[7], SetType, 10)
        self.do_test_data_are_annotated(data[8], DictType, 14)
        self.do_test_data_are_annotated(data[9], DateType, 15)
        self.do_test_data_are_annotated(data[10], DateTimeType, 16)
        self.do_test_data_are_annotated(data[11], ListType, 17)
        self.do_test_data_are_annotated(data[12], ListType, 21)
