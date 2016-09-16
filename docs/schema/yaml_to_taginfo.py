#!/usr/bin/env python3
import os
import json

from ruamel import yaml

from yamltomd import do_multimapify, do_dictsort_unless_ordered

schema_source_dir = os.path.dirname(__file__)


def write_json():
    with open(os.path.join(schema_source_dir, "osmaxx_schema.yaml"), 'r') as in_file:
        data = yaml.load(in_file)

    layers = data['layers']

    osm_tags_for_layer_attributes = [
        OSMTag(key=k, value=v, layer_name=ln, attribute_name=an, tag_combination=tag_combination)
        for ln, l in do_dictsort_unless_ordered(layers)
        for an, a in do_dictsort_unless_ordered(l['attributes'])
        for tag_combination in a.get('osm_tags', [])
        for k, v in do_dictsort_unless_ordered(tag_combination)
        if k != ("not",)
    ]

    osm_tags_for_layer_attribute_values = [
        OSMTag(key=k, value=v, layer_name=ln, attribute_name=an, attribute_value=avn, tag_combination=tag_combination)
        for ln, l in do_dictsort_unless_ordered(layers)
        for an, a in do_dictsort_unless_ordered(l['attributes'])
        for avn, av in do_dictsort_unless_ordered(do_multimapify(a.get('values', {})))
        for tag_combination in av.get('osm_tags', [])
        for k, v in do_dictsort_unless_ordered(tag_combination)
        if k != ("not",)
    ]

    tags = osm_tags_for_layer_attributes + osm_tags_for_layer_attribute_values

    taginfo_project_data = dict(
        data_format=1,
        data_url="https://raw.githubusercontent.com/geometalab/osmaxx-docs/master/osmaxx.json",
        data_updated="",
        project=dict(
            name="OSMaxx",
            description="OSM Arbitrary Excerpt Export - The source of worldwide data for interactive and printed maps and for geospatial data analysis",
            project_url="http://osmaxx.hsr.ch/",
            doc_url="http://giswiki.hsr.ch/OSMaxx#Documentation",
            icon_url="http://giswiki.hsr.ch/images/2/21/Osmaxx_Logo_16x16.png",
            contact_name="Stefan Keller",
            contact_email="sfkeller@hsr.ch",
        ),
        tags=tags,
    )

    with open(os.path.join(schema_source_dir, "osmaxx_taginfo.json"), 'w') as out_file:
        json.dump(taginfo_project_data, out_file, indent=4, cls=Encoder, sort_keys=True)


class OSMTag:
    def __init__(self, layer_name, attribute_name, key, tag_combination, attribute_value=None, value=None):
        assert isinstance(key, str)
        assert isinstance(layer_name, str)
        assert isinstance(attribute_name, str)
        assert isinstance(attribute_value, str) or isinstance(attribute_value, type(None))
        self.key = key
        self.layer_name = layer_name
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.cotags = tag_combination.copy()
        assert self.cotags.pop(key) == value
        if value == '*':
            value = None
        if value is not None:
            assert isinstance(value, str)
            self.value = value

    @property
    def as_dict(self):
        return dict(
            key=self.key,
            **(self._optional('value')),
            description=self.description,
        )

    @property
    def description(self):
        if self.attribute_value is not None:
            return '{cotags}attribute "{attr_name}" with value "{attr_value}" on layer "{layer_name}"'.format(
                attr_name=self.attribute_name,
                attr_value=self.attribute_value,
                layer_name=self.layer_name,
                cotags=self.cotag_description,
            )
        return '{cotags}attribute "{attr_name}" on layer "{layer_name}"'.format(
            attr_name=self.attribute_name,
            layer_name=self.layer_name,
            cotags=self.cotag_description,
        )

    @property
    def cotag_description(self):
        if len(self.cotags) == 0:
            return ""
        from yamltomd import env
        template = env.from_string("{% import 'osm.md.jinja2' as osm %}"
                                   "(when combined with {{ osm.tag_combination(osm_tags)}}) ")
        return template.render(osm_tags=self.cotags).replace('`', '').replace('**', '')

    def _optional(self, attr_name):
        return {attr_name: getattr(self, attr_name)} if hasattr(self, attr_name) else {}


class Encoder(json.JSONEncoder):
    def default(self, obj):
        return obj.as_dict if hasattr(obj, 'as_dict') else super().default(obj)


if __name__ == "__main__":
    write_json()
