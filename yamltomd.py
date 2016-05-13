from jinja2 import Template
from jinja2 import Environment

import yaml


def yaml_to_md(table):
    out.write('## ' + table + '\n\n')
    for data in yaml.load_all(inp):
        key = data['layers'].keys()
        key1 = data['layers'][table]['attributes'].keys()
        dicts = data['layers'][table]['attributes']
        dicts2 = dicts['type']['values']
        key2 = dicts2.keys()

        s =  '|Attributes          |type                |Description                                                           |osm_tags            |\n'
        s += '| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |\n'

        s += "{% for i in range(0, a1) %}"
        s += "{% if dicts[mylist1[i]]['osm_tags'] is defined %}|"
        s += "{{ mylist1[i] }}|"
        s += "{{ dicts[mylist1[i]]['type'] }}|"
        s += "{{ dicts[mylist1[i]]['description'] }}|"
        s += "{{ dicts[mylist1[i]]['osm_tags'].keys()[0]}}=*|\n"
        s += "{% endif %}"
        s += "{% endfor %}"

        t2 = Template(s)
        out.write(t2.render(mylist1=key1, a1=len(key1), space=' ', dicts=dicts))

        if 'correlated_attributes' in dicts2[key2[0]].keys():
            type_table = "\n Values of attributes type  \n\n"
            type_table += '|aggtype             |values              |osm_tags            |description                                                           |\n'
            type_table += '| ------------------ | ------------------ | ------------------ | -------------------------------------------------------------------- |\n'
            type_table += "{% for i in range(0, a)%}"
            type_table += "|{{ dicts[typelist[i]]['correlated_attributes'].values()[0]}}"
            type_table += "|{{ typelist[i] }}|"
            type_table += "{{ dicts[typelist[i]]['osm_tags'][0].keys()[0] }}='{{ dicts[typelist[i]]['osm_tags'][0].values()[0] }}' "
            type_table += "{% if dicts[typelist[i]]['osm_tags'][1] is defined %}"
            type_table += "{{ dicts[typelist[i]]['osm_tags'][1].keys()[0] }}='{{ dicts[typelist[i]]['osm_tags'][1].values()[0] }}'|"
            type_table += "{% else %}"
            type_table += "|"
            type_table += "{% endif %}"
            type_table += "{{ dicts[typelist[i]]['description'] }}|\n"
            type_table += "{% endfor %}"
        else:
            type_table = "\n Values of attributes type  \n\n"
            type_table += '|values              |osm_tags            |description                                                           |\n'
            type_table += '| ------------------ | ------------------ | -------------------------------------------------------------------- |\n'
            type_table += "{% for i in range(0, a)%}"
            type_table += "|{{ typelist[i] }}|"
            type_table += "{{ dicts[typelist[i]]['osm_tags'][0].keys()[0] }}='{{ dicts[typelist[i]]['osm_tags'][0].values()[0] }}' "
            type_table += "{% if dicts[typelist[i]]['osm_tags'][1] is defined %}"
            type_table += "{{ dicts[typelist[i]]['osm_tags'][1].keys()[0] }}='{{ dicts[typelist[i]]['osm_tags'][1].values()[0] }}'|"
            type_table += "{% else %}"
            type_table += "|"
            type_table += "{% endif %}"
            type_table += "{{ dicts[typelist[i]]['description'] }}|\n"
            type_table += "{% endfor %}"

        t3 = Template(type_table)
        out.write(t3.render(typelist=key2, a=len(key2), dicts=dicts2))
        out.write('\n\n')


f = open("osmaxx_trial.yaml", 'r')
inp = f.read()
out = open("mdtrial.md", 'w')
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
