#!/usr/bin/env python3
import fontforge
import os
import ruamel.yaml


class FontMaker:
    """
    Usage Example:
        fm = FontMaker('osmaxx_v1_definition.yml')
        fm.create_font()
    """
    def __init__(self, font_config):
        self.config = self.yml_reader(font_config)
        self._base_path = '/home/fonts/osmaxx/svg'
        self.n = fontforge.font()
        self.n.encoding = 'Unicode'

    def yml_reader(self, font_config):
        return ruamel.yaml.load(open(font_config, 'r').read())

    def add_glyph(self, hex_position, svg):
        glyph = self.n.createChar(hex_position)
        glyph.importOutlines(os.path.join(self._base_path, svg))

    def create_font(self):
        for font, definition in self.config.items():
            print("creating {}".format(font))
            self.n.fontname = definition['fontname']
            self.n.familyname = definition['fontname']
            for hex_position, glyph in definition['mappings'].items():
                hex_value = int(hex_position, 16)
                print(hex_value, glyph['filename'])
                self.add_glyph(hex_value, glyph['filename'])
            self.n.save('{}.sfd'.format(definition['fontname']))
            export_file_name = '{}'.format(definition['filename'])
            self.n.generate(export_file_name)
            print("generated: ", export_file_name)

fm = FontMaker('osmaxx_v1_definition.yml')
fm.create_font()
