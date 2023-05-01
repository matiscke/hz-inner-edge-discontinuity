"""
This file contains the code to generate the datasets for the paper.
It heavily relies on Bioverse and its auxiliary functions.
"""

import scipy
import paths
from utils import *
import pickle
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# Import the Generator class
from bioverse.generator import Generator
from bioverse.survey import TransitSurvey
from bioverse.constants import CONST, DATA_DIR

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

stars_args, planets_args = get_generator_args()

with open(paths.data / 'planets_args.pkl', 'wb') as file:
    pickle.dump(planets_args, file)

sample = generate_sample()
with open(paths.data / 'sample.pkl', 'wb') as file:
    pickle.dump(sample, file)