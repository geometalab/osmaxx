# Osmaxx

## Explanation for scripts in `src/`

### `lsplitter.sh`

This script will read an OSM planet file in .pbf format. The programm works in two steps:

1. Cutting the input file in a series of "stripes", spaced by 1 degree, along meridians.
2. Cutting the "stripes" in parallels to the equator therefore creating tiles with a size of 1 degree by 1 degree.

The results of the first step will be saved into the directory specified by `$tmpdir`. The results of the second step will be saved into the directory specified by `$outdir`.

Input file, $tmpdir and $outdir are hardcoded at the beginning of the file.

### `generate_stats.sh`

This script will read the output of `lsplitter.sh` (the content of the $outdir directory) and generate a single statistics file in .csv format about each of the encountered `180*360=64800` tiles.

The order of the entries is as follows:

- Soutern-most possible latitude for this tile
- Western-most possible longitude for this tile
- Filesize in .pbf format in bytes
- Number of OSM nodes
- Number of OSM ways
- Number of OSM relations

The separating character is a comma (,).

Input parameters are:

1. Path to the outdir directory of `lsplitter.sh`.
2. Name of the output file

### `estimate_size.py`

This script estimates the size of a .pbf extract of the OSM planet along a given bounding box by reading the output of `generate_stats.sh`.

The input parameters are:

- Path to the .csv output file of `generate_stats.sh`.
- Minimum longitude of the bounding box
- Minimum latitude of the bounding box
- Maximum longitude of the bounding box
- Maximum latitude of the bounding box

The estimation is done by checking for each tile what fraction of each tile the bbox covers and multiplying that value with the tile's size.

The size estimate is given in bytes.

### Requirements

The scripts `lsplitter.sh` and `generate_stats.sh` require GNU parallel (https://www.gnu.org/software/parallel/) and a compiled version of osmconvert (http://wiki.openstreetmap.org/wiki/Osmconvert). To avoid the need of having these tools installed by an administrator with root privileges, one can compile them locally (osmconvert) or just copy the Perl file (GNU parallel) in the same directory as the other scripts. The aforementioned scripts are programmed in such a way that they will use these local versions (by calling e.g. `./parallel` instead of `parallel`).
