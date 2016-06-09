#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
from collections import OrderedDict, ChainMap
from ruamel import yaml

env = Environment(
    loader=FileSystemLoader(searchpath='templates'),
    extensions=[
        'jinja2.ext.with_',
    ],
)


def do_dictsort_unless_ordered(value):
    if isinstance(value, OrderedDict):
        return value.items()
    else:
        return sorted(value.items())


def do_included(d):
    dict_t = type(d)
    return dict_t((k, v) for k, v in d.items() if not _is_excluded(k))


def do_excluded(d):
    return ChainMap(*(v for k, v in d.items() if _is_excluded(k)))


def _is_excluded(k):
    return len(k) == 1 and k[0] == 'not'

env.filters['dictsort_unless_ordered'] = do_dictsort_unless_ordered
env.filters['included'] = do_included
env.filters['excluded'] = do_excluded

LAYER_TEMPLATE = env.get_template('layer.md.jinja2')
ATTRIBUTE_VALUES_TEMPLATE = env.get_template('attribute_values.md.jinja2')


def yaml_to_md(layer_name, layer_definition, out):
    out.write(
        LAYER_TEMPLATE.render(
            layer_name=layer_name,
            layer_definition=layer_definition,
        )
    )

    attributes = layer_definition['attributes']

    for attribute_name, attribute in do_dictsort_unless_ordered(attributes):
        try:
            values = attribute['values']
        except KeyError:
            # This is fine. Attributes for which no values are specified will not be documented in a table of their own.
            continue
        else:
            write_attribute_values_table(attribute_name, values, out)


def write_attribute_values_table(attribute_name, attribute_values, out):
    correlated_attributes = set()
    for definition in attribute_values.values():
        for name, _ in definition.get('correlated_attributes', {}).items():
            correlated_attributes.add(name)

    out.write(
        ATTRIBUTE_VALUES_TEMPLATE.render(
            attribute_name=attribute_name,
            attribute_values=attribute_values,
            correlated_attributes=correlated_attributes,
        )
    )
    out.write('\n\n')


with open("osmaxx_schema.yaml", 'r') as in_file:
    data = yaml.load(in_file)
layers = data['layers']
with open('header.md', 'r') as h:
    header_doc = h.read()
with open("documentation.md", 'w') as out_file:
    out_file.write(header_doc)
    for layer_name, layer_definition in sorted(layers.items()):
        yaml_to_md(layer_name, layer_definition, out=out_file)
