"""Plot Radius evolution of different planet types, illustrating degeneracies
and potential for confusion among planet classes.
"""
import pickle
# import hzied_pipeline

from bioverse.constants import CONST

import paths
import numpy as np
import seaborn as sns

from matplotlib import pyplot as plt
import plotstyle
plotstyle.styleplots()

from matplotlib.ticker import ScalarFormatter
from scipy.interpolate import splrep, BSpline, interp1d


def interpolate_grid(t, R):
    tck = splrep(t, R, k=3)
    # t_fine = np.geomspace(min(t), max(t), 50)
    t_fine = np.linspace(min(t), max(t), 50)
    return 10 ** t_fine, BSpline(*tck)(t_fine)


def plot_radiuscomparison(sample, planets_args):
    dd = sample.to_pandas()
    d = dd.sample(min([len(dd), 4000]))
    mo = dd[dd.has_magmaocean].sample(min([len(dd[dd.has_magmaocean]), 4000]))

    fig, ax = plt.subplots()

    def interpolate_MR(df, colname):
        # interpolate M-R relation
        return interp1d(df.M, df[colname], kind='quadratic')

    M = np.linspace(0.33, 1.9, num=200)
    try:
        ax.plot(M, interpolate_MR(mo.sort_values('M'), 'R_steam')(M),
                lw=2., label='dry melt', c='xkcd:dark grey', ls='--')
    except AttributeError:
        pass
    ax.plot(M, interpolate_MR(mo.sort_values('M'), 'R')(M),
            lw=3., label='wet melt', c='C2')

    ax.plot(M, interpolate_MR(d.sort_values('M'), 'R_orig')(M),
            lw=3., label='non-\nrunaway', c='C0')

    ax.set_xlabel('$M_P \,[M_\oplus]$')
    ax.set_ylabel('$R_P \,[R_\oplus]$')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.annotate('$x_{{H_2O}}= ${}'.format(planets_args['wrr']), xy=(0.05, .9), xycoords='axes fraction')
    ax.set_xlim(right=2.24)
    ax.set_ylim(top=1.47)

    for y, lbl, c in zip([max(mo.R_steam) + 0.01, max(mo.R) - 0.04, max(d.R_orig) - 0.03],
                         ax.get_legend_handles_labels()[1], ['xkcd:dark grey', 'C2', 'C0']):
        ax.annotate(lbl, xy=(1.93, y), c=c, va='center')

    radius_change = np.average(mo.R / mo.R_orig) - 1
    # print('avg radius change of runaway GH planets: {:+.0f} %'.format(100 * radius_change))
    density_change = np.average(mo.rho / (CONST['rho_Earth'] * mo.M / mo.R_orig ** 3)) - 1
    # print('avg density change of runaway GH planets: {:+.0f} %'.format(100 * density_change))

    return fig, ax


def plot_planet_evo(N_time=9, v_offset=0.004, interpolate=False, **kwargs):
    fig, ax = plt.subplots()

    t = np.geomspace(1., 2000., N_time)
    R_noatm = [1. for t_ in t]
    R_hz = np.array([1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02])
    R_rgh_lo = np.array([1.135, 1.135, 1.135, 1.135, 1.02, 1.02, 1.02, 1.02, 1.02]) + v_offset
    R_rgh_hi = np.array([1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.02, 1.02])
    R_atmloss = np.array([1.125, 1.1, 1.075, 1.05, 1.025, 1.0, 1.0, 1.0, 1.0]) + v_offset
    R_subNeptune = np.array([1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25]) + v_offset
    c = ['k', 'C2', 'C1', 'C4', 'C3', 'C7']

    for R, col in zip([R_noatm, R_hz, R_rgh_lo, R_rgh_hi, R_atmloss, R_subNeptune],
                      c):
        # ax.plot(t, savgol_filter(R, window_length=7, polyorder=2, mode='nearest'), c=col, **kwargs)
        if interpolate:
            ax.plot(*interpolate_grid(np.log(t), R), c=col, **kwargs)
        else:
            ax.plot(t, R, c=col, **kwargs)

    ax.axhspan(.9, 1.05, alpha=.2)
    ax.text(400., .965, 'non-runaway GH', rotation=0, va='bottom',
            ha='center', c='C0', alpha=1., fontsize=15)
    ax.axhspan(1.12, 1.27, alpha=.2, color='C2')
    ax.text(400., 1.215, 'runaway GH', rotation=0, va='bottom',
            ha='center', c='C2', alpha=1., fontsize=15)

    def annotate(text, coords, color, **annotate_kwargs):
        ax.text(*coords, text, c=color, va='bottom', ha='left',
                fontsize=11, **annotate_kwargs)

    annotate('no atmosphere', (1.3, .975), 'k')
    annotate('Earth-like/dry', (1.3, 1.027), 'C2')
    annotate('atmospheric loss', (1.3, 1.053), 'C3', rotation=-23)
    annotate('runaway GH (low water)', (1.3, 1.148), 'C1')
    annotate('runaway GH (high water)', (1.3, 1.176), 'C4')
    annotate('sub-Neptune', (1.3, 1.229), 'xkcd:dark grey')

    ax.set_xscale('log')
    ax.spines[['right', 'top']].set_visible(False)
    ax.set_xlabel('Time [Myr]')
    ax.set_ylabel('Scaled planet radius R$_\mathrm{P}$/R$_\mathrm{0}$')
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.yaxis.set_ticks(np.arange(1., 1.4, 0.1))
    # ax.get_yaxis().set_major_formatter(FormatStrFormatter('%.2f'))

    return fig, ax

with open(paths.data / 'planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)
with open(paths.data / 'sample.pkl', 'rb') as f:
    sample = pickle.load(f)

fig, ax = plot_radiuscomparison(sample, planets_args)
fig.savefig(paths.figures / 'radiuscomparison.pdf')

fig, ax = plot_planet_evo(interpolate=False, lw=7.)
ax.set_xlim(1., 2000.)
ax.set_ylim(.955, 1.265)
fig.savefig(paths.figures / 'radiusevolution.pdf')
