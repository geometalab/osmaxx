#!/usr/bin/env python
import sys
import os
from flake8.hooks import git_hook

COMPLEXITY = os.getenv('FLAKE8_COMPLEXITY', 10)
STRICT = os.getenv('FLAKE8_STRICT', True)
IGNORE = os.getenv('FLAKE8_IGNORE')
LAZY = os.getenv('FLAKE8_LAZY', False)


if __name__ == '__main__':
    sys.exit(git_hook(
        complexity=COMPLEXITY,
        strict=STRICT,
        ignore=IGNORE,
        lazy=LAZY,
        ))
