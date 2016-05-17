from jinja2 import Template

import yaml

LAYERS_TO_BE_DOCUMENTED = [
    'adminarea_a',
    'building_a',
    'geoname_p',
    'landuse_a',
    'military_p',
    'misc_l',
    'natural_a',
    'nonop_l',
    'poi_p',
    'pow_p',
    'railway_bridge_l',
    'road_ground_l',
    'route_l',
    'traffic_a',
    'traffic_p',
    'transport_a',
    'utility_a',
    'utility_p',
    'utility_l',
    'water_a',
    'water_p',
    'water_l',
]


def yaml_to_md(layer_name, layer_definition, out):
    out.write('## ' + layer_name + '\n\n')

    attributes = layer_definition['attributes']

    # values of layer attribute "type" (not to be confused with an attribute's type)
    type_values = attributes["type"]['values']

    with open('templates/layer_attributes.md.jinja2') as f:
        layer_attributes_template = Template(f.read())
    out.write(layer_attributes_template.render(attributes=attributes))

    if any('correlated_attributes' in definition for definition in type_values.values()):
        with open('templates/attribute_values_with_aggtype.md.jinja2') as f:
            attribute_values_template = Template(f.read())
    else:
        with open('templates/attribute_values.md.jinja2') as f:
            attribute_values_template = Template(f.read())

    out.write(attribute_values_template.render(type_values=type_values))
    out.write('\n\n')


with open("osmaxx_schema.yaml", 'r') as in_file:
    data = yaml.load(in_file)
layers = data['layers']
with open("documentation.md", 'w') as out_file:
    for layer_name in LAYERS_TO_BE_DOCUMENTED:
        yaml_to_md(layer_name, layers[layer_name], out=out_file)
