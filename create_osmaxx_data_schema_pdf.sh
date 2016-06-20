#!/bin/bash
docker run --rm -it -v $(pwd):/pandoc geometalab/pandoc bash -c "pandoc -t html5 osmaxx_data_schema.md -o osmaxx_data_schema.html && wkhtmltopdf --encoding 'utf-8' toc osmaxx_data_schema.html osmaxx_data_schema.pdf"
rm osmaxx_data_schema.html
