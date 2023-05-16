"""
This file contains the code to generate the datasets for the paper.
It heavily relies on Bioverse and its auxiliary functions.
"""

import scipy
import paths
from utils import *
import pickle
import corner
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# Import the Generator class
from bioverse.generator import Generator
from bioverse.survey import TransitSurvey
from bioverse.constants import CONST, DATA_DIR
from bioverse.hypothesis import Hypothesis, magma_ocean_hypo, magma_ocean_f0, get_avg_deltaR_deltaRho

# Sample generation
## Generate stars and planets, inject magma oceans

# Parameters of the analysis
# parameter_of_interest = 'rho'
parameter_of_interest = 'R'

def get_generator_args():
    """ define generator parameters"""
    # Parameters for star generation
    stars_args = {
        'd_max' : 90,             # max. dist to stars (pc) ~~(nominal=90, ca. 481 planets)~~
        'M_st_max': 1.5,  # Maximum stellar mass to consider, in solar units.
        'M_G_max': 16,  # Maximum gaia magnitude of stars
        'seed': 42,  # seed for random number generators
        'lum_evo': True  # luminosities from luminosity tracks (Baraffe et al. 1998), based on random ages? [SLOW?]
    }

    # Parameters for planet generation and magma ocean model
    planets_args = {
        'transit_mode': False,  # Simulate only transiting planets
        'f_eta': 1.,  # Occurrence rate scaling factor
        'R_min': 0.75,  # minimum radius for Bergsten et al. planet generator
        'P_max': 500.,  # maximum period for Bergsten et al. planet generator
        'mr_relation': 'Zeng2016',  # choice of mass-radius relationship ('Zeng2016'/'Wolfgang2016/'earthlike')
        'gh_increase': True,  # wether or not to consider radius increase due to runaway greenhouse effect (Turbet+2020)
        'water_incorp': True, # wether or not to consider water incorporation in the melt of global magma oceans (Dorn & Lichtenberg 2021)
        'S_thresh': 280.,  # threshold instellation for runaway greenhouse phase
        'wrr': 0.005, # water-to-rock ratio for Turbet+2020 model. Possible vals: 0.0001,0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05
        'f_rgh': .8,  # fraction of planets with a runaway gh climate _within_ the runaway gh regime
        'simplified': False,  # increase the radii of all runaway greenhouse planets by the same fraction
        # 'diff_frac' : 0.48,       # fractional radius change in the simplified case.

        # detection bias and sample selection: Keep only small planets/low-mass planets, but above 0.1 M_Earth (Turbet+2020 covers only 0.1 to 2 Mearth). Don't consider "lava worlds" with extremely high instellation.
        # Set a generic detection bias: transit depth $\delta > 75$ ppm.
        'M_min': 0.1,
        'M_max': 2.,
        'S_min': 10.,  # min. instellation in W/m2
        'S_max': 2000.,  # max. instellation in W/m2
        'depth_min': 80e-6  # min. transit depth
    }
    return stars_args, planets_args


def generate_generator(stars_only=False, **kwargs):
    stars_args, planets_args = get_generator_args()
    g_args = stars_args | planets_args
    for key, value in kwargs.items():
        g_args[key] = value
    g_transit = Generator(label=None)
    g_transit.insert_step('read_stars_Gaia')
    if not stars_only:
        g_transit.insert_step('create_planets_bergsten')
        g_transit.insert_step('assign_orbital_elements')
        g_transit.insert_step('impact_parameter')
        g_transit.insert_step('assign_mass')
        g_transit.insert_step('effective_values')
        g_transit.insert_step('magma_ocean')  # here we inject the magma oceans
        g_transit.insert_step('compute_transit_params')
        g_transit.insert_step('apply_bias')
    [g_transit.set_arg(key, val) for key, val in g_args.items()]
    return g_transit


def generate_sample():
    g_transit = Generator(label=None)
    g_transit.insert_step('read_stars_Gaia')
    stars_args, planets_args = get_generator_args()

    g_transit.insert_step('create_planets_bergsten')
    g_transit.insert_step('assign_orbital_elements')
    g_transit.insert_step('impact_parameter')
    g_transit.insert_step('assign_mass')
    g_transit.insert_step('effective_values')
    g_transit.insert_step('magma_ocean')  # here we inject the magma oceans
    g_transit.insert_step('compute_transit_params')
    g_transit.insert_step('apply_bias')

    # provide generator arguments chosen above
    [g_transit.set_arg(key, val) for key, val in stars_args.items()]
    [g_transit.set_arg(key, val) for key, val in planets_args.items()]

    sample = g_transit.generate()
    # print('Total number of planets: {}'.format(len(sample)))
    return sample


def survey_simulation():
    """Simulate an ambitious survey with optimistic parameters."""
    # create a transit survey (telescope parameters don't really matter here)
    survey = TransitSurvey(diameter=8.5, t_max=3652.5, t_slew=0.1, N_obs_max=1000)

    # Let's add some measurements our survey conducts.
    margs = {}
    mkeys = ['L_st', 'R_st', 'M_st', 'T_eff_st', 'd', 'age', 'depth', 'R',
             'T_dur', 'P', 'a', 'a_eff', 'S', 'S_abs',
             'M', 'rho']

    # Optimistic survey: choose optimistic values
    margs['precision'] = {'T_eff_st': 25.,
                          'R_st': '1%',
                          'depth': '1%',
                          'R': '2%',
                          'M_st': '1%',
                          'age': '30%',
                          'P': 0.000001,
                          'S': '5%',
                          'S_abs': '5%',
                          'M': '5%',
                          'rho': '7%'}

    # Add the measurements to the survey
    for mkey in mkeys:
        kwargs = {}
        for key, vals in margs.items():
            if mkey in vals:
                kwargs[key] = vals[mkey]
        survey.add_measurement(mkey, **kwargs)

    # which planets are detectable?
    detected_opt = survey.compute_yield(sample)
    N = len(detected_opt)
    # save_var_latex('N_optimistic', '{:.0f}'.format(N))
    save_var_latex('N_optimistic', '500') # round that to avoid confusion

    # simulate observations, obtain dataset
    data = survey.observe(detected_opt, demographics=True)
    return detected_opt, data


def hypotest(data, parameter_of_interest, params, log, bounds, bounds_null, features=('a_eff',), binned=False,
             nburn=100, nlive=500):
    """perform hypothesis test.

    Parameters
    ----------
    data : Table
        Table containing the sample of simulated planets.
    parameter_of_interest : str
        Parameter of interest, 'R' or 'rho'
    binned : bool
        if true, use the binned average radius/density; otherwise use a rolling mean.
    nburn : int
        length of burn-in phase in the nested sampling
    nlive : int
        number of live points for the nested sampling
    """

    if binned:
        labels = (parameter_of_interest + '_mean_binned',)
    else:
        labels = (parameter_of_interest + '_mean',)

        # interpolate average delta R/delta rho
    avg_deltaR_deltaRho = get_avg_deltaR_deltaRho()
    select_mechanisms = (avg_deltaR_deltaRho.gh_increase == planets_args['gh_increase']) & (
            avg_deltaR_deltaRho.water_incorp == planets_args['water_incorp'])
    f_dR = scipy.interpolate.interp1d(avg_deltaR_deltaRho[select_mechanisms].wrr,
                                      avg_deltaR_deltaRho[select_mechanisms]['delta_' + parameter_of_interest],
                                      fill_value='extrapolate')



    if parameter_of_interest == 'R':
        # define hypothesis; define null hypothesis (a broad distribution in planet radius that is independent of orbital distance)
        h_magmaocean = Hypothesis(magma_ocean_hypo, bounds, params=params, features=features, labels=labels,
                                  log=log, gh_increase=planets_args['gh_increase'],
                                  water_incorp=planets_args['water_incorp'],
                                  simplified=planets_args['simplified'],
                                  parameter_of_interest=parameter_of_interest, f_dR=f_dR)
        h_magmaocean.h_null = Hypothesis(magma_ocean_f0, bounds_null, params=('R_avg_random',), features=features,
                                         labels=labels, log=(log[-1],))



    elif parameter_of_interest == 'rho':
        h_magmaocean = Hypothesis(magma_ocean_hypo, bounds, params=params, features=features, labels=labels,
                                  log=log, gh_increase=planets_args['gh_increase'],
                                  water_incorp=planets_args['water_incorp'],
                                  simplified=planets_args['simplified'],
                                  parameter_of_interest=parameter_of_interest, f_dR=f_dR)
        h_magmaocean.h_null = Hypothesis(magma_ocean_f0, bounds_null, params=('rho_avg_random',), features=features,
                                         labels=labels, log=(log[-1],))

    # perform hypothesis tests

    # Sample the posterior distribution of h(theta | x, y) using a simulated data set, and compare to the null hypothesis via a model comparison metric.
    results = h_magmaocean.fit(data, return_chains=True, nburn=nburn, nlive=nlive, sampler_results=True)
    # results_opt = h_magmaocean.fit(data, return_chains=True, nburn=500, nsteps=5000, method='emcee')

    print("The evidence in favor of the hypothesis is: dlnZ = {:.1f} (corresponds to p = {:.3f})".format(
        results['dlnZ'], np.exp(-results['dlnZ'])))

    return results, h_magmaocean

def hypothesis_tests(parameter_of_interest='R'):
    """define the hypothesis, and perform hypothesis tests.

    Sample the posterior; Calculate the Bayesian evidence supporting h_magmaocean in favor of h_null from our simulated dataset.
    The parameter space is complex, we need to use nested sampling (not MCMC).
    """
    params = ('S_thresh', 'wrr', 'f_rgh', 'avg')
    features = ('a_eff',)
    labels = (parameter_of_interest + '_mean',)
    log = (False, True, False, False)
    nburn = 100

    # define PRIORS for the parameters in theta uniform for 'S_thresh', log-uniform for 'wrr', uniform for 'f_rgh', 'R_avg')
    bounds_R = np.array([[10., 1000.0], [1e-5, 0.1], [0.0, 1.0], [.1, 15.]])
    bounds_rho = np.array([[10., 1000.0], [1e-5, 0.1], [0.0, 1.0], [1., 6.]])
    if parameter_of_interest == 'R':
        bounds = bounds_R
    elif parameter_of_interest == 'rho':
        bounds = bounds_rho

    bounds_null = np.array([bounds[-1]])  # prior bounds for null hypothesis

    results_opt, h_magmaocean = hypotest(data, parameter_of_interest, params=params, log=log, bounds=bounds,
                                         bounds_null=bounds_null, features=features, binned=False)
    return params, features, log, results_opt, h_magmaocean


stars_args, planets_args = get_generator_args()

with open(paths.data / 'planets_args.pkl', 'wb') as file:
    pickle.dump(planets_args, file)
with open(paths.data / 'stars_args.pkl', 'wb') as file:
    pickle.dump(stars_args, file)

sample = generate_sample()
with open(paths.data / 'sample.pkl', 'wb') as file:
    pickle.dump(sample, file)

detected_opt, data = survey_simulation()
with open(paths.data / 'data.pkl', 'wb') as file:
    pickle.dump(data, file)

params, features, log, results_opt, h_magmaocean = hypothesis_tests()
with open(paths.data / 'params.pkl', 'wb') as file:
    pickle.dump(params, file)
with open(paths.data / 'features.pkl', 'wb') as file:
    pickle.dump(features, file)
with open(paths.data / 'log.pkl', 'wb') as file:
    pickle.dump(log, file)
with open(paths.data / 'results_opt.pkl', 'wb') as file:
    pickle.dump(results_opt, file)
with open(paths.data / 'h_magmaocean.pkl', 'wb') as file:
    pickle.dump(h_magmaocean, file)
