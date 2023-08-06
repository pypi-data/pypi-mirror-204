[![Coverage Status](https://coveralls.io/repos/github/i386x/vutils-yaml/badge.svg?branch=main)](https://coveralls.io/github/i386x/vutils-yaml?branch=main)
![CodeQL](https://github.com/i386x/vutils-yaml/actions/workflows/codeql.yml/badge.svg)

# vutils-yaml: Working with YAML Format

This package provides tools for loading data from and saving data to the YAML
format. Features:
* It annotates data while loading them from the YAML format. Every object
  returned by `vutils.yaml.load.load_yaml` has information about its origin.
  This is useful when reporting errors.

Limitations:
* Due to the annotating data, this packages is not suitable for loading YAML
  formatted data containing thousands and hundreds of thousands items. For such
  amounts of data use [PyYAML](https://pypi.org/project/PyYAML/) or other YAML
  parser since it is supposed that large data sets are usually
  machine-generated and consistent so further verification is not required.
* When used for the first time, `vutils.yaml.utils.keyloc` function builds a
  mapping between `dict` keys and their locations. This can be a bottle-neck
  for large dictionaries.

Due to the limitations, this package is suitable for parsing human-written
configurations in YAML format containing at most hundreds of items.

## Installation

```sh
pip install vutils-yaml
```

## How to Use

Topic covered in this short guide is:
* loading annotated YAML data
* API reference

### Loading Annotated YAML Data

To load YAML data with annotations, use the `load_yaml` function from
`vutils.yaml.load`. Example:
```python
from vutils.yaml.load import load_yaml
from vutils.yaml.utils import is_null, keyloc

stream = """
---
food:
  fruit:
    - apple
    - banana
    - orange
  vegetable:
    - potato
    - tomato
    - carrot
  meat: null
"""

data = load_yaml(stream)
food = data["food"]
# `if food["meat"] is None` will not work, `null` is converted to `NullType`
# object to be annotated
if is_null(food["meat"]):
    # `keyloc` retrieves the annotated key object from `food` and return its
    # location
    print(f"{keyloc(food, 'meat')}: At least one kind of meat is required.")
```
Observe the testing if the value is `null` and the retrieving the `meat` key
location to inform a user where the problem with his/her data is.

### API Reference

Module `vutils.yaml.load` provide these functions:
* `load_yaml(stream)` loads YAML data from `stream` and annotates them.
  `stream` can be `str`, `bytes`, or a `file`-like object supporting `read`.

Module `vutils.yaml.utils` provide these functions:
* `getloc(obj)` retrieves the location of `obj`
* `keyloc(obj, kobj)` retrieves the location of `kobj`, which is a key of
  `dict`-like object `obj`.
* `is_null(obj)` tests whether `obj` is `null`.
* `is_bool(obj)` tests whether `obj` is of the Boolean type.
