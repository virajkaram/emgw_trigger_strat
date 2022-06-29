from astropy.io import ascii
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from astropy.table import vstack
from glob import glob
from astropy.table import Table
import pickle
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from matplotlib import colors
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib
import sys
# sys.path.append('/Users/viraj/gwemlightcurves')
from gwemlightcurves.KNModels import KNTable
import pickle
from datetime import datetime


def calc_fdets_grid(lim_mag, filt, distance, t_tiling, locfrac=None, plot=False):
    cmap = colors.LinearSegmentedColormap.from_list("", ['ghostwhite', 'cornflowerblue', 'darkblue'])
    labs = ['r', 'J']
    Ds = np.linspace(20, 500, 20)

    tablelist = []
    with open('app/static/bns_Bulla_parameter_grid_%sband.dat' % (filt), 'rb') as f:
        lcs = pickle.load(f)

    peakmags = []
    for row in lcs:
        peakmags.append(np.min(lcs['mag'][0]))
    lcs['peak_mag'] = peakmags
    tablelist.append(lcs)

    # tablelist = [r,J]
    DMs = 5 * np.log10(Ds * 1e5)
    t_covs = np.arange(0, 15, 0.3)

    fig = plt.figure(figsize=(7, 7))
    gs = GridSpec(1, 1, hspace=0.4, wspace=0.3)

    axs = []

    pmarrays = []

    det_fracs = [[], []]

    for ind in range(len(tablelist)):
        t = tablelist[ind]
        t1 = t

        for DM in DMs:
            fdetarray = []
            for t_cov in t_covs:
                mapps = t1['mag'][:, 0] + DM
                t_ind = np.argmin(np.abs(t1[0]['t'] - t_cov))
                m_at_cov = mapps[:, t_ind]
                ndet = np.sum(m_at_cov < lim_mag)
                fdet = ndet / len(m_at_cov)

                fdetarray.append(fdet)
            det_fracs[ind].append(fdetarray)

        det_fracs = np.array(det_fracs)

    t_ind = np.argmin(np.abs(t_covs - t_tiling))
    d_ind = np.argmin(np.abs(Ds - distance))
    fdet = det_fracs[0][d_ind][t_ind]

    plotname = ''
    if plot:
        ax = fig.add_subplot(gs[0])
        im = ax.imshow(det_fracs[0], extent=[t_covs.min(), t_covs.max(), Ds.min(), Ds.max()], origin='lower',
                       aspect=0.026, vmin=0, vmax=1, cmap=cmap, interpolation='bicubic')
        cs = ax.contour(det_fracs[0], [0.1, 0.5, 0.9], colors='black',
                        extent=[t_covs.min(), t_covs.max(), Ds.min(), Ds.max()], origin='lower',
                        linestyles=['--', '-', ':'], linewidth=3)

        ax.set_ylim(80, 450)
        ax.set_xlim(0, 10)
        ax.set_yticks([100, 200, 300, 400])
        ax.set_xticks([0, 2, 4, 6, 8, 10])
        ax.set_ylabel(r'Distance [Mpc]', size=14)
        ax.set_xlabel(r'Time searched [days]', size=14)

        ax.text(4, 400, '%s-band' % (filt), size=15)
        ax.text(4, 380, r'm$_{\rm{lim}} = %s$' % (lim_mag), size=12)
        ax.text(4, 360, r'f$_{\rm{det, lc}}$ = %.2f' % (fdet), size=12)

        if locfrac is not None:
            ax.text(4, 340, r'f$_{\rm{det}} = %.2f x %.2f = %.2f$' % (fdet, locfrac, fdet * locfrac), size=12)
            fdet = fdet * locfrac
        else:
            ax.text(4, 340, r'Localisation probability not specified', size=12)
        # ax2 = ax.twiny()
        # ax2.set_xlim(np.array([0,10])*9*3600/450 * 1)
        # ax2.set_xlabel(r'Area searched with WINTER [deg$^2$]',size=12,labelpad=10)

        # ax.plot(realistic_area90s/(9*3600/450),realistic_distances,'x',color='red',markersize=7)

        ax.plot(t_tiling, distance, '*', color='red', markersize=12)

        ax.tick_params(labelsize=12)
        # ax2.tick_params(labelsize=12)

        ax.plot(0, 0, label=r'f$_{\rm{det}} = 0.1$', color='black', ls='--')
        ax.plot(0, 0, label=r'f$_{\rm{det}} = 0.5$', color='black', ls='-')
        ax.plot(0, 0, label=r'f$_{\rm{det}} = 0.9$', color='black', ls=':')
        ax.legend(fontsize=12)

        ax.tick_params(labelsize=12)
        # ax2.tick_params(labelsize=12)

        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.75])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.set_label(r'Detected fraction (f$_{\rm{det}}$)', size=15)
        cbar.ax.tick_params(labelsize=15, pad=5)

        ax.legend(fontsize=12, loc=1)

        plotname = r'app/static/tloc_dist_comparisons_%s_%s_%s_%s.jpg' % (filt, lim_mag, distance, t_tiling)
        plt.savefig(plotname, bbox_inches='tight')

    return fdet, plotname


def calculate_multiple_fdets(tilingtimes, limmags, exptimes, distance, locfracs_covered=None, filt='J'):
    fdets = []
    imagenames = []
    if locfracs_covered is None:
        locfracs_covered = [None] * len(exptimes)
    for ind in range(len(exptimes)):
        fdet, plotname = calc_fdets_grid(limmags[ind], filt, distance, tilingtimes[ind], locfrac=locfracs_covered[ind],
                                         plot=True)
        fdets.append(fdet)
        imagenames.append('static/' + plotname.split('/')[-1])

    return fdets, imagenames
