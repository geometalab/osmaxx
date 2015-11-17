#!/bin/bash

infile='../../conversion_service/file_size_estimation/planet-stats.csv'

print_error() {
	echo "ERROR: $1 Expected $2 but got ${3}. Issued command was: $4"
}

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile 8 47 9 48"
size_expected=83129952
size_actual=$($cmd)
if [[ "$size_actual" -ne "$size_expected" ]]; then
	print_error "Check for bbox exactly on 1x1 tile grid failed." $size_expected $size_actual "$cmd"
fi

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile 7.9999 46.9999 9.0001 48.0001"
size_expected=83151443
size_actual=$($cmd)
if [[ "$size_actual" -ne "$size_expected" ]]; then
	print_error "Check for bbox slightly larger than 1x1 tile grid failed." $size_expected $size_actual "$cmd"
fi

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile 8.0001 47.0001 8.9999 47.9999"
size_expected=83096704
size_actual=$($cmd)
if [[ "$size_actual" -ne "$size_expected" ]]; then
	print_error "Check for bbox slightly smaller than 1x1 tile grid failed." $size_expected $size_actual "$cmd"
fi

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile -44 -23 -43 -22"
size_expected=9607872
size_actual=$($cmd)
if [[ "$size_actual" -ne "$size_expected" ]]; then
	print_error "Check for bbox exactly on 1x1 tile grid with negative coordinates failed." $size_expected $size_actual "$cmd"
fi

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile 8 47 10 49"
size_expected=281910219 # 83129952 + 53702399 + 66375657 + 78702211
size_actual=$($cmd)
if [[ "$size_actual" -ne "$size_expected" ]]; then
	print_error "Check for bbox exactly on 2x2 tile grid failed." $size_expected $size_actual "$cmd"
fi

cmd="../../conversion_service/file_size_estimation/estimate_size.py $infile -90 -180 89 179"
size_expected='2373896947'
size_actual=$($cmd)
if [[ "$size_actual" == "$size_expected" ]]; then # can't do integer comparison here!
	print_error "Check for bbox covering the whole planet failed." $size_expected $size_actual "$cmd"
fi
