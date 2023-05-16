## compare avg delta R/rho with expected from atmosphere models
from scipy.interpolate import LinearNDInterpolator

import paths
import pickle
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
import plotstyle
plotstyle.styleplots()

from bioverse.hypothesis import get_avg_deltaR_deltaRho, compute_avg_deltaR_deltaRho
from bioverse.constants import DATA_DIR, CONST
from cycler import cycler

def prepare_data():
    # Read M-R relations from Turbet+2020
    purerock = pd.read_csv(DATA_DIR + 'mass-radius_relationships_mgsio3_Zeng2016.txt')
    purerock.loc[:, 'wrr'] = 0.
    turbet2020 = pd.read_csv(DATA_DIR + 'mass-radius_relationships_STEAM_TURBET2020_FIG2b.dat', comment='#')
    mass_radius = purerock.append(turbet2020, ignore_index=True)

    # Read radius differences from DL21 Fig. 3b
    delta_R = pd.read_csv(DATA_DIR + 'deltaR_DornLichtenberg21_Fig3b.csv', comment='#')
    delta_R.set_index('wrr', inplace=True)

    # Combine Turbet+2020 and DL21 radius diffs:
    # interpolate within planet masses for the given water mass fraction wrr
    x = delta_R.index.to_numpy()
    y = np.array([float(c) for c in delta_R.columns])
    z = delta_R.to_numpy().flatten()
    grid = []
    for xi in x:
        for yi in y:
            grid.append((xi, yi))
    grid= np.array(grid)
    interp = LinearNDInterpolator(list(grid), z)

    mass_radius.loc[:,'radius_tot'] = mass_radius.radius + interp(mass_radius.wrr, mass_radius.mass)
    # plt.scatter(mass_radius.radius, mass_radius.radius_tot)

    # Read radius differences as measured in synthetic population
    # avg_deltaR_deltaRho = get_avg_deltaR_deltaRho()
    with open(paths.data / 'stars_args.pkl', 'rb') as f:
        stars_args = pickle.load(f)
    with open(paths.data / 'planets_args.pkl', 'rb') as f:
        planets_args = pickle.load(f)

    try:
        avg_deltaR_deltaRho = avg_deltaR_deltaRho = pd.read_csv(paths.data / 'avg_deltaR_deltaRho.csv', comment='#')
    except:
        avg_deltaR_deltaRho = compute_avg_deltaR_deltaRho(stars_args, planets_args, transiting_only=True, savefile=True)
        # write table to file
        with open(paths.data / 'avg_deltaR_deltaRho.csv', 'w') as f:
            f.write('# Radius and bulk density differences based on a sample of low-mass ({:.1f}-{:.1f} Mearth) '
                    'and detectable (transit depth >{:.2E}) planets, excluding extreme irradiances '
                    '(>{:.0f} W/m2).\n'.format(*[planets_args[key] for key in ['M_min', 'M_max', 'depth_min', 'S_max']]))
            avg_deltaR_deltaRho.to_csv(f, index=False)
    return mass_radius, avg_deltaR_deltaRho

def plot_model_pop_comparison(mass_radius, target_mass, avg_deltaR_deltaRho):
    fig, axs = plt.subplots(1, 2, figsize=[12, 4])

    r2rho = lambda M, R: CONST['rho_Earth'] * M / R ** 3
    for i, x in enumerate(['R', 'rho']):
        ax = axs[i]
        for target_mass, color in zip(np.linspace(0.6, 1.8, 7),
                                      cycler(color=reversed(sns.color_palette("rocket", n_colors=8, desat=None)))):
            # compute dry radius at target mass
            mr_dry = mass_radius[mass_radius.wrr == 0.]
            mr_drym = mr_dry.iloc[(mr_dry.mass - target_mass).abs().argsort()[0], :]

            if x == 'R':
                dry_x = mr_drym.radius
            elif x == 'rho':
                dry_x = r2rho(mr_drym.mass, mr_drym.radius)

            wrrs = mass_radius.wrr.unique()
            dx_models = []
            dx_pop = []
            for wrri in wrrs:
                # for each water mass fraction, compute difference between model and synthetic population mean
                mrwrr = mass_radius[mass_radius.wrr == wrri]
                mrwrr.reset_index(drop=True, inplace=True)
                mrwrrm = mrwrr.iloc[(mrwrr.mass - target_mass).abs().argsort()[0], :]
                if x == 'R':
                    dx_models.append(mrwrrm.radius_tot - dry_x)
                elif x == 'rho':
                    dx_models.append(r2rho(mrwrrm.mass, mrwrrm.radius_tot) - dry_x)

                dx_pop.append(avg_deltaR_deltaRho[avg_deltaR_deltaRho.gh_increase
                                                  & avg_deltaR_deltaRho.water_incorp & (
                                                              avg_deltaR_deltaRho.wrr == wrri)]['delta_' + x])

            # plt.scatter(dx_models, dx_pop)
            ax.plot(wrrs, np.subtract(np.array(dx_models), np.array(dx_pop).flatten()) / np.array(dx_models),
                    label='{:.1f}'.format(target_mass),
                    color=color['color'])
        ax.set_xscale('log')
        ax.set_xlabel('Water mass fraction $x_\mathrm{H_2O}$')
        if x == 'R':
            ax.set_ylabel(
                r'$\frac{{\Delta {0}_\mathrm{{model}} - \langle \Delta {0}_\mathrm{{population}}\rangle }}{{\Delta {0}_\mathrm{{model}}}}$'.format(
                    x))
        elif x == 'rho':
            ax.set_ylabel(
                r'$\frac{{\Delta \{0}_\mathrm{{model}} - \langle \Delta \{0}_\mathrm{{population}}\rangle}}{{\Delta \{0}_\mathrm{{model}}}}$'.format(
                    x))
    ax.legend(loc='upper left', ncol=1, bbox_to_anchor=(1.03, 1.15), title='$M_P \, [M_\oplus]$',
              frameon=False, labelspacing=1.3)
    fig.subplots_adjust(top=1., wspace=0.3)
    axs[0].set_title('Radius measurement')
    axs[1].set_title('Density measurement')
    return fig, axs


# target_mass = 1.0  # mass to compare in Earth masses
# mass_radius, avg_deltaR_deltaRho = prepare_data()
# fig, axs = plot_model_pop_comparison(mass_radius, target_mass, avg_deltaR_deltaRho)
# fig.savefig(paths.figures / 'model_pop_comparison.pdf')

# avoid expensive computation above and use static figure from previous run
import os
os.system('cp  {}/model_pop_comparison.pdf {}/model_pop_comparison.pdf'.format(paths.static, paths.figures))