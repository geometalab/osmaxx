import os

import pytest


@pytest.fixture
def simple_osmosis_line_string():
    return os.linesep.join([
        'none',
        '1-outer',
        '  0.000000E+00 0.000000E+00',
        '  0.000000E+00 1.000000E+00',
        '  1.000000E+00 1.000000E+00',
        '  0.000000E+00 0.000000E+00',
        'END',
        '2-outer',
        '  1.000000E+00 1.000000E+00',
        '  1.000000E+00 2.000000E+00',
        '  2.000000E+00 2.000000E+00',
        '  1.000000E+00 1.000000E+00',
        'END',
        'END',
        '',
    ])
