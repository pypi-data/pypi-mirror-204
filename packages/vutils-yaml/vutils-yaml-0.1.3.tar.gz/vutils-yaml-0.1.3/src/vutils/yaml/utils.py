#
# File:    ./src/vutils/yaml/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-23 21:40:39 +0200
# Project: vutils-yaml: Working with YAML format
#
# SPDX-License-Identifier: MIT
#
"""
Miscellaneous utilities.

:const ANNOTATION_SLOT: The name of the slot that holds an annotation
:const KEYLOC_SLOT: The name of the slot that holds the location of a key
:const TYPEMAP: The mapping between type and its annotation-friendly wrapper
"""

import datetime
from typing import TYPE_CHECKING, cast

import yaml
from vutils.python.objects import merge_data
from vutils.validator.value import Location

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Iterator

    from vutils.yaml import (
        CtorDecorType,
        CtorFuncType,
        CtorSpecType,
        CtorType,
        MarkType,
        NodeType,
        PyDict,
        PyList,
        PySet,
        new_date,
        new_datetime,
    )
else:
    PyList = list
    PySet = set
    PyDict = dict
    new_date = datetime.date.__new__
    new_datetime = datetime.datetime.__new__

ANNOTATION_SLOT: str = "__yaml_annotation__"
KEYLOC_SLOT: str = "__yaml_keyloc__"


class Annotation:
    """
    Holds YAML values annotation.

    :ivar location: The value's location
    """

    location: Location
    __slots__ = ("location",)

    def __init__(self, location: "Location | None" = None) -> None:
        """
        Initialize annotation object.

        :param location: The YAML value's location
        """
        if location is None:
            location = Location()
        self.location = location


class YamlDataType:
    """Base class for annotated YAML objects."""

    __slots__ = ()


class NullType(YamlDataType):
    """
    A null (:obj:`None`) type.

    Since :obj:`None` has a special meaning it cannot be annotated nor it is
    possible to inherit from its type. This workaround is used to store
    annotation alongside with ``null``.
    """

    def __bool__(self) -> bool:
        """
        Convert :class:`.NullType` object to the :class:`bool` object.

        :return: always :obj:`False`
        """
        return False

    def __eq__(self, other: object) -> bool:
        """
        Test the equality of this and the :arg:`other` object.

        :param other: The other object
        :return: :obj:`True` if this and the :arg:`other` object are considered
            equal
        """
        return other is None or isinstance(other, type(self))

    def __hash__(self) -> int:
        """
        Return the object hash.

        :return: the hash of this object
        """
        return hash(None)


class BoolType(YamlDataType):
    """
    Represent a Boolean type.

    Since :class:`bool` is not an acceptable base class this workaround is used
    to store annotation alongside with Boolean values.
    """

    __value: bool

    def __init__(self, value: bool) -> None:
        """
        Initialize the :class:`bool`-like object.

        :param value: The value
        """
        YamlDataType.__init__(self)
        self.__value = value

    def __bool__(self) -> bool:
        """
        Convert this object to :class:`bool` object.

        :return: the kept value
        """
        return self.__value

    def __eq__(self, other: object) -> bool:
        """
        Test the equality of this and the :arg:`other` object.

        :param other: The other object
        :return: :obj:`True` if this and the :arg:`other` object are considered
            equal
        """
        if isinstance(other, (bool, BoolType)):
            return bool(self) is bool(other)
        if isinstance(other, (int, float)):
            return int(bool(self)) == other
        return False

    def __hash__(self) -> int:
        """
        Return the object hash.

        :return: the hash of this object
        """
        return hash(bool(self))


class IntType(int, YamlDataType):
    """
    Wrap the :class:`int` type.

    Needed to store annotation.
    """


class FloatType(float, YamlDataType):
    """
    Wrap the :class:`float` type.

    Needed to store annotation.
    """


class StrType(str, YamlDataType):
    """
    Wrap the :class:`str` type.

    Needed to store annotation.
    """


class BytesType(bytes, YamlDataType):
    """
    Wrap the :class:`bytes` type.

    Needed to store annotation.
    """


class ListType(PyList, YamlDataType):
    """
    Wrap the :class:`list` type.

    Needed to store annotation.
    """


class SetType(PySet, YamlDataType):
    """
    Wrap the :class:`set` type.

    Needed to store annotation.
    """


class DictType(PyDict, YamlDataType):
    """
    Wrap the :class:`dict` type.

    Needed to store annotation.
    """


class DateType(datetime.date, YamlDataType):
    """
    Wrap the :class:`datetime.date` type.

    Needed to store annotation.
    """

    def __new__(cls, *args: object) -> "DateType":
        """
        Create the date object.

        :param args: Either :class:`datetime.date` object or
            :class:`datetime.date`'s positional arguments
        :return: the date object
        """
        if isinstance(args[0], datetime.date):
            date: datetime.date = args[0]
            return datetime.date.__new__(cls, date.year, date.month, date.day)
        return new_date(cls, *args)


class DateTimeType(datetime.datetime, YamlDataType):
    """
    Wrap the :class:`datetime.datetime` type.

    Needed to store annotation.
    """

    def __new__(cls, *args: object, **kwargs: object) -> "DateTimeType":
        """
        Create the datetime object.

        :param args: Either :class:`datetime.datetime` object or
            :class:`datetime.datetime`'s positional arguments
        :param kwargs: Key-value arguments to :class:`datetime.datetime`
        :return: the datetime object
        """
        if isinstance(args[0], datetime.datetime):
            stamp: datetime.datetime = args[0]
            return datetime.datetime.__new__(
                cls,
                stamp.year,
                stamp.month,
                stamp.day,
                stamp.hour,
                stamp.minute,
                stamp.second,
                stamp.microsecond,
                stamp.tzinfo,
                fold=stamp.fold,
            )
        return new_datetime(cls, *args, **kwargs)


TYPEMAP: "dict[object, type[YamlDataType]]" = {
    bool: BoolType,
    int: IntType,
    float: FloatType,
    str: StrType,
    bytes: BytesType,
    list: ListType,
    set: SetType,
    dict: DictType,
    datetime.date: DateType,
    datetime.datetime: DateTimeType,
}


def obj2xobj(obj: object) -> YamlDataType:
    """
    Make object extensible.

    :param obj: The object
    :return: the extensible object
    :raises TypeError: when object cannot be made extensible

    Make object extensible so additional information can be added to it. This
    changes the object type.
    """
    if obj is None:
        return NullType()
    cls: "type[YamlDataType] | None" = TYPEMAP.get(type(obj))
    if cls is None:
        raise TypeError(f"{type(obj)} object cannot be made extensible")
    return cast("Callable[[object], YamlDataType]", cls)(obj)


def newc(name: str, args: "tuple[object, ...]") -> object:
    """
    Create a new container based on the constructor name.

    :param name: The constructor name
    :param args: The constructor arguments
    :return: the new container
    """
    if name == "construct_yaml_set":
        return set()
    if name == "construct_yaml_map":
        return {}
    if name == "construct_yaml_object":
        return cast("Callable[[object], object]", args[0].__new__)(args[0])
    return []


def annotate(data: object, node: "NodeType") -> YamlDataType:
    """
    Annotate data with information from node.

    :param data: The data object
    :param node: The node
    :return: the annotated data object
    :raises yaml.error.YAMLError: when operation fails
    """
    mark: "MarkType" = node.start_mark
    name: str = mark.name
    line: int = mark.line + 1
    column: int = mark.column + 1

    ydata: YamlDataType = cast(YamlDataType, data)
    if not hasattr(data, ANNOTATION_SLOT):
        try:
            ydata = obj2xobj(data)
        except TypeError as exc:
            detail: str = cast("tuple[str]", exc.args)[0]
            raise yaml.constructor.ConstructorError(
                f"{name}:{line}:{column}: {detail}"
            )
        setattr(ydata, ANNOTATION_SLOT, Annotation())

    location: Location = getloc(ydata)
    location.path = name
    location.line = line
    location.column = column

    return ydata


def make_ctor(name: str, base_cls: "type[CtorType]") -> "CtorFuncType":
    """
    Create YAML object constructor (function).

    :param name: The constructor function name
    :param base_cls: The base of the constructor class
    :return: the constructor function
    """

    def ctor(
        inst: "CtorType", node: "NodeType", *args: object, **kwargs: object
    ) -> object:
        """
        Construct an annotated YAML object.

        :param inst: The YAML constructor class instance
        :param node: The node
        :param args: Additional positional arguments
        :param kwargs: Additional key-value arguments
        :return: the annotated YAML object
        """
        base_ctor: "CtorFuncType" = cast(
            "CtorFuncType", getattr(base_cls, name)
        )
        data: object = base_ctor(inst, node, *args, **kwargs)
        return annotate(data, node)

    return ctor


def make_gctor(name: str, base_cls: "type[CtorType]") -> "CtorFuncType":
    """
    Create YAML object constructor (generator).

    :param name: The constructor name
    :param base_cls: The base of the constructor class
    :return: the constructor generator
    """

    def gctor(
        inst: "CtorType", node: "NodeType", *args: object, **kwargs: object
    ) -> "Iterator[object]":
        """
        Generate an annotated YAML object.

        :param inst: The YAML constructor class instance
        :param node: The node
        :param args: Additional positional arguments
        :param kwargs: Additional key-value arguments
        :return: the annotated YAML object
        """
        data: object = annotate(newc(name, args), node)
        yield data
        base_ctor: "CtorFuncType" = cast(
            "CtorFuncType", getattr(base_cls, name)
        )
        generator: "Iterator[object]" = cast(
            "Iterator[object]", base_ctor(inst, node, *args, **kwargs)
        )
        gdata: object = {}
        for item in generator:
            gdata = item
        merge_data(data, gdata)

    return gctor


def annotate_constructed_objects(*spec: "CtorSpecType") -> "CtorDecorType":
    """
    Annotate constructed YAML objects with their location.

    :param spec: Each argument is a triple holding constructor name, tag, and
        a Boolean value, respectively, saying whether the constructor is a
        generator or not. Constructor name specifies the constructor involved
        in annotating a YAML object during its construction, tag is a tag
        associated with the constructor or :obj:`None`
    :return: the decorator function that patches the class
    """

    def patch_constructors(cls: "type[CtorType]") -> "type[CtorType]":
        """
        Patch YAML object constructors.

        :param cls: The constructor class
        :return: the patched constructor class

        A decorator that patches YAML object constructors of the given class
        with the ability to annotate constructed objects with their location.
        """
        base_cls: "type[CtorType]" = cls.__bases__[0]
        for name, tag, is_gen in spec:
            mfunc: "CtorFuncType" = (
                make_gctor(name, base_cls)
                if is_gen
                else make_ctor(name, base_cls)
            )
            setattr(cls, name, mfunc)
            if tag is not None:
                cast("dict[str, CtorFuncType]", cls.yaml_constructors)[
                    tag
                ] = mfunc
        return cls

    return patch_constructors


def getloc(obj: YamlDataType) -> Location:
    """
    Get the location of the object.

    :param obj: The object
    :return: the location of the object
    """
    return cast(
        Annotation, getattr(obj, ANNOTATION_SLOT, Annotation())
    ).location


def keyloc(obj: DictType, kobj: object) -> Location:
    """
    Get the location of the key object.

    :param obj: The annotated :class:`dict` object
    :param kobj: The key
    :return: the location of the key
    """
    if not hasattr(obj, KEYLOC_SLOT):
        key2loc: "dict[YamlDataType, Location]" = {}
        for key in obj:
            key2loc[cast(YamlDataType, key)] = getloc(cast(YamlDataType, key))
        setattr(obj, KEYLOC_SLOT, key2loc)
    return cast("dict[object, Location]", getattr(obj, KEYLOC_SLOT)).get(
        kobj, Location()
    )


def is_null(obj: YamlDataType) -> bool:
    """
    Test whether the object is null.

    :param obj: The annotated object
    :return: :obj:`True` if :arg:`obj` is null
    """
    return isinstance(obj, NullType)


def is_bool(obj: YamlDataType) -> bool:
    """
    Test whether the object has Boolean type.

    :param obj: The annotated object
    :return: :obj:`True` if :arg:`obj` has Boolean type
    """
    return isinstance(obj, BoolType)
