# osmaxx-docs
Documents from and about Osmaxx project.

These are the documents and resources to be expected here 2016:
* Data model of Osmaxx, i.e. a schema description ith tables, attributes/fields and values. 
* Point symbols in SVG format and as a symbol font (TTF).
* Config. file (osmaxx.json) to be listed as "Project" in taginfo web app
* Other related stuff


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

To remove a symbol, just delete the corresponding lines in the `osmaxx_v1_definition.yml`. 

Then follow the instructions in section [Generating the font](#generating-the-font) below.

### Create initial yml/move the entire symbols to another range

1. Edit `yaml_generator.py` and set the (new) start_number, ie. `start_number = 0xE000` for the `user defined range`.
2. Run `python3 yaml_generator.py`

Then follow the instructions in section [Generating the font](#generating-the-font) below.

### Generating the font

Run 
```
docker-compose build
docker-compose run --rm
```

Open the generated font found in the `out` directory and check whether the symbols are placed correctly.
