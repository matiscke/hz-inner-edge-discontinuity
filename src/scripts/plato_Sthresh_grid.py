import paths
import pickle
from warnings import warn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import plotstyle
plotstyle.styleplots()


def plot_posterior_hist(results_grid, fig=None, ax=None, truth=None, seed=42, param_idx=0, **grid_kwargs):
    np.random.seed(seed)
    try:
        grid = results_grid['grid'].copy()
        seq = [0] * len(grid)
        for i, (key, val) in enumerate(results_grid['grid'].items()):
            if key in grid_kwargs:
                seq[i] = np.argmin(np.abs(val - grid_kwargs[key]))

            elif key == 'N':
                # Pick a random simulation unless specified
                seq[i] = np.random.choice(grid['N'])
            elif len(val) > 1:
                warn("which value of '{:s}' should be plotted? assuming {:s} = {:.1f}".format(key, key, val[0]))

            # Removes 'N' and other reduced grid dimensions
            del grid[key]

        # Extract the MCMC samples for this simulation
        samples = results_grid['chains'][tuple(seq)]

    except KeyError:
        samples = results_grid['chains']

    if fig is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    if 'h' in results_grid:
        xmin, xmax = results_grid['h'].bounds[param_idx]
    else:
        xmin, xmax = (np.min(samples[...,param_idx]), np.max(samples[...,param_idx]))


    bins = np.logspace(np.log10(xmin), np.log10(xmax), 50)
    # bins = np.linspace(0, 1, 50)
    # ax.hist(samples[..., param_idx], histtype='step', bins=bins, lw=lw, color='black', density=True)
    ax.hist(samples[..., param_idx], histtype='step', bins=bins, color='black', density=True)

    if truth:
        # Plot the truth value
        ax.axvline(truth, lw=5, c='C0', alpha=0.75)

    # Axes
    # ax.set_xlim([0, 1])
    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])

    ax.get_xaxis().set_major_formatter(ScalarFormatter())

    return fig, ax


def plot_posterior_hist_(results_grid, fig=None, ax=None, lw=1.0, seed=42, param='S_thresh', **grid_kwargs):
    np.random.seed(seed)
    # Reduce the grid to the 1 or 2 dimensions in `axes`
    grid = results_grid['grid'].copy()
    seq = [0] * len(grid)
    truth = None
    for i, (key, val) in enumerate(results_grid['grid'].items()):
        if key in grid_kwargs:
            seq[i] = np.argmin(np.abs(val - grid_kwargs[key]))
            if key == param:
                # Determine the truth value of the parameter in this set of simulations
                truth = grid[key][seq[i]]
        elif key == 'N':
            # Pick a random simulation unless specified
            seq[i] = np.random.choice(grid['N'])
        elif len(val) > 1:
            warn("which value of '{:s}' should be plotted? assuming {:s} = {:.1f}".format(key, key, val[0]))

        # Removes 'N' and other reduced grid dimensions
        del grid[key]

    # Extract the MCMC samples for this simulation
    samples = results_grid['chains'][tuple(seq)]
    # power = analysis.compute_statistical_power(results_grid, method='dBIC')
    # print(power[tuple(seq)[:-1]])
    # print(results_grid['p'][tuple(seq)]<0.05, results_grid['dBIC'][tuple(seq)]>6)

    # Plot samples of specified parameter
    if fig is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    xmin, xmax = results_grid['h'].bounds[1]

    bins = np.logspace(np.log10(xmin), np.log10(xmax), 50)
    # bins = np.linspace(0, 1, 50)
    ax.hist(samples[..., 1], histtype='step', bins=bins, lw=lw, color='black', density=True)

    if truth:
        # Plot the truth value
        ax.axvline(truth, lw=5, c='C0', alpha=0.75)

    # Axes
    # ax.set_xlim([0, 1])
    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])

    ax.get_xaxis().set_major_formatter(ScalarFormatter())

    return fig, ax

def plot_plato_Sthresh_grid(grids, planets_args):

    [print(g['N_pl'].mean()) for g in grids]

    nrows = 7
    ncols = len(grids)
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, gridspec_kw={'wspace': 0.1, 'hspace': 0.1}, figsize=(6, 6))

    for col, case in zip(range(ncols), grids):
        for i, (ax, f_rgh) in enumerate(zip(axs[:, col], np.linspace(0.95, .05, nrows))):
            plot_posterior_hist(case, fig=fig, ax=ax, seed=i + 99, wrr=0.005, f_rgh=f_rgh)

            if col == ncols - 1:
                ax.text(1.07, 0.5, '{:.2f}'.format(f_rgh),
                        transform=ax.transAxes, va='center_baseline', fontsize=10)

    # annotate truth
    axs[0, 0].text(.35, .9, 'truth', rotation=0, ha='left', c='C1',
                   transform=axs[0, 0].transAxes, va='top', fontsize=11)

    # arrow with f_rgh
    axs[-1, -1].text(1.40, 0., 'Dilution factor  $f_\\mathrm{{rgh}}$', ha='left', rotation=90,
                     transform=axs[-1, -1].transAxes, va='bottom', fontsize=11)
    arrow = axs[-1, -1].annotate('', (1.35, -.05), xytext=(1.35, 3.5), arrowprops={'arrowstyle': '<-'},
                                 xycoords=axs[-1, -1].transAxes, va='center')

    # eye candy
    for ax in axs.flatten():
        # plot truths
        ax.axvline(planets_args['S_thresh'], c='C1', lw=1.5)

        ax.tick_params(left=False, right=False, labelleft=False,
                       labelbottom=False, bottom=False)
        # ax.set_xlim(100, 1000)
        ax.invert_xaxis()
        ax.spines[['left', 'right', 'top']].set_visible(False)

    for ax in axs[-1, :]:
        ax.tick_params(labelbottom=True, bottom=True)
        ax.set_xlabel('$S_\mathrm{thresh}$ [W/m$^2$]')

    for ax in axs[-1, :-1]:
        ax.xaxis.set_ticks([100, 1000])

    # fig.suptitle('N=100', y=1.15)
    axs[0, 0].set_title('No follow-up\n', y=1.1, fontsize=12)
    axs[0, 1].set_title('Follow-up\n', y=1.1, fontsize=12)
    axs[0, 2].set_title('Follow-up,\nonly M dwarfs', y=1.2, fontsize=12)

    return fig, axs



if __name__ == "__main__":
    with open(paths.data / 'pipeline/planets_args.pkl', 'rb') as f:
        planets_args = pickle.load(f)

    """load previously computed hypothesis test grids"""
    hypothesisgrids = {'res_fg_plato100' : 'plato100_f-grid.pkl',
                       'res_fg_plato_rho': 'plato_rho_f-grid.pkl',
                       'res_fg_plato_M_rho_100':'plato_M_rho_100.pkl',}
    for varname, path in zip(hypothesisgrids.keys(),
                             [str(paths.data) + '/bioverse_objects/' + fname for fname in hypothesisgrids.values()]):
        with open(path, 'rb') as f:
            loaded_obj = pickle.load(f)
            exec(varname + '= loaded_obj')
    grids = [res_fg_plato100, res_fg_plato_rho, res_fg_plato_M_rho_100]
    fig, axs = plt.subplots(nrows=6, ncols=3)
    fig, axs = plot_plato_Sthresh_grid(grids, planets_args)

    fig.savefig(paths.figures / "S_thresh_posteriors.pdf")