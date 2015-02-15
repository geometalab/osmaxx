#!/bin/bash

export infile='planet-150202.osm.pbf'
export tmpdir='lsplitter-tmpdir' # directory for temporary "stripes"
export outdir='lsplitter-outdir' # directory for final tiles
parallel_options="-v --noswap"

doit1() {
	minlat=-90
	minlon=$1
	maxlat=90
	maxlon=$(($minlon+1))
	export TIMEFORMAT=%R # http://stackoverflow.com/a/3795634
	time ./osmconvert $infile -b="$minlon,$minlat,$maxlon,$maxlat" --out-pbf -o=$tmpdir/out_${minlon}.pbf --hash-memory=5000
}

doit2() {
	minlat=$1
	minlon=$2
	maxlat=$(($minlat+1))
	maxlon=$(($minlon+1))
	export TIMEFORMAT=%R # http://stackoverflow.com/a/3795634
	time ./osmconvert $tmpdir/out_${minlon}.pbf -b="$minlon,$minlat,$maxlon,$maxlat" --out-pbf -o=$outdir/out_${minlat}_${minlon}.pbf --hash-memory=5000
}

mkdir -p $outdir
mkdir -p $tmpdir

echo "Starting phase 1..."

export -f doit1 # see http://stackoverflow.com/a/26702789
time ./parallel $parallel_options doit1 ::: {-180..179} #minlon

echo "Starting phase 2..."

export -f doit2 # see http://stackoverflow.com/a/26702789
time ./parallel $parallel_options doit2 ::: {-90..89} ::: {-180..179} # minlat, minlon (changing this order will make things slower)
