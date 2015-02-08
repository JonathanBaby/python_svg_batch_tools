
About SVG with Python
----------------------

    "On Unix systems, Cairo + librsvg, but said to have limitations rendering complex SVGs compared to..."
    http://stackoverflow.com/a/6599172/578783

    PIL does not handle SVG.
    Python Imaging Library is unfortunately not well-supported on all Mac versions.
    http://stackoverflow.com/questions/2200742/python-default-common-way-to-read-png-images


github
-------

SVGExport - color replacement and raster
    https://github.com/developingo/SVGExport/blob/master/icons.py
    - uses xml.etree.ElementTree and Inkscape
    - replaces one color with another (string.replace())
    TODO: provide feedback

SVGPlease - changement de couleur, de style, de texte, et différentiel (pas de composition)
    https://github.com/sapal/svgplease


For graphists - tools with UI
------------------------------

    Inkscape built-in SVGClean plugin:
        http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG

    Open-source project to create SVG logo and promote SVG tools:
        http://johan.github.io/kilobyte-svg-challenge/

    SVG Cleaner: 
        Download:	http://qt-apps.org/content/show.php/SVG+Cleaner?content=147974
        Interview:  http://libregraphicsworld.org/blog/entry/introducing-svg-cleaner
        C++ reboot: http://libregraphicsworld.org/blog/entry/svg-cleaner-0.5-leaner-faster-runs-on-mac

    Illustrator export options:
        http://creativedroplets.com/export-svg-for-the-web-with-illustrator-cc/
        IMPORTANT: uncheck "Preserve Illustrator Editing Capabilities"


Raster to PNG
-----------------------
    ImageMagick
        ImageMagick "convert" command line
        "Wand" library: http://docs.wand-py.org/en/0.3.8/
        
    Inkscape command line

    RSVG command line

Threads:
    http://superuser.com/questions/516095/bake-an-svg-image-into-a-png-at-a-given-resolution


Pure SVG composition
---------------------
    Flatten SVG transformations:
        https://github.com/petercollingridge/SVG-Optimiser
        http://petercollingridge.appspot.com/svg-transforms
        online version: http://petercollingridge.appspot.com/svg-optimiser

    About SVG viewport:
        http://sarasoueidan.com/blog/svg-coordinate-systems/

    Ruby topic about SVG composition/overlay:
        https://www.ruby-forum.com/topic/129319

    Nice PERL API to build SVG:
        http://search.cpan.org/~ronan/SVG-2.36/lib/SVG/Manual.pm#General_Steps_to_generating_an_SVG_document
        http://www.roitsystems.com/twiki/bin/view/SVG/SVGDataWidgets
        http://www.roitsystems.com/twiki/bin/view/SVG/WebAutoTrace


SVG tricks for the Web
-----------------------

    SVG stack - SVG vector sprite sheets to embeb multiple image in a single file
        https://github.com/preciousforever/SVG-Stacker

    SVG and responsive design:
        http://css-tricks.com/using-svg/
        http://benfrain.com/tips-for-using-svgs-in-web-projects/
        http://soqr.fr/testsvg/embed-svg-liquid-layout-responsive-web-design.php
