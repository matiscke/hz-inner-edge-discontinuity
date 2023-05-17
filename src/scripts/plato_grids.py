import paths
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

import plotstyle
plotstyle.styleplots()

from bioverse import analysis, plots


def plot_plato_grids(f_grid, results, labels, yaxis='dlnZ', interpolate=False, plot_percentiles=False,
                     ci_percentiles=(16., 84.), fig=None, ax=None, smooth=True, **plot_kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    if yaxis == 'dlnZ':
        y_label = 'Log-evidence difference $ \Delta \ln Z$'
        for i, (r, l) in enumerate(zip(results, labels)):
            y = r['dlnZ']
            # y_mean = np.median(y, axis=-1)
            y_mean = np.median(y, axis=-1)
            percentiles = np.percentile(y, ci_percentiles, axis=1)  # 5% and 95% percentiles
            if interpolate:
                f_grid_fine = np.linspace(min(f_grid), max(f_grid), num=60)
                interpolate_grid = interp1d(f_grid, y_mean, kind='quadratic')
                y_mean = interpolate_grid(f_grid_fine)
                # p = fit_poly(f_grid, y_mean, 3)
                # y_mean = p(f_grid_fine)
                interpolate_p_lo = interp1d(f_grid, percentiles[0], kind='quadratic')
                interpolate_p_up = interp1d(f_grid, percentiles[1], kind='quadratic')
                percentiles = [interpolate_p_lo(f_grid_fine), interpolate_p_up(f_grid_fine)]
                x = f_grid_fine
            else:
                x = f_grid

            if smooth:
                # y_mean = convolve(y_mean, Gaussian1DKernel(0.8)) #Box1DKernel(3, mode='integrate'))
                y_mean = savgol_filter(y_mean, window_length=15, polyorder=2, mode='nearest')
            p = ax.plot(x, y_mean, lw=3, label=l, **plot_kwargs)
            if plot_percentiles:
                lns2 = ax.fill_between(x,
                                       percentiles[0],
                                       percentiles[1],
                                       alpha=.15, color=p[-1].get_color())
        ax.axhline(3, lw=1, c='gray', linestyle='-')
        ax.annotate('$\Delta \ln Z$ = 3', (.97, 2.4), va='top', ha='right', c='gray')
        ax.set_yscale('symlog')

    elif yaxis == 'power':
        y_label = 'Statistical power [%]'
        for i, (r, l) in enumerate(zip(results, labels)):
            y = analysis.compute_statistical_power(r, threshold=None, method='dlnZ')
            ax.plot(f_grid, np.array(y) * 100, lw=2,
                    label=l, **plot_kwargs)

    ax.set_xlabel('Dilution factor $f_\mathrm{rgh}$')
    ax.set_ylabel(y_label)
    ax.set_xlim(0, 1)
    # # plt.ylim(1e-5, 20)
    ax.legend(loc='lower left', ncol=2, bbox_to_anchor=(0.02, .98),
              frameon=False, columnspacing=6)
    return fig, ax


"""load pre-computed hypothesis testing grids."""
hypothesisgrids = {'res_fg_plato': 'plato_f-grid.pkl',
                   'res_fg_plato100' : 'plato100_f-grid.pkl',
                   'res_fg_plato40' : 'plato40_f-grid.pkl',
                   'res_fg_plato_rho' : 'plato_rho_f-grid.pkl',
                   'res_fg_plato_FGK_R':'plato_FGK_R.pkl',
                   'res_fg_plato_FGK_rho':'plato_FGK_rho.pkl', # FGK vs M
                   'res_fg_plato_M_R':'plato_M_R.pkl',
                   'res_fg_plato_M_rho':'plato_M_rho.pkl',} # FGK vs M
for varname, path in zip(hypothesisgrids.keys(),
                         [str(paths.data) + '/bioverse_objects/' + fname for fname in hypothesisgrids.values()]):
    with open(path, 'rb') as f:
        loaded_obj = pickle.load(f)
        exec(varname + '= loaded_obj')

N_plato = np.rint(res_fg_plato['N_pl'].mean())
num_grid = 11 # number of points in the grid
f_grid = np.linspace(0., 1., num_grid)

# plot different sample sizes and with/without follow-up
interpolate = False
smooth = True  # Apply Savgol filter (always compare with unsmoothed version to ensure no weird features are introduced)

# with plt.style.context('dark_background'):
fig, [ax, ax1, ax2] = plt.subplots(1, 3, sharey=True, figsize=[12, 4],
                                   gridspec_kw={'wspace': 0.08, 'width_ratios': [8, 8, 1]})
# fig, [ax, ax1] = plt.subplots(1, 2, sharey=True, figsize=[12, 4], gridspec_kw={'wspace': 0.1, 'width_ratios':[8,8]})
fig, ax = plot_plato_grids(f_grid, [res_fg_plato],
                           ['$N={:.0f}$'.format(N_plato)],
                           interpolate=interpolate, fig=fig, ax=ax, c='k')

fig, ax = plot_plato_grids(f_grid, [res_fg_plato100],
                           ['${N=100}$'],
                           interpolate=interpolate, fig=fig, ax=ax)

fig, ax = plot_plato_grids(f_grid, [res_fg_plato40],
                           ['${N=40}$'],
                           interpolate=interpolate, fig=fig, ax=ax, c='C4')

fig, ax = plot_plato_grids(f_grid, [res_fg_plato_rho],
                           ['Follow-up$_{N=100}$'],
                           # ['PLATO'],
                           interpolate=interpolate, ci_percentiles=(16, 84.),
                           fig=fig, ax=ax, linestyle=':', c='C0')

# plot FGK vs. M
# ================
default_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
custom_cycle = [default_cycle[i] for i in [3, 1, 3, 1]]

# fig, ax = plt.subplots()
ax1.set_prop_cycle(color=custom_cycle)

fig, ax1 = plot_plato_grids(f_grid, [res_fg_plato_FGK_R, res_fg_plato_M_R],
                            ['${FGK}$', '${M}$'],
                            fig=fig, ax=ax1, interpolate=interpolate)

fig, ax1 = plot_plato_grids(f_grid, [res_fg_plato_FGK_rho, res_fg_plato_M_rho],
                            ['Follow-up$_{FGK}$', 'Follow-up$_{M}$'],
                            # ['PLATO'],
                            interpolate=interpolate, ci_percentiles=(16, 84.),
                            fig=fig, ax=ax1, linestyle=':')

ax.set_title('Impact of sample size', y=1.24, fontsize=15)
ax1.set_title('FGK vs. M', y=1.24, fontsize=15)

ax1.set_ylabel(None)
ax1.set_xlim(left=0.01)
ax2.axis('off')
ax2.set_xlim(left=-0.2)
ax2.plot([0., 0.], [ax1.get_ylim()[0], 2.5], lw=10, c='r', alpha=.66, solid_capstyle="butt")
ax2.text(0.3, 3., 'non-detection  ', rotation=90, va='top', c='r', alpha=.66)
ax2.plot([0., 0.], [3.5, ax1.get_ylim()[1]], lw=10, c='g', alpha=.66, solid_capstyle="butt")
ax2.text(0.3, 3., '      detection', rotation=90, va='bottom', c='g', alpha=.66)
# ax1.set_ylim(-2.5, 400)
ax1.set_ylim(-1., 301)

fig.savefig(paths.figures / 'plato_fgrid.pdf')