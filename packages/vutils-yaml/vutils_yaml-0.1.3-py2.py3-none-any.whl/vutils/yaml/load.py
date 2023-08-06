#
# File:    ./src/vutils/yaml/load.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-24 00:41:59 +0200
# Project: vutils-yaml: Working with YAML format
#
# SPDX-License-Identifier: MIT
#
"""Load YAML document."""

from typing import TYPE_CHECKING, cast

import yaml

from vutils.yaml.utils import YamlDataType, annotate_constructed_objects

if TYPE_CHECKING:
    from collections.abc import Callable

    from vutils.yaml import StreamType


@annotate_constructed_objects(
    ("construct_scalar", None, False),
    ("construct_sequence", None, False),
    ("construct_mapping", None, False),
    ("construct_pairs", None, False),
    ("construct_yaml_null", "tag:yaml.org,2002:null", False),
    ("construct_yaml_bool", "tag:yaml.org,2002:bool", False),
    ("construct_yaml_int", "tag:yaml.org,2002:int", False),
    ("construct_yaml_float", "tag:yaml.org,2002:float", False),
    ("construct_yaml_binary", "tag:yaml.org,2002:binary", False),
    ("construct_yaml_timestamp", "tag:yaml.org,2002:timestamp", False),
    ("construct_yaml_omap", "tag:yaml.org,2002:omap", True),
    ("construct_yaml_pairs", "tag:yaml.org,2002:pairs", True),
    ("construct_yaml_set", "tag:yaml.org,2002:set", True),
    ("construct_yaml_str", "tag:yaml.org,2002:str", False),
    ("construct_yaml_seq", "tag:yaml.org,2002:seq", True),
    ("construct_yaml_map", "tag:yaml.org,2002:map", True),
    ("construct_yaml_object", None, True),
)
class AnnotateConstructor(yaml.constructor.SafeConstructor):
    """Construct annotated YAML objects."""

    __slots__ = ()


class AnnotateLoader(
    yaml.reader.Reader,
    yaml.scanner.Scanner,
    yaml.parser.Parser,
    yaml.composer.Composer,
    AnnotateConstructor,
    yaml.resolver.Resolver,
):
    """Load YAML, annotate constructed objects."""

    __slots__ = ()

    def __init__(self, stream: "StreamType") -> None:
        """
        Initialize the YAML loader.

        :param stream: The stream
        """
        yaml.reader.Reader.__init__(self, stream)
        yaml.scanner.Scanner.__init__(self)
        yaml.parser.Parser.__init__(self)
        yaml.composer.Composer.__init__(self)
        AnnotateConstructor.__init__(self)
        yaml.resolver.Resolver.__init__(self)


def load_yaml(stream: "StreamType") -> YamlDataType:
    """
    Load YAML from the stream.

    :param stream: The stream
    :return: the YAML document object
    """
    loader: AnnotateLoader = AnnotateLoader(stream)
    try:
        return cast(YamlDataType, loader.get_single_data())
    finally:
        cast("Callable[[], None]", loader.dispose)()
