"""Plot prototypical detection in an optimistic survey"""

import pickle
import paths
import numpy as np
import matplotlib.pyplot as plt

import plotstyle
plotstyle.styleplots()

from bioverse.util import S2a_eff
from bioverse.hypothesis import magma_ocean_hypo

def plot_survey(data, results, planets_args, parameter_of_interest='R', show_rolling_mean=True, show_binned_stats=False):
    yvar = parameter_of_interest
    xvar = 'S_abs'
    # yvar = 'R'

    fig, ax = plt.subplots()
    ax.scatter(data[xvar], data[yvar], s=2, c='k')
    ax.errorbar(data[xvar], data[yvar], xerr=data.error[xvar], yerr=data.error[yvar], fmt='o', ms=2., elinewidth=1,
                color='k', alpha=.5, label='measured')

    if show_binned_stats:
        # means, edges, n, std = binned_stats(data, xvar, yvar, np.geomspace(np.min(data[xvar]),
        # np.max(data[xvar]), num=12), statistic='mean')
        # ax.errorbar(edges[:-1]+(edges[1:]-edges[:-1])/2, means, xerr=(edges[1:]-edges[:-1])/2,
        # yerr=None, fmt='none', color='C2', label='binned {} statistic'.format(yvar), elinewidth=2.5)
        binned_avg = data[yvar + '_mean_binned']
        ax.plot(data[xvar], binned_avg, color='C2', label='binned average')
        std = data.error[yvar + '_mean_binned']
        ax.fill_between(data.sort_by('S_abs')['S_abs'], (binned_avg - std),
                        (binned_avg + std), color='C2', alpha=.3)

    # overplot samples from the posterior
    nburn = 100
    sampler_results = results['sampler_results']
    posterior_sample = sampler_results.samples[nburn::300]

    S_grid = np.geomspace(10., 2000., 300)
    a_eff_grid = S2a_eff(S_grid)

    colors = plt.cm.OrRd(np.linspace(0, 1, len(posterior_sample)))
    for i, s in enumerate(posterior_sample):
        P_magma = magma_ocean_hypo((s[0], s[1], s[2], s[3]), a_eff_grid,
                                   gh_increase=planets_args['gh_increase'], water_incorp=planets_args['water_incorp'],
                                   simplified=planets_args['simplified'], parameter_of_interest=parameter_of_interest)
        ax.plot(S_grid, P_magma,
                c=colors[i],
                # c='k',
                alpha=.5, lw=1.)
    ax.plot(S_grid, P_magma,
            c=colors[i],
            #         # c='k',
            alpha=.63, lw=1., label='posterior draws')

    ax.set_xscale('log')
    # ax.set_yscale('log')
    if xvar == 'S_abs':
        ax.set_xlabel('Net instellation [$\mathrm{W/m^2}$]')
        ax.axvline(planets_args['S_thresh'], ls='-.', c='gray', alpha=.33)
        ax.invert_xaxis()
    if yvar == 'R':
        ax.set_ylabel('Planet radius [R$_\oplus$]')
    elif yvar == 'rho':
        ax.set_ylabel('bulk density(g/cm3)')

    if show_rolling_mean:
        # add confidence interval of rolling mean radius
        mean = data.sort_by('S_abs')[parameter_of_interest + '_mean']
        sem = data.error.sort_by('S_abs')[parameter_of_interest + '_mean']
        ax.plot(data.sort_by('S_abs')['S_abs'], mean,
                color='C2', lw=1)
        ax.fill_between(data.sort_by('S_abs')['S_abs'], (mean - sem),
                        (mean + sem), color='C2', alpha=.3, label='moving average')

    ax.set_title('Optimistic survey ({} planets)'.format(len(data)), y=1.15, fontsize=14)
    fig.legend(fontsize=12, loc='lower left', ncol=99, bbox_to_anchor=(0.15, .97),
               frameon=False, columnspacing=1.6)

    # ax.axhline(0.98, color='C2', ls='--', label='mean')

    ax.set_xlim(2000, 50.)
    ax.set_ylim(0.75, 1.4)
    # ax.set_ylim(1.8, 5.)
    return fig, ax



with open(paths.data / 'pipeline/data.pkl', 'rb') as f:
    data = pickle.load(f)
with open(paths.data / 'pipeline/results_opt.pkl', 'rb') as f:
    results_opt = pickle.load(f)
with open(paths.data / 'pipeline/planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)


fig, ax = plot_survey(data, results_opt, planets_args, parameter_of_interest='R', show_rolling_mean=True, show_binned_stats=False)
fig.savefig(paths.figures / 'optimistic_R-S.pdf')