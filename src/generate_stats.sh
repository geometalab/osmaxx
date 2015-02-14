#!/bin/bash

if [[ $# -ne 2 ]]; then
	echo "Usage: $0 directory/with/pbffiles/ outfile"
fi

if [[ ! -d $1 ]]; then
	echo "ERROR: $1 is not a directory."
	exit 1
fi

if [[ -e $2 ]]; then
	echo "ERROR: $2 exists."
	exit 2
fi

indir=$1
outfile=$2

for lat in {-90..89}; do
	for lon in {-180..179}; do
		infile=$indir/out_${lat}_${lon}.pbf
		filesize=$(stat -c '%s' $infile)
		stats=$(./osmconvert $infile --out-statistics)
		nodes=$(echo "$stats"     | grep 'nodes: '     | sed -e 's!.*: \(.*\)!\1!')
		ways=$(echo "$stats"      | grep 'ways: '      | sed -e 's!.*: \(.*\)!\1!')
		relations=$(echo "$stats" | grep 'relations: ' | sed -e 's!.*: \(.*\)!\1!')
		echo "$lat,$lon,$filesize,$nodes,$ways,$relations" >> $outfile
	done
done
