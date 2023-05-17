"""Plot prototypical detection in an optimistic survey (binned version)"""
import numpy as np
import pickle
import paths

import plotstyle
plotstyle.styleplots()

from optimistic_RS import plot_survey
from hzied_pipeline import hypotest

with open(paths.data / 'pipeline/data.pkl', 'rb') as f:
    data = pickle.load(f)
with open(paths.data / 'pipeline/planets_args.pkl', 'rb') as f:
    planets_args = pickle.load(f)

params = ('S_thresh', 'wrr', 'f_rgh', 'avg')
log = (False, True, False, False)
bounds = np.array([[10., 1000.0], [1e-5, 0.1], [0.0, 1.0], [.1, 15.]])
bounds_null = np.array([bounds[-1]])            # prior bounds for null hypothesis

results_binned, h_magmaocean = hypotest(data, 'R', params, log, bounds, bounds_null, binned=True)  # this time, perform hypothesis tests on binned average R/rho
fig, ax = plot_survey(data, results_binned, planets_args, parameter_of_interest='R', show_rolling_mean=False, show_binned_stats=True)
ax.set_title('Optimistic survey (binned)', y=1.13)

fig.savefig(paths.figures / 'optimistic_R-S_binned.pdf')