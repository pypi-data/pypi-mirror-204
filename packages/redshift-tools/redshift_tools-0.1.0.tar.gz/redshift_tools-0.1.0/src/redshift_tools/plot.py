#! /usr/bin/env python

# Copyright (C) 2022 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import redshift_tools as rt
from cosmic_toolbox import colors


COLORS = list(colors.get_colors().values())


def plot_bins(
    nz,
    nz_tot=None,
    nz_is_path=False,
    colors=COLORS,
    linestyle=["-", ":", "--", "-."],
    figsize=(6, 3),
):
    """
    Plot the redshift bins.

    :param nz: list of redshift distributions
    :param nz_tot: total redshift distribution
    :param nz_is_path: if True, the redshift distributions are loaded from the given paths
    :param colors: list of colors
    :param linestyle: list of linestyles
    :param figsize: figure size
    """

    nz, nz_tot, nz_is_path = _prepare_nz(nz, nz_tot, nz_is_path)
    max_bins = get_max_number_of_bins(nz) + 1
    n_nz = len(nz)

    cc = cycler(linestyle=linestyle[:n_nz]) * cycler(
        color=["k"] + colors[: max_bins - 1]
    )
    mpl.rcParams["axes.prop_cycle"] = cc

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    for nz_i, nz_is_path_i, nz_tot_i in zip(nz, nz_is_path, nz_tot):
        if nz_tot is not None:
            nz_i = [nz_tot_i] + nz_i

        _plot(ax, nz_i, max_bins)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$z$", fontsize=24)
    ax.set_ylabel(r"$n(z)$", fontsize=24)
    ax.set_yticks([])
    ax.tick_params(labelsize=20)


def _prepare_nz(nz, nz_tot, nz_is_path):
    """
    Prepare the redshift distributions for plotting.

    :param nz: list of redshift distributions
    :param nz_tot: total redshift distribution
    :param nz_is_path: if True, the redshift distributions are loaded from the given paths
    :return: list of redshift distributions
    :return: total redshift distribution
    :return: list of bools indicating whether the redshift distributions are paths
    """

    def single(nz):
        return (len(np.shape(nz)) == 3) | isinstance(nz, str)

    if single(nz):
        nz = [nz]
        nz_tot = [nz_tot]
    if not isinstance(nz_is_path, list):
        nz_is_path = len(nz) * [nz_is_path]
    if not isinstance(nz_tot, list):
        nz_tot = len(nz) * [nz_tot]
    nz, nz_tot = _load_all_missing_bins(nz, nz_is_path, nz_tot)

    return nz, nz_tot, nz_is_path


def _plot(ax, nz, max_bins):
    """
    Plot the redshift distributions.

    :param ax: axis
    :param nz: list of redshift distributions
    :param max_bins: maximum number of bins
    """
    for i in range(max_bins):
        try:
            z = nz[i][:, 0]
            n = nz[i][:, 1]
            ax.plot(z, n, zorder=max_bins - i)
        except Exception:
            ax.plot(-1, -1)


def plot_bins_2panels(
    nz_up,
    nz_down,
    nz_tot_up=None,
    nz_tot_down=None,
    nz_up_is_path=False,
    nz_down_is_path=False,
    y_labels=[r"$n(z)$", r"$g(z)$"],
    colors=COLORS,
    linestyle=["-", ":", "--", "-."],
    figsize=(6, 3),
):
    """
    Plot the redshift bins in two panels.

    :param nz_up: list of redshift distributions for the upper panel
    :param nz_down: list of redshift distributions for the lower panel
    :param nz_tot_up: total redshift distribution for the upper panel
    :param nz_tot_down: total redshift distribution for the lower panel
    :param nz_up_is_path: if True, the redshift distributions are loaded from the given paths
    :param nz_down_is_path: if True, the redshift distributions are loaded from the given paths
    :param y_labels: list of y labels
    :param colors: list of colors for the different bins of the redshift distributions
    :param linestyle: list of linestyles for the different bins of the redshift distributions
    :param figsize: figure size
    """
    nz_up, nz_tot_up, nz_up_is_path = _prepare_nz(nz_up, nz_tot_up, nz_up_is_path)
    nz_down, nz_tot_down, nz_down_is_path = _prepare_nz(
        nz_down, nz_tot_down, nz_down_is_path
    )

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=figsize)
    fig.subplots_adjust(hspace=0)

    for i, (nz, nz_tot, nz_is_path) in enumerate(
        zip(
            [nz_up, nz_down],
            [nz_tot_up, nz_tot_down],
            [nz_up_is_path, nz_down_is_path],
        )
    ):
        ax = axs[i]
        max_bins = get_max_number_of_bins(nz) + 1
        n_nz = len(nz)

        cc = cycler(linestyle=linestyle[:n_nz]) * cycler(
            color=["k"] + colors[: max_bins - 1]
        )
        mpl.rcParams["axes.prop_cycle"] = cc

        for nz_i, nz_is_path_i, nz_tot_i in zip(nz, nz_is_path, nz_tot):
            if nz_tot is not None:
                nz_i = [nz_tot_i] + nz_i

            _plot(ax, nz_i, max_bins)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel(r"$z$", fontsize=24)
        ax.set_ylabel(y_labels[i], fontsize=24)
        ax.set_yticks([])
        ax.tick_params(labelsize=20)


def _load_all_missing_bins(nz, nz_is_path, nz_tot):
    """
    Load the redshift distributions from the given paths.

    :param nz: list of redshift distributions
    :param nz_is_path: list of bools indicating whether the redshift distributions are paths
    :param nz_tot: total redshift distribution
    :return: list of redshift distributions
    :return: total redshift distribution
    """
    for i in range(len(nz)):
        if nz_is_path[i]:
            nz[i], nz_tot[i] = rt.load_bins(nz[i])
    return nz, nz_tot


def get_max_number_of_bins(nz):
    """
    Get the maximum number of bins.

    :param nz: list of redshift distributions
    :return: maximum number of bins
    """
    max_bins = 0
    for n in nz:
        if len(n) > max_bins:
            max_bins = len(n)
    return max_bins
