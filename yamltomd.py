from jinja2 import Template

import yaml


def yaml_to_md(table):
    out.write('## ' + table + '\n\n')
    data = yaml.load(inp)

    attribute_names = data['layers'][table]['attributes'].keys()
    attributes = data['layers'][table]['attributes']
    dicts2 = attributes['type']['values']
    key2 = dicts2.keys()

    with open('templates/layer_attributes.md.jinja2') as f:
        t2 = Template(f.read())
    out.write(t2.render(attribute_names=attribute_names, attributes=attributes))

    if 'correlated_attributes' in dicts2[key2[0]].keys():
        with open('templates/attribute_values_with_aggtype.md.jinja2') as f:
            type_table = f.read()
    else:
        with open('templates/attribute_values.md.jinja2') as f:
            type_table = f.read()

    t3 = Template(type_table)
    out.write(t3.render(typelist=key2, a=len(key2), dicts=dicts2))
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
