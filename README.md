Command line Python scripts to style, raster and compose (overlay) SVG image files.

## Change SVG files color
```bash
python svg_style_updater.py -i SVG_DIR -o OUTPUT_DIR --color red
```
`--color` can use any CSS-like format:
* hexadecimal (6 or 3 digits) like "#FF0000" or "#F00",
* [CSS color names](code/color_names.cfg) like "red",
* RGB strings like "rgb(255, 0, 0)".

`--match` specifies a color to replace.

`--rules` applies a list of style "match/set" rules, allowing to control not only fill colors but any SVG style attribute (stroke, stroke-width, opacity, etc.). Rules are provided with a JSON file like this:
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
The script will look for available renderers (ImageMagick/Inkscape). It does command line calls and deals with densities computing - espcially for ImageMagick. ImageMagick is faster, but Inkscape has a better support of SVG standard.
```bash
python svg_to_png.py -i SVG_DIR -o OUTPUT_DIR --width 92 --renderer inkscape --density xhdpi
```
`--density`, if provided, will use a [density configurations list](code/densities.json) to raster each file to all of these densities. This option was intended to output Android assets multiple resolutions.

`--renderer RENDERER_NAME` forces the use of a specific renderer.


## Compose (overlay) images over another
```bash
python compose_bitmap.py --background BACKGROUND_BITMAP -i OVERLAYS_FILES_DIR -o OUTPUT_DIR
```
Typical usage is to compose multiple icons over a same background.
For now, it works only with bitmaps over bitmap. Nice goal would be to handle SVG composition, with flattened transformations and single unit space.

 Some [notes](notes_about_svg.md) about what I found be interesting around SVG tools.
