#!/usr/bin/env python3
import os
import unicodedata
from xml.etree import ElementTree

UNICODE_MAX = 0x10FFFF  # last chr of plane 16 (plane 0x10)

class UnicodeRanger:
    def __init__(self, start, stop=UNICODE_MAX):
        assert start >= 0
        assert stop <= UNICODE_MAX
        self.current = start
        self.high = stop
        self.stop = stop
        self._allowed_ranges = [
            ('Co', 'Other', 'Private Use'),
            ('LC', 'Letter', 'Cased'),
            ('Ll', 'Letter', 'Lowercase'),
            ('Lo', 'Letter', 'Other'),
            ('Lt', 'Letter', 'Titlecase'),
            ('Lu', 'Letter', 'Uppercase'),
            ('Nd', 'Number', 'Decimal Digit'),
            ('Sc', 'Symbol', 'Currency'),
            ('Sm', 'Symbol', 'Math'),
            ('So', 'Symbol', 'Other'),
            ('Zs', 'Separator', 'Space'),
        ]
        self._included_ranges = [t[0] for t in self._allowed_ranges]

    def __iter__(self):
        return self

    def __next__(self):
        if self.stop is not None and self.current > self.stop:
            raise StopIteration
        else:
            self.current += 1
            while unicodedata.category(chr(self.current)) not in self._included_ranges:
                self.current += 1
                self.stop += 1
            return self.current

svg_dir = os.path.join(os.path.dirname(__file__), '..', 'osmaxx-symbology', 'OSMaxx_point_symbols', 'svg')

svgs = [f for f in os.listdir(svg_dir) if f.lower().endswith('.svg')]
svgs.sort()

start_number = 0xE000
r = UnicodeRanger(start_number)
outfile = os.path.join(os.path.dirname(__file__), 'osmaxx_v1_definition.yml')
oufile_writer = open(outfile, 'w+')

ns = dict(svg='http://www.w3.org/2000/svg')

print('''---
osmaxx_v1:
  filename: OSMaxx_v1.ttf
  fontname: OSMaxx_v1
  mappings:''', file=oufile_writer)

count = 0
already_done = set()
for svg in svgs:
    tree = ElementTree.parse(os.path.join(svg_dir, svg))
    for path_el in tree.findall('.//svg:path', ns):
        h = hash(path_el.get('d'))
        if h not in already_done:
            el_id = path_el.get('id')
            print("    \"{:#06x}\":".format(r.__next__()), file=oufile_writer)
            print("      filename: \"{}\"".format(svg), file=oufile_writer)
            print("      element: \"{}\"".format(el_id), file=oufile_writer)
            already_done.add(h)
            count += 1
