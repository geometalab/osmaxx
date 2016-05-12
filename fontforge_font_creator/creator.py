#!/usr/bin/env python3
import fontforge
import os
import ruamel.yaml
import shutil
from xml.etree import ElementTree
from tempfile import NamedTemporaryFile

class FontMaker:
    """
    Usage Example:
        fm = FontMaker('osmaxx_v1_definition.yml')
        fm.create_font()
    """
    def __init__(self, font_config):
        self.config = self.read_yaml(font_config)
        self._base_path = '/home/fonts/osmaxx/svg'
        self.fontforge_font = fontforge.font()
        self.fontforge_font.encoding = 'Unicode'

    def read_yaml(self, file_name):
        with open(file_name, 'r') as yaml_file:
            parsed_yaml = ruamel.yaml.load(yaml_file.read())
        return parsed_yaml

    def fillet_glyph(self, svg, element_name):
        ns = dict(svg='http://www.w3.org/2000/svg')
        tree = ElementTree.parse(os.path.join(self._base_path, svg))
        for parent in tree.findall('.//svg:path/..', ns):
            for path_el in parent.getchildren():
                if path_el.get('id') != element_name:
                    parent.remove(path_el)
        return tree

    def add_glyph(self, hex_position, svg):
        glyph = self.fontforge_font.createChar(hex_position)
        glyph.importOutlines(os.path.join(self._base_path, svg))
        assert glyph.isWorthOutputting()

    def create_font(self):
        for font, definition in self.config.items():
            print("creating {}".format(font))
            self.fontforge_font.fontname = definition['fontname']
            self.fontforge_font.familyname = definition['fontname']
            self.fontforge_font.fullname = definition['fontname']
            self.fontforge_font.comment = definition['fontname']
            self.fontforge_font.weight = 'normal'
            for hex_position, glyph in definition['mappings'].items():
                hex_value = int(hex_position, 16)
                print(hex_value, glyph['filename'], glyph['element'])
                tree = self.fillet_glyph(glyph['filename'], glyph['element'])
                with NamedTemporaryFile(suffix='.svg') as glyph_svg_file:
                    tree.write(glyph_svg_file)
                    glyph_svg_file.flush()
                    self.add_glyph(hex_value, glyph_svg_file.name)
            self.fontforge_font.save('{}.sfd'.format(definition['fontname']))
            export_file_name = '{}'.format(definition['filename'])
            self.fontforge_font.generate(export_file_name)
            print("generated: ", export_file_name)
            shutil.move(export_file_name, '/out/OSMaxx_v1.ttf')

if __name__ == '__main__':
    fm = FontMaker('osmaxx_v1_definition.yml')
    fm.create_font()
