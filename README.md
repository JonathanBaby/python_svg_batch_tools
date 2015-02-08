Command line Python scripts to style, raster and compose (overlay) SVG image files.

#### Change color of SVG files
```bash
python svg_style_updater.py -i SVG_FILES_DIR -o OUTPUT_DIR --color red
```
`--color` can use any CSS-like format:
* [CSS color names](code/color_names.htm) like "red",
* hexadecimal (6 or 3 digits) like "#FF0000" or "#F00",
* or RGB strings like "rgb(255, 0, 0)".
`--match` option specifies a color to replace
`--rules` option applies a list of style "match/set" rules, allowing to control not only fill colors but any SVG style attribute (stroke, stroke-width, opacity, etc.). Rules are provided with a JSON file like this:
 ```json
 [
{
    "match":"fill:none",
    "set":"fill:#ff0000;fill-opacity:0.5",
    "name":"Replace black or empty with semi-transparent red."
},
{
    "match":"fill:#00ffff",
    "set":"fill:#ff00ff;stroke:#00ff00;stroke-opacity:1;stroke-width:25;",
    "name":"Replace cyan with magenta, and add a green stroke."
}
]
 ```

#### Raster SVG files to PNG (and handle Android densities)
```bash
python svg_to_png.py -i SVG_FILES_DIR -o OUTPUT_DIR --width 200
```
The script will actually look for the available renderers, either ImageMagick or Inkscape.
It simply calls their command line interfaces and deals with the density computing (specifically for ImageMagick). Note ImageMagick is faster, but Inkscape has a better support of SVG standard. To force the one of these renderer, use the `--renderer` option.
```bash
python svg_to_png.py -i SVG_FILES_DIR -o OUTPUT_DIR --width 200 --renderer inkscape --density xxhdpi
```
`--density`, if provided, will use a [density configurations list](code/densities.json) to raster each file to all of these densities. This option was intended to output Android assets multiple resolutions.

#### Batch compose (overlay) a list of images over an other
```bash
python compose_bitmap.py --background BACKGROUND_BITMAP -i OVERLAYS_FILES_DIR -o OUTPUT_DIR
```
Purpose of this script is to compose multiple icons over a same background.
Currently works only for bitmaps over bitmap, but ultimate goal would be to handle pure SVG composition, with flattened transformations and uniform space units.

 For a lot of great things I came across writing these tiny scripts, see these [notes](notes_about_svg.md) and the various todos left in sources.
