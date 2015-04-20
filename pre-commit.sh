#!/bin/sh

echo
echo 'linting python3 code:'
echo '====================='
flake8 --max-line-length=119 source/
RC=$?
if [ $RC -ne 0 ]; then
  echo ' python code linting (flake8) failed!'
  exit 1
fi
