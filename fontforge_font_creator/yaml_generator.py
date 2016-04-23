#!/usr/bin/env python3
import os

excluded_ranges = list(range(0x0000, 0x0021)) + list(range(0x007F, 0x00A1))


class Ranger:
    def __init__(self, start, stop, excluded_range=None):
        self.current = start
        self.high = stop
        self.stop = stop
        self.excluded_range = excluded_range

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.stop:
            raise StopIteration
        else:
            self.current += 1
            while self.current in self.excluded_range:
                self.current += 1
                self.stop += 1
            return self.current

svg_dir = os.path.join(os.path.dirname(__file__), '..', 'osmaxx-symbology', 'OSMaxx_point_symbols', 'svg')

svgs = [f for f in os.listdir(svg_dir) if f.endswith('svg')]
svgs.sort()

start_number = 0xE000
r = Ranger(start_number, start_number + len(svgs), excluded_ranges)
outfile = os.path.join(os.path.dirname(__file__), 'osmaxx_v1_definition.yml')
oufile_writer = open(outfile, 'w+')

print('''---
osmaxx_v1:
  filename: OSMaxx_v1.ttf
  fontname: OSMaxx_v1
  mappings:''', file=oufile_writer)

count = 0
for svg in svgs:
    print("    \"{:#06x}\":".format(r.__next__()), file=oufile_writer)
    print("      filename: \"{}\"".format(svg), file=oufile_writer)
    count += 1

