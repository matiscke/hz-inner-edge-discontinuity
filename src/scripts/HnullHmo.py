""" Plot sub- and super-runaway planets in the sample and the corresponding hypotheses in instellation-radius space."""

import pickle
import paths
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from bioverse.hypothesis import magma_ocean_hypo, magma_ocean_f0
from bioverse.util import S2a_eff, a_eff2S
from bioverse.constants import CONST

import plotstyle
plotstyle.styleplots()


def plot_transitingplanets(sample, planets_args, ax, parameter_of_interest='R'):
    """ Make a scatter plot highlighting the transiting planets.

    Parameters
    ----------
    sample : Bioverse Table or pandas DataFrame
        Table with the synthetic sample
    planets_args : dict
        arguments for planet sample creation with Bioverse
    ax : matplotlib axis object
    parameter_of_interest : str
        y-axis parameter to plot. Either 'R' or 'rho'.

    Returns
    -------
    ax : matplotlib axis object
        the axis with the plot
    """
    yvar = parameter_of_interest

    try:
        sampledf = sample.to_pandas()
    except AttributeError:
        sampledf = sample
    ax.scatter(sampledf[sampledf.transiting == False].S_abs, sampledf[sampledf.transiting == False][yvar], s=.3,
               c='dimgray', alpha=.5, label='synthetic\nplanets')

    # transiting planets
    # sc = ax.scatter(sampledf[sampledf.transiting == True].S_abs, sampledf[sampledf.transiting == True][yvar], s=20,
    #            marker='x', c=np.where(sampledf[sampledf.transiting == True].has_magmaocean, 'C2', 'C0'), label='transiting')
    ax.scatter(sampledf[(sampledf.transiting) & ~(sampledf.has_magmaocean)].S_abs, sampledf[(sampledf.transiting) & ~(sampledf.has_magmaocean)][yvar], s=50,
                    marker='X', c='C0', edgecolors='k', linewidth=1.25, label='transiting')
    ax.scatter(sampledf[(sampledf.transiting) & (sampledf.has_magmaocean)].S_abs, sampledf[(sampledf.transiting) & (sampledf.has_magmaocean)][yvar], s=50,
                    marker='X', c='C2', edgecolors='k', linewidth=1.25, label='transiting, RGH')

    # show differences in radius due to magma ocean
    if yvar == 'R':
        X_coords = np.array([sampledf[sampledf.transiting == True].S_abs, sampledf[sampledf.transiting == True].S_abs])
        Y_coords = np.array([sampledf[sampledf.transiting == True].R_orig, sampledf[sampledf.transiting == True].R])
        ax.plot(X_coords, Y_coords, c='gray', lw=1.5, alpha=.5, zorder=-1)

        for i in range(len(sampledf[sampledf.transiting == True])):
            if Y_coords[1][i] != Y_coords[0][i]:
                ax.annotate(
                    "",
                    xy=(X_coords[0][i], Y_coords[1][i]), xytext=(0, -1.),  # xytext=(0., Y_coords[1][i]),
                    textcoords='offset points', ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', alpha=0.5),
                    arrowprops=dict(arrowstyle='-', connectionstyle='arc3,rad=0', alpha=.5, lw=1.5),
                    zorder=-9
                )

        ax.set_ylabel('Radius [$R_\oplus$]')
    elif yvar == 'rho':
        ax.set_ylabel('bulk density [$\mathrm{g/cm^3}$]')

    ax.set_xlabel('Instellation [$\mathrm{W/m^2}$]')
    ax.set_xscale('log')
    # ax.legend(loc='lower left', ncol=3, bbox_to_anchor=(0.0, 1.),
    #           frameon=False, columnspacing=1.6)

    ax.invert_xaxis()
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    return ax


def plot_HnullHmo(sample, planets_args, ax, parameter_of_interest='R', f_dR=None):
    """Produce a plot showing the null hypothesis and the magma ocean hypothesis.

    Parameters
    ----------
    sample : Bioverse Table or pandas DataFrame
        Table with the synthetic sample
    planets_args : dict
        arguments for planet sample creation with Bioverse
    ax : matplotlib axis object
    parameter_of_interest : str
        y-axis parameter to plot. Either 'R' or 'rho'.

    Returns
    -------
    ax : matplotlib axis object
        the axis with the plot
    """

    S_grid = np.linspace(30., 2000., 250)
    a_eff_grid = S2a_eff(S_grid)

    R_avg_out = np.average(sample['R'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting']])

    rho_avg_out = np.average(CONST['rho_Earth'] * sample['M'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting']] /
                             (sample['R'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting']]) ** 3)

    try:
        dd = sample.to_pandas()
    except AttributeError:
        dd = sample
    mo = dd[dd.has_magmaocean]


    if parameter_of_interest == 'R':
        # compute radius change
        radius_change = np.average(mo.R / mo.R_orig) - 1
        P_magma = magma_ocean_hypo((planets_args['S_thresh'], planets_args['wrr'], planets_args['f_rgh'], R_avg_out), a_eff_grid,
                                   gh_increase=planets_args['gh_increase'], water_incorp=planets_args['water_incorp'],
                                   simplified=planets_args['simplified'], diff_frac=radius_change,
                                   parameter_of_interest=parameter_of_interest, f_dR=f_dR)

        P0 = magma_ocean_f0(R_avg_out, a_eff_grid)

    elif parameter_of_interest == 'rho':
        # compute density change
        density_change = np.average(mo.rho / (CONST['rho_Earth'] * mo.M / mo.R_orig ** 3)) - 1
        P_magma = magma_ocean_hypo((planets_args['S_thresh'], planets_args['wrr'], planets_args['f_rgh'], rho_avg_out), a_eff_grid,
                                   diff_frac=density_change,
                                   parameter_of_interest=parameter_of_interest, f_dR=f_dR)
        P0 = magma_ocean_f0(rho_avg_out, a_eff_grid)

    # back transform from a_eff to S
    S_grid = a_eff2S(a_eff_grid)

    offset = 0.003
    ax.plot(S_grid, P0, label='H$_\mathrm{0}$', c='C0', zorder=9)
    ax.plot(S_grid, P_magma + offset, label='H$_\mathrm{rgh}$', c='C2', zorder=9)
    ax.set_xscale('log')
    ax.set_xscale('log')

    ax.set_xlabel('Net instellation [$\mathrm{W/m^2}$]')

    if parameter_of_interest == 'R':
        ax.set_ylabel('Planet radius [R$_\oplus$]')
    elif parameter_of_interest == 'rho':
        ax.set_ylabel('Bulk density [$\mathrm{g/cm^3}$]')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())

    ax.set_xlim(2050, 37)
    ax.set_ylim(.75, 1.41)

    # create legend with custom order and markers
    handles, labels = ax.get_legend_handles_labels()
    order = [2, 3, 1, 0]
    leg = ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order],
               loc='upper left', ncol=1, bbox_to_anchor=(1.0, 1.02),
               frameon=False, columnspacing=0, labelspacing=1.6)
    try:
        leg.legend_handles[0].set_color('k')
        leg.legend_handles[0].set_sizes([4])
        leg.legend_handles[1].set_color('white')
        leg.legend_handles[1].set_ec('black')
    except AttributeError:
        # for older matplotlib versions ~<3.7
        leg.legendHandles[0].set_color('k')
        leg.legendHandles[0].set_sizes([4])
        leg.legendHandles[1].set_color('white')
        leg.legendHandles[1].set_ec('black')

    return ax


def draw_Sthresh(ax, planets_args):
    """add vertical line at threshold instellation."""
    ax.axvline(planets_args['S_thresh'], ymin=-10., linestyle='--', c='gray')
    ax.annotate("S$_\mathrm{thresh}$", xy = (planets_args['S_thresh'], 0.75), xycoords='data', xytext = (0, -18.),
                textcoords = 'offset points', ha = 'center', va = 'top', zorder=-9,
                arrowprops = dict(arrowstyle='-|>', connectionstyle='arc3,rad=0', lw=1.5, color='gray'))
    ax.xaxis.labelpad = 20
    return ax

def plot_has_magmaocean(sample, ax):
    sample = sample.sample(3000, random_state=42)

    for has_MO, color in zip([False, True], ['C0', 'C2']):
        x, y = sample[sample['has_magmaocean'] == has_MO]['P'], sample[sample['has_magmaocean'] == has_MO]['has_magmaocean']
        ax.scatter(x,y, s=1.5, c=color, alpha=.5)

    ax.set_xscale('log')
    ax.set_xlabel('Orbital period [d]')
    ax.set_yticks([0,1])
    ax.tick_params(axis='y', which='both', length=0)
    ax.set_yticklabels(['non-runaway','runaway'])

    # ax.annotate("runaway GH", xy=(0.05, 1.), xytext=(0, 0), fontsize=12, xycoords='axes fraction',
    #                         textcoords='offset points', ha='left', va='top', color='C2')
    # ax.annotate("no runaway GH", xy=(.95, 0.2), xytext=(0, 0), fontsize=12, xycoords='axes fraction',
    #                         textcoords='offset points', ha='right', va='bottom', color='C0')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # To turn off the bottom or left
    #ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_ylim(-.25, 1.5)
    # ax.legend(loc='lower right', ncol=99, bbox_to_anchor=(.99, .7),
    #                               frameon=False, columnspacing=1.6)
    return ax


def main(sample, planets_args, parameter_of_interest, f_dR=None):
    # sample from the sample for a less cluttered plot
    sample_df = sample.to_pandas().sample(min(15000, len(sample)), random_state=42)


    fig, (ax, ax2) = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [1.5, 6]}, figsize=[10.36, 6.4])
    ax = plot_has_magmaocean(sample_df, ax)
    ax2 = draw_Sthresh(ax2, planets_args)
    ax2 = plot_transitingplanets(sample_df, planets_args, ax2, parameter_of_interest=parameter_of_interest)
    ax2 = plot_HnullHmo(sample_df, planets_args, ax2, parameter_of_interest=parameter_of_interest, f_dR=f_dR)
    ax.set_title('Synthetic planets', y=1.35, fontsize=14)
    fig.tight_layout(h_pad=2.)

    fig.savefig(paths.figures / "HnullHmo.pdf")
    return fig, (ax, ax2)

with open(paths.data / 'planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)
with open(paths.data / 'sample.pkl', 'rb') as f:
    sample = pickle.load(f)

main(sample, planets_args, parameter_of_interest='R', f_dR=None)