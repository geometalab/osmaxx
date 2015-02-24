#!/bin/bash

parallel_options="-k -j50% --noswap" # number of parallel instances = 50 * number of cores, less if swapping occurs (50 proved itself to be a good number in a quick benchmark)

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

export indir=$1
outfile=$2

process() {
	minlat=$1
	minlon=$2
	infile=$indir/out_${minlat}_${minlon}.pbf
	filesize=$(stat -c '%s' $infile)
	stats=$(./osmconvert $infile --out-statistics)
	nodes=$(echo "$stats"     | grep 'nodes: '     | sed -e 's!.*: \(.*\)!\1!')
	ways=$(echo "$stats"      | grep 'ways: '      | sed -e 's!.*: \(.*\)!\1!')
	relations=$(echo "$stats" | grep 'relations: ' | sed -e 's!.*: \(.*\)!\1!')
	echo "$minlat,$minlon,$filesize,$nodes,$ways,$relations"
}

ulimit -n 3000 # increase the allowed number of open files
export -f process # make function available to GNU parallel
time ./parallel $parallel_options process ::: {-90..89} ::: {-180..179} > $outfile # minlat, minlon
