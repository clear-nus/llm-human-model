#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
from colors import *

def configure_fonts(fontsize=15, legend_fontsize=8,
                      usetex=False, figure_dpi=300):
    """
    Configure fonts. Fonts are set to serif .
    @param fontsize The size of the fonts used on the axis and within the figure
    @param legend_fontsize The size of the legend fonts
    @param usetex If true, configure to use latex for formatting all text
    @param figure_dpi Set the dots per inch for any saved version of the plot
    """
    plt.rcParams.update({
            'font.family':'sans-serif',
            'font.serif':'Computer Modern Roman',
            'font.size': fontsize,
            'legend.fontsize': legend_fontsize,
            'legend.labelspacing': 0,
            'text.usetex': usetex,
            'savefig.dpi': figure_dpi
    })


def shaded_error(ax, xvals, yvals, errs, color=None):
    """
    Draw a shaded region describing the error. 
    @param ax The axis to draw the region on
    @param xvals The xvals of the data
    @param yvals The yvals of the data (should be same length as xvals)
    @param errs The errors for each data point (should be same length as xvals)
       For each point, a shaded region is draw between the yvals - errs and yvals + errs
    @param color A string describing the color to draw the shaded region (i.e. 'grey')
       The colors.py script will be used to convert this to a color code
    """
    ax.fill_between(xvals, yvals - errs, yvals + errs,
                    where = numpy.isfinite(errs),
                    facecolor = color,
                    edgecolor = 'none',
                    alpha=1.0)
    
    
def simplify_axis(ax, xbottom=True, xtop=False,  yleft=True, yright=False):
    """
    Remove white spacing from axis. Make lines around axis bold.
    @param ax The axis to simplify
    @param xbottom If true, draw the bottom axis - otherwise remove the line
    @param xtop If true, draw the top axis - otherwise remove the lin
    @param yleft If true, draw the left axis - otherwise remove the line
    @param yright If true, draw the right axis - otherwise remove the line
    """

    ax.set_frame_on(False)
    xmin, xmax = ax.get_xaxis().get_view_interval()
    ymin, ymax = ax.get_yaxis().get_view_interval()

    if yleft:
        ax.add_artist(plt.Line2D((xmin, xmin), (ymin, ymax), 
                                   color='black', linewidth=1, 
                                   zorder=100, clip_on=False))
        ax.get_yaxis().tick_left()

    if yright:
        ax.add_artist(plt.Line2D((xmax, xmax), (ymin, ymax), 
                                   color='black', linewidth=1, 
                                   zorder=100, clip_on=False))
        ax.get_yaxis().tick_right()

    if yleft and yright:
        ax.get_yaxis().set_ticks_position('both')

    if xbottom:
        ax.add_artist(plt.Line2D((xmin, xmax), (ymin, ymin), 
                                   color='black', linewidth=1, 
                                   zorder=100, clip_on=False))
        ax.get_xaxis().tick_bottom()

    if xtop:
        ax.add_artist(plt.Line2D((xmin, xmax), (ymax, ymax), 
                                   color='black', linewidth=1, 
                                   zorder=100, clip_on=False))
        ax.get_xaxis().tick_top()

    if xbottom and xtop:
        ax.get_xaxis().set_ticks_position('both')


def output(fig, path, size, fontsize=8, legend_fontsize=8, latex=True):
    """
    Save the figure.
    @param fig The figure to save
    @param path The output path to write the figure to 
       (if None, figure not saved, just rendered to screen)
    @param size The size of the output figure
    @param fontsize The size of the font
    @param legend_fontsize The size of the legend font
    @param latex If true, use latex to render the text in the figure
    """
    if path is not None:
        configure_fonts(fontsize=fontsize, legend_fontsize=legend_fontsize,
                        usetex=latex)
        fig.set_size_inches(size)
        fig.savefig(path, pad_inches=0.02, bbox_inches='tight')
    else:
        plt.show()
