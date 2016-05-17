from jinja2 import Template

import yaml


def yaml_to_md(layer_name):
    out.write('## ' + layer_name + '\n\n')
    data = yaml.load(inp)

    layer = data['layers'][layer_name]
    attributes = layer['attributes']

    # values of layer attribute "type" (not to be confused with an attribute's type)
    type_values = attributes["type"]['values']

    with open('templates/layer_attributes.md.jinja2') as f:
        layer_attributes_template = Template(f.read())
    out.write(layer_attributes_template.render(attributes=attributes))

    if any('correlated_attributes' in definition for definition in type_values.values()):
        with open('templates/attribute_values_with_aggtype.md.jinja2') as f:
            type_table = f.read()
    else:
        with open('templates/attribute_values.md.jinja2') as f:
            type_table = f.read()

    attribute_values_template = Template(type_table)
    out.write(attribute_values_template.render(type_values=type_values))
    out.write('\n\n')


f = open("osmaxx_schema.yaml", 'r')
inp = f.read()
out = open("documentation.md", 'w')
yaml_to_md('adminarea_a')
yaml_to_md('building_a')
yaml_to_md('geoname_p')
yaml_to_md('landuse_a')
yaml_to_md('military_p')
yaml_to_md('misc_l')
yaml_to_md('natural_a')
yaml_to_md('nonop_l')
yaml_to_md('poi_p')
yaml_to_md('pow_p')
yaml_to_md('railway_bridge_l')
yaml_to_md('road_ground_l')
yaml_to_md('route_l')
yaml_to_md('traffic_a')
yaml_to_md('traffic_p')
yaml_to_md('transport_a')
yaml_to_md('utility_a')
yaml_to_md('utility_p')
yaml_to_md('utility_l')
yaml_to_md('water_a')
yaml_to_md('water_p')
yaml_to_md('water_l')
