#!/usr/bin/env python3
import os
from itertools import chain

from jinja2 import Environment, FileSystemLoader
from collections import OrderedDict, ChainMap, Mapping
from ruamel import yaml

schema_source_dir = os.path.dirname(__file__)
schema_markdown_dir = os.path.dirname(schema_source_dir)

env = Environment(
    loader=FileSystemLoader(searchpath=os.path.join(schema_source_dir, 'templates')),
    extensions=[
        'jinja2.ext.with_',
    ],
)


def do_layer_geometry_type(layer_name):
    return dict(
        _a='MultiPolygon',
        _l='MultiLineString',
        _p='Point',
    )[layer_name[-2:]].upper()


def do_multimapify(value):
    if isinstance(value, Mapping):
        return value
    else:
        return PseudoMultiMap(value)


class PseudoMultiMap:
    def __init__(self, iterable):
        assert all(len(item) == 2 for item in iterable)  # Require an iterable of pairs
        self._items = tuple(iterable)

    def items(self):
        return self._items

    def keys(self):
        return tuple(k for k, _ in self._items)

    def values(self):
        return tuple(v for _, v in self._items)


def do_collect_correlated_attributes(attribute_values):
    attribute_value_definitions = attribute_values.values()
    return ChainMap(
        *(definition.get('correlated_attributes', {}) for definition in attribute_value_definitions)
    ).keys()


def do_dictsort_unless_ordered(value):
    if isinstance(value, OrderedDict) or isinstance(value, PseudoMultiMap):
        return value.items()
    else:
        return sorted(value.items(), key=lambda x: tuple(str(y) for y in x))


def do_included(d):
    dict_t = type(d)
    return dict_t((k, v) for k, v in d.items() if not _is_excluded(k))


def do_excluded(d):
    if all(isinstance(v, list) for k, v in d.items() if _is_excluded(k)):
        return_t = lambda *x: list(chain(*x))
    else:
        return_t = ChainMap
    return return_t(*(v for k, v in d.items() if _is_excluded(k)))


def _is_excluded(k):
    return len(k) == 1 and k[0] == 'not'

env.filters['layer_geometry_type'] = do_layer_geometry_type
env.filters['collect_correlated_attributes'] = do_collect_correlated_attributes
env.filters['multimapify'] = do_multimapify
env.filters['dictsort_unless_ordered'] = do_dictsort_unless_ordered
env.filters['included'] = do_included
env.filters['excluded'] = do_excluded

LAYERS_TEMPLATE = env.get_template('layers.md.jinja2')

with open(os.path.join(schema_source_dir, "osmaxx_schema.yaml"), 'r') as in_file:
    data = yaml.load(in_file)
layers = data['layers']
with open(os.path.join(schema_source_dir, 'header.md'), 'r') as h:
    header_doc = h.read()
with open(os.path.join(schema_markdown_dir, "osmaxx_data_schema.md"), 'w') as out_file:
    out_file.write(header_doc)
    out_file.write(
        LAYERS_TEMPLATE.render(
            layers=layers,
        )
    )
