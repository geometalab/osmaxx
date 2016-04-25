#!/usr/bin/env python3
import fontforge
import os
import ruamel.yaml
import shutil


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

    def add_glyph(self, hex_position, svg):
        glyph = self.fontforge_font.createChar(hex_position)
        glyph.importOutlines(os.path.join(self._base_path, svg))

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
                print(hex_value, glyph['filename'])
                self.add_glyph(hex_value, glyph['filename'])
            self.fontforge_font.save('{}.sfd'.format(definition['fontname']))
            export_file_name = '{}'.format(definition['filename'])
            self.fontforge_font.generate(export_file_name)
            print("generated: ", export_file_name)
            shutil.move(export_file_name, '/out/OSMaxx_v1.ttf')

fm = FontMaker('osmaxx_v1_definition.yml')
fm.create_font()
