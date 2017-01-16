#!/bin/bash

# Determine the dir this script is in with the one-liner from http://stackoverflow.com/a/246128/674064
# (CC-BY-SA 3.0, various contributors)
#
# This assumes this script is NOT called via a file symlink.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Generate the PDF
pushd $DIR
docker run --rm -it -v $(pwd)/..:/pandoc geometalab/pandoc bash -c "pandoc -t html5 osmaxx_data_schema.md -o osmaxx_data_schema.html && wkhtmltopdf --encoding 'utf-8' toc osmaxx_data_schema.html osmaxx_data_schema.pdf"
rm ../osmaxx_data_schema.html
popd
