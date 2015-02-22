
Nice Python SVG tools on GitHub
--------------------------------

[SVGExport](https://github.com/developingo/SVGExport): color replacement and raster.
* uses xml.etree.ElementTree and Inkscape
* replaces one color with another (`string.replace()`)

[SVGPlease](https://github.com/sapal/svgplease): impressive command line grammar handling fill/stroke color changes, styles, text, tiling and even SVG diff/sum.


Softwares for graphists (with UI)
---------------------------------

[Inkscape](https://inkscape.org), with built-in [SVGClean plugin](http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG).

[SVG Cleaner](http://qt-apps.org/content/show.php/SVG+Cleaner?content=147974):
* Interview:  http://libregraphicsworld.org/blog/entry/introducing-svg-cleaner
* C++ reboot: http://libregraphicsworld.org/blog/entry/svg-cleaner-0.5-leaner-faster-runs-on-mac

[SVGOMG](https://jakearchibald.github.io/svgomg/) for "SVG Optimizer Missing GUI", an equivalent to SVG Cleaner but on-line, using Node-JS.

[Illustrator export options](http://creativedroplets.com/export-svg-for-the-web-with-illustrator-cc/): uncheck "Preserve Illustrator Editing Capabilities".

[Kylobyte SVG Challenge](http://johan.github.io/kilobyte-svg-challenge/): an open-source project to create SVG logo and promote SVG tools.


Raster SVG to PNG
------------------
* [ImageMagick](http://www.imagemagick.org/) "convert" command line
* [Inkscape command line](https://inkscape.org/doc/inkscape-man.html)
* RSVG command line
> On Unix systems, Cairo + librsvg, but said to have limitations rendering complex SVGs compared to...

Sources:
* http://stackoverflow.com/a/6599172/578783
* http://superuser.com/questions/516095/bake-an-svg-image-into-a-png-at-a-given-resolution


Pure SVG composition
---------------------

Flatten SVG transformations:
* https://github.com/petercollingridge/SVG-Optimiser
* http://petercollingridge.appspot.com/svg-transforms
* online version: http://petercollingridge.appspot.com/svg-optimiser

About XPath in SVG with Python ElementTree module and regular expressions
https://github.com/berteh/svg-objects-export/issues/9#issuecomment-74086171


About SVG viewport:
* http://sarasoueidan.com/blog/svg-coordinate-systems/

Ruby topic about SVG composition/overlay:
* https://www.ruby-forum.com/topic/129319

Nice PERL API to build SVG:
* http://search.cpan.org/~ronan/SVG-2.36/lib/SVG/Manual.pm#General_Steps_to_generating_an_SVG_document
* http://www.roitsystems.com/twiki/bin/view/SVG/SVGDataWidgets
* http://www.roitsystems.com/twiki/bin/view/SVG/WebAutoTrace


SVG tricks for the Web
-----------------------

[SVG stack](https://github.com/preciousforever/SVG-Stacker): SVG vector sprite sheets to embed multiple images in a single file.

SVG and responsive design:
* http://css-tricks.com/using-svg/
* http://benfrain.com/tips-for-using-svgs-in-web-projects/
* http://soqr.fr/testsvg/embed-svg-liquid-layout-responsive-web-design.php
