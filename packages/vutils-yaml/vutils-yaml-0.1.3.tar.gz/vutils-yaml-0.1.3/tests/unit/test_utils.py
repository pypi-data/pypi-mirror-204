#
# File:    ./tests/unit/test_utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-07-07 15:36:27 +0200
# Project: vutils-yaml: Working with YAML format
#
# SPDX-License-Identifier: MIT
#
"""
Test :mod:`vutils.yaml.utils` module.

.. |Annotation| replace:: :class:`~vutils.yaml.utils.Annotation`
.. |NullType| replace:: :class:`~vutils.yaml.utils.NullType`
.. |NullType.__hash__| replace:: :meth:`NullType.__hash__
       <vutils.yaml.utils.NullType.__hash__>`
.. |NullType.__eq__| replace:: :meth:`NullType.__eq__
       <vutils.yaml.utils.NullType.__eq__>`
.. |BoolType| replace:: :class:`~vutils.yaml.utils.BoolType`
.. |BoolType.__hash__| replace:: :meth:`BoolType.__hash__
       <vutils.yaml.utils.BoolType.__hash__>`
.. |BoolType.__eq__| replace:: :meth:`BoolType.__eq__
       <vutils.yaml.utils.BoolType.__eq__>`
.. |YamlDataType| replace:: :class:`~vutils.yaml.utils.YamlDataType`
.. |IntType| replace:: :class:`~vutils.yaml.utils.IntType`
.. |FloatType| replace:: :class:`~vutils.yaml.utils.FloatType`
.. |StrType| replace:: :class:`~vutils.yaml.utils.StrType`
.. |BytesType| replace:: :class:`~vutils.yaml.utils.BytesType`
.. |ListType| replace:: :class:`~vutils.yaml.utils.ListType`
.. |SetType| replace:: :class:`~vutils.yaml.utils.SetType`
.. |DictType| replace:: :class:`~vutils.yaml.utils.DictType`
.. |DateType| replace:: :class:`~vutils.yaml.utils.DateType`
.. |DateTimeType| replace:: :class:`~vutils.yaml.utils.DateTimeType`
.. |obj2xobj| replace:: :func:`~vutils.yaml.utils.obj2xobj`
.. |newc| replace:: :func:`~vutils.yaml.utils.newc`
.. |annotate| replace:: :func:`~vutils.yaml.utils.annotate`
.. |getloc| replace:: :func:`~vutils.yaml.utils.getloc`
.. |keyloc| replace:: :func:`~vutils.yaml.utils.keyloc`
.. |is_null| replace:: :func:`~vutils.yaml.utils.is_null`
.. |is_bool| replace:: :func:`~vutils.yaml.utils.is_bool`
"""

import datetime

import yaml
from vutils.testing.mock import make_mock
from vutils.testing.testcase import TestCase
from vutils.testing.utils import make_type
from vutils.validator.value import Location

from vutils.yaml.load import load_yaml
from vutils.yaml.utils import (
    Annotation,
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
    annotate,
    getloc,
    is_bool,
    is_null,
    keyloc,
    newc,
    obj2xobj,
)

from .utils import SLOT, VALUE


class AnnotationTestCase(TestCase):
    """Test case for |Annotation|."""

    __slots__ = ()

    def test_annotation_initialization(self):
        """Test |Annotation| initialization."""
        location = Location("./foo.yml", 1, 2)

        self.assertEqual(f"{Annotation().location}", "")
        self.assertIs(Annotation(location).location, location)


class NullTypeTestCase(TestCase):
    """Test case for |NullType|."""

    __slots__ = ()

    def test_null_type_behaves_like_false(self):
        """Test whether |NullType| object behaves like :obj:`False`."""
        self.assertFalse(NullType())

    def test_hashing_and_equality(self):
        """Test |NullType.__hash__| and |NullType.__eq__|."""
        self.assertEqual(hash(NullType()), hash(None))

        self.assertEqual(NullType(), None)
        self.assertEqual(NullType(), NullType())
        self.assertNotEqual(NullType(), 0)


class BoolTypeTestCase(TestCase):
    """Test case for |BoolType|."""

    __slots__ = ()

    def test_bool_type_can_hold_value(self):
        """Test whether a |BoolType| object can hold a Boolean value."""
        self.assertTrue(BoolType(True))
        self.assertFalse(BoolType(False))

    def test_hashing_and_equality(self):
        """Test |BoolType.__hash__| and |BoolType.__eq__|."""
        self.assertEqual(hash(BoolType(False)), hash(False))
        self.assertEqual(hash(BoolType(True)), hash(True))

        self.assertEqual(BoolType(False), BoolType(False))
        self.assertEqual(BoolType(False), False)
        self.assertEqual(BoolType(True), BoolType(True))
        self.assertEqual(BoolType(True), True)

        self.assertNotEqual(BoolType(False), BoolType(True))
        self.assertNotEqual(BoolType(False), True)
        self.assertNotEqual(BoolType(True), BoolType(False))
        self.assertNotEqual(BoolType(True), False)

        self.assertEqual(BoolType(False), 0)
        self.assertEqual(BoolType(False), IntType(0))
        self.assertEqual(BoolType(True), 1)
        self.assertEqual(BoolType(True), IntType(1))
        self.assertNotEqual(BoolType(True), 2)

        self.assertEqual(BoolType(False), 0.0)
        self.assertEqual(BoolType(False), FloatType(0.0))
        self.assertEqual(BoolType(True), 1.0)
        self.assertEqual(BoolType(True), FloatType(1.0))
        self.assertNotEqual(BoolType(True), 2.0)

        self.assertNotEqual(BoolType(False), [])
        self.assertNotEqual(BoolType(True), [])


class YamlDataTypeTestCase(TestCase):
    """Test case for |YamlDataType| and its subclasses."""

    __slots__ = ()

    def do_arithmetic_check(self, cls, zero, unit):
        """
        Test arithmetic types.

        :param cls: The arithmetic type
        :param zero: The zero element
        :param unit: The unit element
        """
        self.assertEqual(cls(unit), unit)
        self.assertEqual(cls(unit) + cls(unit), unit + unit)
        self.assertLess(cls(unit), unit + unit)
        self.assertFalse(cls(zero))
        self.assertTrue(cls(unit))

    def do_sequence_check(self, cls, sequence, empty):
        """
        Test sequence types.

        :param cls: The sequence type
        :param sequence: The nonempty sequence
        :param empty: The empty sequence
        """
        self.assertEqual(cls(sequence), sequence)
        self.assertEqual(cls(sequence)[0], sequence[0])
        self.assertTrue(cls(sequence))
        self.assertFalse(cls(empty))

    def do_extensibility_check(self, obj):
        """
        Test whether :arg:`obj` is extensible.

        :param obj: The YAML data object
        """
        self.assertFalse(hasattr(obj, SLOT))
        setattr(obj, SLOT, VALUE)
        self.assertTrue(hasattr(obj, SLOT))
        self.assertEqual(getattr(obj, SLOT), VALUE)

    @staticmethod
    def make_key(klass, key):
        """
        Make the key object.

        :param klass: The YAML data type
        :param key: The key
        :return: the :arg:`key` as the instance of :arg:`klass`
        """
        return NullType() if klass is NullType else klass(key)

    def do_hashability_check(self, cls, key):
        """
        Test whether :arg:`cls` objects are hashable.

        :param cls: The YAML data type
        :param key: The key
        """
        key1 = self.make_key(cls, key)
        key2 = self.make_key(cls, key)
        val1 = 1
        val2 = 2
        dobj = DictType({})

        dobj[key1] = val1
        dobj[key2] = val2

        self.assertEqual(dobj[key1], val2)
        self.assertEqual(dobj[key1], dobj[key])
        self.assertEqual(dobj[key1], dobj[key2])
        self.assertEqual(len(dobj), 1)
        for kobj in dobj:
            self.assertIs(kobj, key1)


class IntTypeTestCase(YamlDataTypeTestCase):
    """Test case for |IntType|."""

    __slots__ = ()

    def test_int_type_mimics_int(self):
        """Test whether |IntType| mimics :class:`int`."""
        self.do_arithmetic_check(IntType, 0, 1)

    def test_int_type_is_extensible(self):
        """Test whether |IntType| can be extended."""
        self.do_extensibility_check(IntType(42))


class FloatTypeTestCase(YamlDataTypeTestCase):
    """Test case for |FloatType|."""

    __slots__ = ()

    def test_float_type_mimics_float(self):
        """Test whether |FloatType| mimics :class:`float`."""
        self.do_arithmetic_check(FloatType, 0.0, 1.0)

    def test_float_type_is_extensible(self):
        """Test whether |FloatType| can be extended."""
        self.do_extensibility_check(FloatType(0.5))


class StrTypeTestCase(YamlDataTypeTestCase):
    """Test case for |StrType|."""

    __slots__ = ()

    def test_str_type_mimics_str(self):
        """Test whether |StrType| mimics :class:`str`."""
        self.do_sequence_check(StrType, "abc", "")

    def test_str_type_is_extensible(self):
        """Test whether |StrType| can be extended."""
        self.do_extensibility_check(StrType("abc"))


class BytesTypeTestCase(YamlDataTypeTestCase):
    """Test case for |BytesType|."""

    __slots__ = ()

    def test_bytes_type_mimics_bytes(self):
        """Test whether |BytesType| mimics :class:`byte`."""
        self.do_sequence_check(BytesType, b"abc", b"")

    def test_bytes_type_is_extensible(self):
        """Test whether |BytesType| can be extended."""
        self.do_extensibility_check(BytesType(b"\0"))


class ListTypeTestCase(YamlDataTypeTestCase):
    """Test case for |ListType|."""

    __slots__ = ()

    def test_list_type_mimics_list(self):
        """Test whether |ListType| mimics :class:`list`."""
        self.do_sequence_check(ListType, [1, 2, 3], [])

    def test_list_type_is_extensible(self):
        """Test whether |ListType| can be extended."""
        self.do_extensibility_check(ListType([1, 2, 3]))


class SetTypeTestCase(YamlDataTypeTestCase):
    """Test case for |SetType|."""

    __slots__ = ()

    def test_set_type_mimics_set(self):
        """Test whether |SetType| mimics :class:`set`."""
        self.assertEqual(SetType({1, 2.5, "a"}), {"a", 1, 2.5})
        self.assertIn("a", SetType({"a"}))
        self.assertFalse(SetType(set()))
        self.assertTrue(SetType({2}))

    def test_set_type_is_extensible(self):
        """Test whether |SetType| can be extended."""
        self.do_extensibility_check(SetType({"a"}))


class DictTypeTestCase(YamlDataTypeTestCase):
    """Test case for |DictType|."""

    __slots__ = ()

    def test_dict_type_mimics_dict(self):
        """Test whether |DictType| mimics :class:`dict`."""
        self.assertEqual(DictType({"a": 1}), {"a": 1})
        self.assertIn("a", DictType({"a": "b"}))
        self.assertEqual(DictType({"a": "b"})["a"], "b")
        self.assertFalse(DictType({}))
        self.assertTrue(DictType({"a": 1}))

    def test_dict_type_is_extensible(self):
        """Test whether |DictType| can be extended."""
        self.do_extensibility_check(DictType({"a": 3.14}))

    def test_null_type_is_hashable(self):
        """Test whether |NullType| is hashable."""
        self.do_hashability_check(NullType, None)

    def test_bool_type_is_hashable(self):
        """Test whether |BoolType| is hashable."""
        self.do_hashability_check(BoolType, True)
        self.do_hashability_check(BoolType, False)

    def test_int_type_is_hashable(self):
        """Test whether |IntType| is hashable."""
        self.do_hashability_check(IntType, 1)

    def test_float_type_is_hashable(self):
        """Test whether |FloatType| is hashable."""
        self.do_hashability_check(FloatType, 1.6)

    def test_str_type_is_hashable(self):
        """Test whether |StrType| is hashable."""
        self.do_hashability_check(StrType, "abc")

    def test_bytes_type_is_hashable(self):
        """Test whether |BytesType| is hashable."""
        self.do_hashability_check(BytesType, b"\xff")

    def test_date_type_is_hashable(self):
        """Test whether |DateType| is hashable."""
        self.do_hashability_check(DateType, datetime.date(2008, 1, 1))

    def test_datetime_type_is_hashable(self):
        """Test whether |DateTimeType| is hashable."""
        self.do_hashability_check(DateTimeType, datetime.datetime(2008, 1, 1))


class DateTypeTestCase(YamlDataTypeTestCase):
    """Test case for |DateType|."""

    __slots__ = ()

    def test_date_type_mimics_date(self):
        """Test whether |DateType| mimics :class:`datetime.date`."""
        date_a = datetime.date(2008, 7, 8)
        date_b = DateType(2008, 7, 8)
        date_c = DateType(date_a)

        self.assertEqual(date_b, date_a)
        self.assertEqual(date_b, date_c)

    def test_date_type_is_extensible(self):
        """Test whether |DateType| can be extended."""
        self.do_extensibility_check(DateType(2008, 1, 1))


class DateTimeTypeTestCase(YamlDataTypeTestCase):
    """Test case for |DateTimeType|."""

    __slots__ = ()

    def test_datetime_type_mimics_datetime(self):
        """Test whether |DateTimeType| mimics :class:`datetime.datetime`."""
        tzinfo = datetime.tzinfo(datetime.timedelta(hours=2, minutes=0))
        dt_a = datetime.datetime(2008, 7, 8, 13, 17, 21, 476, tzinfo, fold=1)
        dt_b = DateTimeType(2008, 7, 8, 13, 17, 21, 476, tzinfo, fold=1)
        dt_c = DateTimeType(dt_a)

        self.assertEqual(dt_b, dt_a)
        self.assertEqual(dt_b, dt_c)

    def test_datetime_type_is_extensible(self):
        """Test whether |DateTimeType| can be extended."""
        self.do_extensibility_check(
            DateTimeType(
                2008,
                1,
                1,
                13,
                0,
                0,
                0,
                datetime.tzinfo(datetime.timedelta(hours=1)),
                fold=0,
            )
        )


class Obj2XObjTestCase(TestCase):
    """Test case for |obj2xobj|."""

    __slots__ = ()

    def do_test_obj2xobj(self, klass, obj):
        """
        Do the |obj2xobj| test.

        :param klass: The subclass of |YamlDataType|
        :param obj: The object
        """
        xobj = obj2xobj(obj)
        self.assertIsInstance(xobj, klass)
        self.assertEqual(xobj, obj)

    def test_obj2xobj(self):
        """Test |obj2xobj|."""
        self.do_test_obj2xobj(NullType, None)
        self.do_test_obj2xobj(BoolType, False)
        self.do_test_obj2xobj(IntType, 1)
        self.do_test_obj2xobj(FloatType, 1.25)
        self.do_test_obj2xobj(StrType, "abc")
        self.do_test_obj2xobj(BytesType, b"\12")
        self.do_test_obj2xobj(ListType, [1, 2])
        self.do_test_obj2xobj(SetType, {1, 2})
        self.do_test_obj2xobj(DictType, {1: 2})
        self.do_test_obj2xobj(DateType, datetime.date(2011, 4, 24))
        self.do_test_obj2xobj(DateTimeType, datetime.datetime(2009, 12, 26))
        with self.assertRaises(TypeError) as ctx:
            obj2xobj(obj2xobj)
        self.assertEqual(
            ctx.exception.args[0],
            "<class 'function'> object cannot be made extensible",
        )


class NewCTestCase(TestCase):
    """Test case for |newc|."""

    __slots__ = ()

    def do_test_newc(self, ctor, obj, *args):
        """
        Do the |newc| test.

        :param ctor: The name of the constructor
        :param obj: The object to be used for comparison
        :param args: Additional positional arguments to |newc|
        """
        cobj = newc(ctor, args)
        self.assertIs(type(cobj), type(obj))
        self.assertEqual(cobj, obj)

    def test_newc(self):
        """Test |newc|."""

        def eqfn(inst, other):
            """
            Equality test.

            :param inst: The instance of the owner object
            :param other: The instance of the other object
            :return: :obj:`True` if the two objects are equal
            """
            return isinstance(other, type(inst)) and inst.foo == other.foo

        tcls = make_type("TestType", members={"foo": 42, "__eq__": eqfn})

        self.do_test_newc("construct_yaml_set", set())
        self.do_test_newc("construct_yaml_map", {})
        self.do_test_newc("construct_yaml_object", tcls(), tcls)
        self.do_test_newc("construct_yaml_seq", [])


class AnnotateTestCase(TestCase):
    """
    Test case for |annotate|.

    :ivar mark: The mock of :class:`yaml.error.Mark` instance
    :ivar node: The mock of :class:`yaml.nodes.Node` instance
    """

    __slots__ = ("mark", "node")

    def setUp(self):
        """Set up the test."""
        mark = make_mock()
        mark.name = "./foo.yml"
        mark.line = 41
        mark.column = 7

        node = make_mock()
        node.start_mark = mark

        self.mark = mark
        self.node = node

    def test_annotate(self):
        """Test |annotate|."""
        obj = annotate({}, self.node)
        loc = getloc(obj)

        self.assertEqual(loc.path, self.mark.name)
        self.assertEqual(loc.line, self.mark.line + 1)
        self.assertEqual(loc.column, self.mark.column + 1)

        with self.assertRaises(yaml.constructor.ConstructorError) as ctx:
            annotate(loc, self.node)
        self.assertEqual(
            str(ctx.exception),
            (
                f"{loc.path}:{loc.line}:{loc.column}: "
                "<class 'vutils.validator.value.Location'>"
                " object cannot be made extensible"
            ),
        )


class GetLocTestCase(TestCase):
    """Test case for |getloc|."""

    __slots__ = ()

    def test_getloc(self):
        """Test |getloc|."""
        data = load_yaml("a: b")
        loc = getloc(data)

        self.assertEqual(loc.path, "<unicode string>")
        self.assertEqual(loc.line, 1)
        self.assertEqual(loc.column, 1)


class KeyLocTestCase(TestCase):
    """Test case for |keyloc|."""

    __slots__ = ()

    def test_keyloc(self):
        """Test |keyloc|."""
        data = load_yaml("{a: 1, b: 2, a: 3}")

        self.assertEqual(keyloc(data, "a").column, 2)
        self.assertEqual(keyloc(data, "b").column, 8)


class IsXTestCase(TestCase):
    """Test case for |is_null| and |is_bool|."""

    __slots__ = ()

    def test_isx(self):
        """Test |is_null| and |is_bool|."""
        self.assertTrue(is_null(NullType()))
        self.assertFalse(is_null(BoolType(False)))

        self.assertTrue(is_bool(BoolType(True)))
        self.assertFalse(is_bool(IntType(0)))
