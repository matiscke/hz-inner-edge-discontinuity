""" Config file with my personal preference of default matplotlibrc settings.
"""
from matplotlib import rc, rcParams
from cycler import cycler


def get_color_palette():
    """ return a custom made color palette."""
    return ['#029e73', '#fc4f30', '#008fd5',
            '#e5ae38', '#810f7c', '#00035b', '#005249',
            '#8b8b8b', '#fe828c']


def styleplots():
    # Set plot style
    spinewidth = 1.8

    font = {'family': 'sans',
            'weight': 'normal',
            'size': 14}
    legend = {'handlelength': 0.75,
              'handletextpad': 0.5}
    figure = {'dpi': 100,
              'subplot.left': 0.16,  # the left side of the subplots of the figure
              'subplot.bottom': 0.21,  # the bottom of the subplots of the figure
              'subplot.right': 0.98,  # the right side of the subplots of the figure
              'subplot.top': 0.97,  # the top of the subplots of the figure
              'subplot.hspace': 0.0}  # height reserved for space between subplots

    rc('font', **font)
    rc('legend', **legend)
    rc('figure', **figure)
    rc('lines', linewidth=2.5)

    rc('axes', linewidth=spinewidth)
    rc('xtick.major', width=spinewidth)
    rc('ytick.major', width=spinewidth)
    rc('xtick.minor', width=.5 * spinewidth)
    rc('ytick.minor', width=.5 * spinewidth)
    rc('image', cmap='inferno')
    rc('hist', bins=20)
    rc('patch', edgecolor='black')
    rc('savefig', bbox='tight', dpi=200)

    rcParams['axes.prop_cycle'] = cycler(color=get_color_palette())


def set_size(width='aa', subplot=[1,1], scale=1):
    """ Set aesthetic figure dimensions to avoid scaling in latex.

    Parameters
    ----------
    width: float or string
        either width in pts or one of the following strings:
        'aa' : A&A column width
        'aaDouble' : A&A total text width
    subplot : list
        subplot dimensions in [rows, columns]
    scale: float
        fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
        Dimensions of figure in inches

    Credits
    -------
    Adapted from https://jwalton.info/Embed-Publication-Matplotlib-Latex/
    """
    aa_textwidth = 523.53       # textwidth of A&A template, as measured with "\the\textwidth" Latex command
    thesis_textwidth = 468.90   # measured in my PhD thesis
    if width == 'aaDouble':
        width_pt = aa_textwidth
    elif width == 'thesis':
        width_pt = thesis_textwidth
    else:
        width_pt = aa_textwidth/2

    # Width of figure
    fig_width_pt = width_pt * scale

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt

    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplot[0] / subplot[1])
    fig_dim = [fig_width_in, fig_height_in]

    return fig_dim


styleplots()
