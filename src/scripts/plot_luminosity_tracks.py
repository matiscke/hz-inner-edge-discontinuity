import pandas as pd
import matplotlib.pyplot as plt
import glob
from natsort import natsorted
from scipy import interpolate
import seaborn as sns
import cmocean

import paths
import plotstyle
plotstyle.styleplots()

# sns.set(style="ticks")

# Change color cycle: https://matplotlib.org/3.1.1/users/dflt_style_changes.html#colors-in-default-property-cycle
# https://seaborn.pydata.org/tutorial/color_palettes.html
from cycler import cycler
# plt.rcParams['axes.prop_cycle'] = cycler(color=reversed(sns.cubehelix_palette(8)))
plt.rcParams['axes.prop_cycle'] = cycler(color=reversed(sns.color_palette("cmo.thermal", n_colors=8, desat=None)))

lum_tracks = natsorted(glob.glob(str(paths.data) + "/Lum_m*.txt"))
# print(lum_tracks)

for lum_track in reversed(lum_tracks):

    luminosity_df = pd.read_csv(lum_track)

    star_mass = str(lum_track[-7:-4])

    ages            = luminosity_df["age"]*1e+3
    luminosities    = luminosity_df["lum"]

    p = plt.plot(ages, luminosities, label=star_mass+" $M_{\odot}$")

    # Plot interpolated luminosities
    interpolate_luminosity  = interpolate.interp1d(ages, luminosities)
    age_grid                = ages
    
    # Plot interpolated values
    # lum_interpolated    = interpolate_luminosity(age_grid)
    # plt.plot(age_grid, lum_interpolated, '--')

    # Plot Sun as reference point
    if star_mass == "1.0":
        # Retrieve last color
        c = p[-1].get_color()
        plt.plot(4603, interpolate_luminosity([4603]), 'o', color=c, ms=8)
        plt.annotate('current Sun',
            xy=(4603, interpolate_luminosity([4603])), xycoords='data',
            xytext=(-9, +12), textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='top', color=c)
        
        # Moon-forming impact
        # plt.annotate('', xy=(30, 0.55), xycoords='data', xytext=(100, 0.55), textcoords='data', arrowprops=dict(arrowstyle="|-|, widthA=0.2, widthB=0.2", fc=c, ec=c, linewidth=1.2), horizontalalignment='center', verticalalignment='center')
        # plt.annotate('Moon-forming giant impact', xy=(65, 0.54), xycoords='data', xytext=(0, -5), textcoords='offset pixels', horizontalalignment='center', verticalalignment='top', color=c, fontsize=8)

plt.loglog()
plt.ylabel("Bolometric luminosity ($L/L_{\odot}$)")
plt.xlabel("Time (Myr)")

sns.despine()
# plt.legend(loc='lower left', ncol=4, bbox_to_anchor=(0.0, 1.),
#                               frameon=False, columnspacing=1.6)
plt.legend(loc='upper left', ncol=1, bbox_to_anchor=(1.0, 1.),
           frameon=False, labelspacing=1.8)
plt.tight_layout(pad=0.2, w_pad=0.5, h_pad=0.5) # https://matplotlib.org/users/tight_layout_guide.html

plt.savefig(paths.figures / "luminosity_tracks.pdf")
