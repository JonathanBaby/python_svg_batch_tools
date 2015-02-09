Command line scripts to style, raster and compose (overlay) Scalable Vector Graphics. Batch processing.

## Change SVG files color
```bash
python svg_style_updater.py -i SVG_DIR -o OUTPUT_DIR --color red
```
`--color` accepts different formats:
* hexadecimal strings like "#FF0000" or "#F00",
* "rgb" strings like "rgb(255, 0, 0)",
* [color names](code/color_names.cfg) like "red".

`--match` specifies a color to replace.

`--rules` applies a list of "match/set" rules to update any SVG style attribute (stroke, stroke-width, opacity, etc.). Rules are described with a JSON file:
 ```javascript
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


## Raster SVG files to PNG
```bash
python svg_to_png.py -i SVG_DIR -o OUTPUT_DIR --width 92
```
The script looks for the available renderers, deals with densities and performs command line calls.
```bash
python svg_to_png.py -i SVG_DIR -o OUTPUT_DIR --width 92 --renderer inkscape --density xhdpi
```
`--density` specifies the density associated with the given size and rasters each file to a [list of densities](code/densities.json). It was intended to output Android assets multiple resolutions.

`--renderer` forces the use of a specific renderer. ImageMagick is faster, but Inkscape has a better support of SVG standard.


## Compose (overlay) images over another
```bash
python compose_bitmap.py --background BACKGROUND_BITMAP -i OVERLAYS_DIR -o OUTPUT_DIR
```
Typical usage is to compose multiple icons over a same background. For now, it works only with bitmaps. A nice improvement would be to handle SVG composition.

 Further: [notes about interesting SVG tools](doc/notes_about_svg.md).
