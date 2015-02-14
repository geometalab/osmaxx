#!/bin/bash

parallel_options="-k -j50% --noswap"

if [[ $# -ne 2 ]]; then
	echo "Usage: $0 directory/with/pbffiles/ outfile"
	exit
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

process() {
	indir=$1
	minlat=$2
	minlon=$3
	infile=$indir/out_${minlat}_${minlon}.pbf
	filesize=$(stat -c '%s' $infile)
	stats=$(./osmconvert $infile --out-statistics)
	nodes=$(echo "$stats"     | grep 'nodes: '     | sed -e 's!.*: \(.*\)!\1!')
	ways=$(echo "$stats"      | grep 'ways: '      | sed -e 's!.*: \(.*\)!\1!')
	relations=$(echo "$stats" | grep 'relations: ' | sed -e 's!.*: \(.*\)!\1!')
	echo "$minlat,$minlon,$filesize,$nodes,$ways,$relations"
}

ulimit -n 3000 # increase the allowed number of open files
export -f process
time ./parallel $parallel_options process $indir ::: {-90..89} ::: {-180..179} > $outfile # minlat, minlon
