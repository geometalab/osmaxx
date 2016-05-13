# osmaxx-docs
Documents from and about Osmaxx project.

These are the documents and resources to be expected here 2016:
* Data model of Osmaxx, i.e. a schema description ith tables, attributes/fields and values. 
* Point symbols in SVG format and as a symbol font (TTF).
* Config. file (osmaxx.json) to be listed as "Project" in taginfo web app
* Other related stuff

## Symbol Font Versioning

The major version of the font is part of the symbol font's font name and of the filename of the font's TTF file. Finer-grained versions are not part of these names. Font revisions of the same major version are backwards compatible: You can always replace an older revision with a newer revision within major version, without otherwise having to modify your symbolization. They aren't backwards compatible, though: Replacing a newer version with an older _may_ break a style, even if the major version of those revisions is the same.

### Compatible and incompatible changes

To ensure the above, incompatible changes require the major version to be bumped.

A new symbol font version is considered compatible to an old one, if ArcGIS and QGIS styles using the old version for displaying point features don't have to be changed when switching to the new version. This does **not imply** that a style using the new version can also use the old version without being modified, nor that the rendered result when using the new font version will look like the rendering did with the old font version.

Thus a compatible change is one that:
* doesn't technically break existing styles referencing codepoints in the font
* doesn't change the semantics of the codepoints

#### Examples of compatible symbol font changes

* adding a new symbol as a new glyph on a previously unused codepoint (by manually editing `osmaxx_v1_definition.yml`)
* aliasing an existing symbol as a new glyph on a previously unused codepoint
* changing the appearance of a symbol/glyph by modifying the respective `<path />` element in an SVG (as long as the old and new appearance capture the same semantics and are of sufficiently comparable size and shape to be used exchangably)
* changing the value of an `id` attribute of a `<path />` element in an SVG and adapting the references in `osmaxx_v1_definition.yml` accordingly

#### Examples of incompatible symbol font changes

* removing a symbol
* moving a symbol to a different codepoint, leaving the original codepoint unoccupied
* swap / reorder / sort symbols
* appearance changes unsuitable as drop-in replacements
* re-running `yaml_generator.py` after adding, removing or renaming SVG files
* re-running `yaml_generator.py` after certain edits to SVG files

Note that renaming SVG files and adapting references in `osmaxx_v1_definition.yml` accordingly will result in a compatible _font file_ revision but break styles that use and reference the SVG files directly.

### New major versions

If you must make an incompatible change, bump the major version. To do so edit `yaml_generator.py` and change the value of constant `FONT_MAJOR_VERSION`.

It is recommended that you then re-run `python3 yaml_generator.py` so that symbols occupy codepoints in alphabetical order of the symbol names again. If you don't, also edit the values for `filename` and `fontname` in `osmaxx_v1_definition.yml` to include the new version.

## Symbol Font Generation

The font-generation for OSMaxx can be found in `fontforge_font_creator`.

**This might live on a separate repository soonish, since this is not really documentation.**

Prerequisites:

* Docker
* Docker-Compose
* Python

Change to the directory `fontforge_font_creator`.

### Add/remove a symbol

To add a single Symbol, edit the `osmaxx_v1_definition.yml` manually and add a hex value below the existing ones,
best in ascending order (next higher number).

To remove a symbol, just delete the corresponding lines in the `osmaxx_v1_definition.yml`. Note that removal is an incompatible change that requires a new major version.

Then follow the instructions in section [Generating the font](#generating-the-font) below.

### Create initial SVG-to-Codepoint mapping YAML / move the entire symbols to another range

Doing this usually results in an incompatible change that requires a new major version. As long as feasible, prefer manual [compatible edits](#examples-of-compatible-symbol-font-changes) to `osmaxx_v1_definition.yml`.

1. Edit `yaml_generator.py` and set the (new) start_number, ie. `start_number = 0xE000` for the `user defined range`.
2. Run `python3 yaml_generator.py`

Then follow the instructions in section [Generating the font](#generating-the-font) below.

### Generating the font

Run 
```bash
docker-compose build
docker-compose run --rm fontforge
```

Open the generated font found in the `out` directory and check whether the symbols are placed correctly.

Once you are happy with the symbol font in `out/`, replace the current font with it:
```bash
mv out/OSMaxx_v*.ttf ../osmaxx-symbology/OSMaxx_point_symbols/
```

#### Modifying the SVG-to-Codepoint mapping
The `docker-compose build` step has to be **repeated** after modifying `osmaxx_v1_definition.yml` (whether by manual editing or running `yaml_generator.py`) if you want `docker-compose run --rm fontforge` to pick up the changes.

Changes in existing SVG files will be picked up regardless of whether the container was rebuilt. Note though, that changed SVG file names, changed `id` attribute values of `<path />` elements in SVGs and added or removed paths will usually require modifications to `osmaxx_v1_definition.yml` and thus also the subsequent container rebuilding.
