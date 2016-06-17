#!/bin/bash
docker run --rm -it -v $(pwd):/pandoc geometalab/pandoc bash -c "pandoc -t html5 documentation.md -o documentation.html; wkhtmltopdf --encoding 'utf-8' toc documentation.html documentation.pdf"
rm documentation.html
