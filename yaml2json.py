from jinja2 import Template

import yaml

f = open("osmaxx_trial.yaml", 'r')
inp = f.read()
out = open("osmaxx.json", 'w')

data = yaml.load(inp)
table = data['layers'].keys()
for i in range(0, len(table)):
	dicts = data['layers'][table[i]]
	attr = dicts['attributes'].keys()
	for j in range(0, len(attr)):
		if attr[j] == 'type':

			type_attr = dicts['attributes'][attr[j]]['values'].keys()
			
			for k in range(0, len(type_attr)):
				type_tags = dicts['attributes'][attr[j]]['values'][type_attr[k]]['osm_tags']
				type_tags_description = dicts['attributes'][attr[j]]['values'][type_attr[k]]['description']
				type_len = len(type_tags)

				for l in range(0, type_len):
					if type_tags[l] == None:
						continue
					else:

						s = "{{ '\n{'|indent(16, true) }}"
						s += "{{ '\n\"key\": '|indent(16, true)}}"
						s += "\"{{ type_tags[m].keys()[0] }}\",\n"
						s += "{{ '\"value\": '|indent(16, true) }}"
						s += "\"{{ type_tags[m].values()[0] }}\",\n"        
						s += "{{ '\"description\": '|indent(16, true) }}"
						s += "\"{{ type_tags_description }}\""
						s += "{{ '\n},'|indent(16, true) }}"

						t = Template(s)
						out.write(t.render(type_tags=type_tags, type_tags_description=type_tags_description, m=l))


		if 'osm_tags' in dicts['attributes'][attr[j]].keys() or \
		table[i] == 'road_ground_l' or table[i] == 'road_bridge_l' or table[i] == 'road_tunnel_l' \
		or table[i] == 'railway_ground_l' or table[i] == 'railway_bridge_l' or table[i] == 'railway_tunnel_l':
			if attr[j] == 'bridge' or attr[j] == 'tunnel':

				attr_tags_keys = dicts['attributes'][attr[j]]['values'][dicts['attributes'][attr[j]]['values'].keys()[0]] \
				                 ['osm_tags'].keys()
				attr_tags_values = dicts['attributes'][attr[j]]['values'][dicts['attributes'][attr[j]]['values'].keys()[0]] \
				                   ['osm_tags'].values()
				attr_tags_description = dicts['attributes'][attr[j]]['description']


				s = "{{ '\n{'|indent(16, true) }}"
				s += "{{ '\n\"key\": '|indent(16, true)}}"
				s += "\"{{ attr_tags_keys[0] }}\",\n"
				s += "{{ '\"value\": '|indent(16, true) }}"
				s += "\"{{ attr_tags_values[0] }}\",\n"        
				s += "{{ '\"description\": '|indent(16, true) }}"
				s += "\"{{ attr_tags_description }}\""
				s += "{{ '\n},'|indent(16, true) }}"


				t = Template(s)
				out.write(t.render(attr_tags_keys=attr_tags_keys, attr_tags_description=attr_tags_description, \
					               attr_tags_values=attr_tags_values))
			elif attr[j] == 'aggtype' or attr[j] == 'type':
				continue
			
			else: 
				
				attr_tags_keys = dicts['attributes'][attr[j]]['osm_tags'].keys()
				attr_tags_description = dicts['attributes'][attr[j]]['description']


				s = "{{ '\n{'|indent(16, true) }}"
				s += "{{ '\n\"key\": '|indent(16, true)}}"
				s += "\"{{ attr_tags_keys[0] }}\",\n"
				s += "{{ '\"description\": '|indent(16, true) }}"
				s += "\"{{ attr_tags_description }}\""
				s += "{{ '\n},'|indent(16, true) }}"


				t = Template(s)
				out.write(t.render(attr_tags_keys=attr_tags_keys, attr_tags_description=attr_tags_description))
		

		elif table[i] == 'nonop_l':
			continue

		elif attr[j] == 'aggtype':
			continue
		