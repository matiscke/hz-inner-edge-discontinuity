"""Explore inference with alternative mass-radius relations"""

import pickle
import paths
import numpy as np
import pandas as pd
from matplotlib.transforms import blended_transform_factory

import plotstyle
plotstyle.styleplots()
import seaborn as sns


def plot_splitviolin(planets_args, res_fg_MR_earthlike, res_fg_MR_Wolfgang2016):
    # sns.set_theme(style="whitegrid")
    earthlike = pd.DataFrame(np.mean(res_fg_MR_earthlike['chains'][:, :, :, 0].T, axis=1),
                             columns=res_fg_MR_earthlike['grid']['f_rgh'])
    earthlike.loc[:, 'M-R relation'] = 'Earth-like'
    wolfgang = pd.DataFrame(np.mean(res_fg_MR_Wolfgang2016['chains'][:, :, :, 0].T, axis=1),
                            columns=res_fg_MR_Wolfgang2016['grid']['f_rgh'])
    wolfgang = wolfgang[[c for c in wolfgang.columns if c in earthlike.columns]]

    wolfgang.loc[:, 'M-R relation'] = 'Wolfgang et al. (2016)'
    mr_df = pd.merge(left=earthlike, right=wolfgang, how='outer')

    # workaround for a weird rounding error...
    colnames = [np.round(c, decimals=1) for c in mr_df.columns[:-1]]
    colnames.append('M-R relation')
    mr_df.columns = colnames

    mr = pd.melt(mr_df, id_vars=['M-R relation'], var_name='f_rgh', value_name='S_thresh')
    mr = mr[mr['S_thresh'].notna()]

    # Draw a nested violinplot and split the violins for easier comparison
    # fig, ax = plt.subplots(figsize=[12,4])
    ax = sns.violinplot(data=mr, x="f_rgh", y="S_thresh", hue="M-R relation",
                        split=True,
                        inner="quartile",
                        # cut=0.5,
                        # saturation=.8,
                        linewidth=1.,
                        palette={'Earth-like': 'C1', 'Wolfgang et al. (2016)': 'C0'})

    # plot truths
    ax.text(5.6, planets_args['S_thresh'], 'truth', rotation=0, ha='left', c='.2',
            va='center', fontsize=13)
    ax.axhline(planets_args['S_thresh'], c='gray', lw=2., ls=(0, (3, 1, 1, 1)))

    # show dlnZ
    mean_dlnZ_earthlike = np.mean(res_fg_MR_earthlike['dlnZ'], axis=1)
    mean_dlnZ_wolfgang = np.mean(res_fg_MR_Wolfgang2016['dlnZ'], axis=1)
    trans = blended_transform_factory(x_transform=ax.transData, y_transform=ax.transAxes)
    for i, (dlnZ_e, dlnZ_w) in enumerate(zip(mean_dlnZ_earthlike, mean_dlnZ_wolfgang)):
        ax.text(i - 0.2, .85, '{:.0f}'.format(dlnZ_e), rotation=0, c='C1',
                transform=trans, fontsize=11, ha='center', style='italic')
        ax.text(i + 0.2, .85, '{:.0f}'.format(dlnZ_w), rotation=0, c='C0',
                transform=trans, fontsize=11, ha='center', style='italic')
    ax.annotate('$\Delta \ln Z$', (5.35, .87), (5.6, .96), xycoords=trans, fontsize=12,
                arrowprops=dict(arrowstyle="-|>", fc='k', connectionstyle="arc3,rad=-0.4"))

    sns.despine(left=False, bottom=True, offset=10.)
    ax.set_xlabel('Dilution factor $f_\\mathrm{rgh}$')
    ax.set_ylabel('Threshold instellation $S_\\mathrm{thresh} \, \, [W/m^2]$')
    ax.legend(fontsize=12, loc='lower left', ncol=2, bbox_to_anchor=(0., 1.),
              frameon=False, columnspacing=1.6)
    return ax


with open(paths.data / 'pipeline/planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)

# load previously computed hypothesis test grids
hypothesisgrids = {'res_fg_MR_Wolfgang2016':'optimistic_MR_Wolfgang2016.pkl', 'res_fg_MR_earthlike':'optimistic_MR_earthlike.pkl',
                   'res_optimistic_H2O_fg':'optimistic_H2O-f-grid.pkl'}
for varname, path in zip(hypothesisgrids.keys(),
                         [str(paths.data) + '/bioverse_objects/' + fname for fname in hypothesisgrids.values()]):
    with open(path, 'rb') as f:
        loaded_obj = pickle.load(f)
        exec(varname + '= loaded_obj')

ax = plot_splitviolin(planets_args, res_fg_MR_earthlike, res_fg_MR_Wolfgang2016)

ax.get_figure().savefig(paths.figures / 'MR-violins.pdf')