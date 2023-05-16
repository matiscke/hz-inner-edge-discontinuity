"""Show corner plot of parameter inference example"""

import pickle
import corner
import paths
import numpy as np
import pandas as pd
from bioverse.constants import CONST

import plotstyle
plotstyle.styleplots()

def cornerplot(results, params, log, planets_args, parameter_of_interest, sample):
    # sampler_results into DataFrame, make logged columns for params with log priors
    chains = pd.DataFrame(results['chains'], columns=params)
    for p, l in zip(params, log):
        if l:
            chains['log_' + p] = np.log10(chains[p])

    # compute truths
    if parameter_of_interest == 'R':
        avg_out = np.average(sample['R'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting']])
    elif parameter_of_interest == 'rho':
        avg_out = np.average \
            (CONST['rho_Earth' ] *sample['M'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting'] ]/
                             (sample['R'][(sample['S_abs'] < planets_args['S_thresh']) & sample['transiting']] )**3)
    truths =np.array([planets_args['S_thresh'], np.log10(planets_args['wrr']), planets_args['f_rgh'], avg_out])

    fig = corner.corner(
        chains[['S_thresh', 'log_wrr', 'f_rgh']], labels=['$S_{thresh}$', '$\log(x_{H_2O})$', '$f_\mathrm{rgh}$'],
        truths=truths[:-1], truth_color='C1',
        range=[(10 ,600), (-5, -1.), (-0.01, 1.)],
        quantiles=[0.16, 0.5, 0.84],
        show_titles=True, title_kwargs={"fontsize": 12},
        hist_bin_factor=2.,
        smooth=.1,
        smooth1d=.1
    )
    return fig


with open(paths.data / 'sample.pkl', 'rb') as f:
    sample = pickle.load(f)
with open(paths.data / 'results_opt.pkl', 'rb') as f:
    results_opt = pickle.load(f)
with open(paths.data / 'params.pkl', 'rb') as f:
    params = pickle.load(f)
with open(paths.data / 'log.pkl', 'rb') as f:
    log = pickle.load(f)
with open(paths.data / 'planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)

fig = cornerplot(results_opt, params, log, planets_args, parameter_of_interest='R', sample=sample)

fig.savefig(paths.figures / 'corner.pdf')