import os

import vcr

absolute_cassette_lib_path = os.path.join(os.path.dirname(__file__))

vcr_explicit_path = vcr.VCR(
    cassette_library_dir=absolute_cassette_lib_path,
)
