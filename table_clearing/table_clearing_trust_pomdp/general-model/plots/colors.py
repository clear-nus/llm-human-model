#!/usr/bin/env python
import logging
logger = logging.getLogger('ss_plotting')

SHADE = 'shade'
STANDARD = 'standard'
EMPHASIS = 'emphasis'

color_library = {}


BLUE = 'blue_1'

color_library[BLUE] = {}
#color_library[BLUE][SHADE] = '#deebf7'

color_library[BLUE][SHADE] = '#ffffff'
color_library[BLUE][STANDARD] = '#000033'
color_library[BLUE][EMPHASIS]='#3182bd'

BLUE = 'blue_2'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#000099'
color_library[BLUE][EMPHASIS]='#3182bd'


BLUE = 'blue_3'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#0000ff'
color_library[BLUE][EMPHASIS]='#3182bd'


BLUE = 'blue_4'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#6600ff'
color_library[BLUE][EMPHASIS]='#3182bd'


BLUE = 'blue_5'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#bb00ff'
color_library[BLUE][EMPHASIS]='#3182bd'

BLUE = 'blue_5b'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#abddff'
color_library[BLUE][EMPHASIS]='#3182bd'



BLUE = 'blue_6'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#bbddff'
color_library[BLUE][EMPHASIS]='#3182bd'


TEAL = 'teal'
color_library[TEAL] = {}
color_library[TEAL][SHADE] = '#deebf7'
color_library[TEAL][STANDARD] = '#008080'
color_library[TEAL][EMPHASIS]='#3182bd'


TEAL = 'teal2'
color_library[TEAL] = {}
color_library[TEAL][SHADE] = '#deebf7'
color_library[TEAL][STANDARD] = '#bb8080'
color_library[TEAL][EMPHASIS]='#3182bd'


TEAL = 'teal3'
color_library[TEAL] = {}
color_library[TEAL][SHADE] = '#deebf7'
color_library[TEAL][STANDARD] = '#ee8080'
color_library[TEAL][EMPHASIS]='#3182bd'

TEAL = 'teal4'
color_library[TEAL] = {}
color_library[TEAL][SHADE] = '#deebf7'
color_library[TEAL][STANDARD] = '#ff80aa'
color_library[TEAL][EMPHASIS]='#3182bd'

BLUE = 'blue'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#0000ff'
color_library[BLUE][EMPHASIS]='#3182bd'

BLUE = 'steel_blue'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#4682B4'
color_library[BLUE][EMPHASIS]='#3182bd'

BLUE = 'bleudefrance'
color_library[BLUE] = {}
color_library[BLUE][SHADE] = '#deebf7'
color_library[BLUE][STANDARD] = '#318CE7'
color_library[BLUE][EMPHASIS]='#3182bd'

APRICOT = 'apricot'
color_library[APRICOT] = {}
color_library[APRICOT][SHADE] = '#deebf7'
color_library[APRICOT][STANDARD] = '#FBCEB1'
color_library[APRICOT][EMPHASIS]='#3182bd'

APRICOT = 'bittersweet'
color_library[APRICOT] = {}
color_library[APRICOT][SHADE] = '#deebf7'
color_library[APRICOT][STANDARD] = '#FE6F5E'
color_library[APRICOT][EMPHASIS]='#3182bd'

# Orange
ORANGE = 'orange'
color_library[ORANGE]={}
color_library[ORANGE][SHADE]='#fee6ce'
color_library[ORANGE][STANDARD]='#FF7F00'
color_library[ORANGE][EMPHASIS]='#e6550d'

# Magentas
MAGENTA = 'magenta'
color_library[MAGENTA]={}
color_library[MAGENTA][SHADE]='#efedf5'
color_library[MAGENTA][STANDARD]='#ff00ff'
color_library[MAGENTA][EMPHASIS]='#756bb1'

# Green
GREEN = 'green'
color_library[GREEN]={}
color_library[GREEN][SHADE]='#e5f5e0'
color_library[GREEN][STANDARD]='#a1d99b'
color_library[GREEN][EMPHASIS]='#31a354'

# Green
GREEN = 'true_green'
color_library[GREEN]={}
color_library[GREEN][SHADE]='#e5f5e0'
color_library[GREEN][STANDARD]='#00ff00'
color_library[GREEN][EMPHASIS]='#31a354'

# GREY
GREY = 'grey'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#bdbdbd"
color_library[GREY][EMPHASIS]="#636363"

#GREY shades
GREY = 'grey1'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#111111"
color_library[GREY][EMPHASIS]="#636363"

GREY = 'grey2'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#663333"
color_library[GREY][EMPHASIS]="#636363"

GREY = 'grey3'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#995555"
color_library[GREY][EMPHASIS]="#636363"

GREY = 'grey4'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#aa7777"
color_library[GREY][EMPHASIS]="#636363"


GREY = 'grey5'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#cc9999"
color_library[GREY][EMPHASIS]="#636363"

GREY = 'grey6'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#eebbbb"
color_library[GREY][EMPHASIS]="#636363"

GREY = 'grey7'
color_library[GREY]={}
color_library[GREY][SHADE]="#f0f0f0"
color_library[GREY][STANDARD]="#ffbbee"
color_library[GREY][EMPHASIS]="#636363"

# RED
RED = 'red'
color_library[RED]={}
color_library[RED][SHADE]="#fee0d2"
color_library[RED][STANDARD]="#fc9272"
color_library[RED][EMPHASIS]="#de2d26"


# RED
RED = 'true_red'
color_library[RED]={}
color_library[RED][SHADE]="#fee0d2"
color_library[RED][STANDARD]="#ff0000"
color_library[RED][EMPHASIS]="#de2d26"

# PINK
PINK = 'white'
color_library[PINK]={}
color_library[PINK][SHADE]="#fde0dd"
color_library[PINK][STANDARD]="#ffffff"
color_library[PINK][EMPHASIS]="#c51b8a"

# PINK
PINK = 'pink'
color_library[PINK]={}
color_library[PINK][SHADE]="#fde0dd"
color_library[PINK][STANDARD]="#fa9fb5"
color_library[PINK][EMPHASIS]="#c51b8a"

PURPLE = 'purple'
color_library[PURPLE]={}
color_library[PURPLE][SHADE]="#fde0dd"
color_library[PURPLE][STANDARD]="#beafd3"
color_library[PURPLE][EMPHASIS]="#c51b8a"

def get_plot_color(color=None, emphasis=False):
    """
    Returns color data for the requested color.
    @param color A string describing the general color (i.e. 'blue')
    @param emphasis If true, return a bold version of the color, 
        otherwise return a standard
    @return A hex code for the color. This can be passed directly
        to most matplotlib commands.
    """
    if not isinstance(color, basestring):
        return [ float(c) / 255. if isinstance(c, int) else c for c in color ]

    try:
        color_data = color_library[color]
    except KeyError, e:
        default_color = GREY
        color_data = color_library[default_color]
        logger.warn('Failed to find color %s in library. Returning %s.' % (color, default_color))

    if emphasis:
        return color_data[EMPHASIS]
    else:
        return color_data[STANDARD]
        

def get_shade_color(color=None):
    """
    Returns a color code for a light shade of the requested color
    @param color A string describing the general color (i.e. 'blue')
    @return A hex code for the color. This can be passed directly
        to most matplotlib commands.
    """

    try:
        color_data = color_library[color]
    except KeyError, e:
        default_color = GREY
        color_data = color_library[default_color]
        logger.warn('Failed to find color %s in library. Returning %s.' % (color, default_color))

    return color_data[SHADE]
