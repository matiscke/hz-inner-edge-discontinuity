import paths
import pickle
import numpy as np
import cmocean
import matplotlib.pyplot as plt

import plotstyle
plotstyle.styleplots()

from bioverse import analysis, plots

def statistical_power_grid():
    wrr_grid = [0., 0.0001,0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05]
    # wrr_grid = [0.0001, 0.005, 0.05]
    f_rgh_grid = np.linspace(0., 1., len(wrr_grid))

    reduced_args = {key: planets_args[key] for key in planets_args if (key != 'wrr') & (key != 'f_rgh')} # remove keys used in the grid
    # results_grid = analysis.test_hypothesis_grid(h_magmaocean, g_transit, survey, wrr=wrr_grid, f_rgh=f_rgh_grid, N=20, processes=8, **reduced_args)
    results_grid = analysis.test_hypothesis_grid(h_magmaocean, g_transit, survey, wrr=wrr_grid, f_rgh=f_rgh_grid,
                                                 N=20, processes=8, return_chains=True, **reduced_args)
    return results_grid

def load_grid():
    """load previously computed statistical power grid"""
    with open(paths.data / 'bioverse_objects/optimistic_H2O-f-grid_G16.pkl', 'rb') as f:
        results_grid = pickle.load(f)
    wrr_grid = [0., 0.0001,0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05]
    f_rgh_grid = np.linspace(0., 1., len(wrr_grid))
    return results_grid, wrr_grid, f_rgh_grid

def plot_power_grid(results_grid):
    fig, ax = plt.subplots(figsize=[6, 4])
    labels = ('Water mass fraction $x_\mathrm{H_2O}$', 'Dilution factor $f_\mathrm{rgh}$')
    fig, ax = plots.plot_power_grid(results_grid, method='dBIC', axes=('wrr', 'f_rgh'), labels=labels,
                                    log=(True, False), show=False, fig=fig, ax=ax,
                                    # zoom_factor=2, smooth_sigma=.5,
                                    zoom_factor=0, smooth_sigma=.2,
                                    levels=[50, 95], cmap=cmocean.cm.dense_r)

    # workaround for smoothing, necessary when a parameter = 0 in the logged grid
    plt.close()
    from scipy.ndimage import zoom

    qm = ax.get_children()[0]
    z = qm.get_array().reshape(qm._meshWidth, qm._meshHeight)
    z[z < 20] = 0.  # set low values to zero to account for fluctuations

    zoom_factor=4
    z = zoom(z, zoom_factor, mode='nearest')
    x = zoom(wrr_grid, zoom_factor, mode='nearest')
    y = zoom(f_rgh_grid, zoom_factor, mode='nearest')

    fig, ax = plt.subplots(figsize=[6, 4])
    fig, ax = plots.image_contour_plot(x, y, z, colorbar=True, labels=(*labels, 'Statistical power (%)'),
                                       fmt=' %.0f %% ', levels=[50, 95], ticks=4, log=(True, False),
                                       fig=fig, ax=ax, return_ctr=False, zoom_factor=None, cmap=cmocean.cm.dense_r,
                                       plus=False, smooth_sigma=0, vmin=0., vmax=100)

    ax.set_xlim(2e-5, 0.05)
    ax.set_ylim(0, 1)

    ax.set_xlabel(labels[0], fontsize=12)
    ax.set_ylabel(labels[1], fontsize=12)
    # ax.set_title('Optimistic survey ({} planets)'.format(N), y=1.05, fontsize=14)
    ax.set_title('Statistical power', y=1.05, fontsize=14)
    ax.collections[0].colorbar.set_label('Statistical power [%]', fontsize=12, labelpad=13.)
    return fig, ax

results_grid, wrr_grid, f_rgh_grid = load_grid()

fig, ax = plot_power_grid(results_grid)
fig.savefig(paths.figures / 'optimistic_statpwr_H2O-f.pdf')


