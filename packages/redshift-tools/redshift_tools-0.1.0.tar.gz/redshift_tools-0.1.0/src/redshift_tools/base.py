#! /usr/bin/env python

# Copyright (C) 2022 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import numpy as np
from scipy.interpolate import interp1d
import PyCosmo
import redshift_tools as rt
from cosmic_toolbox import logger


LOGGER = logger.get_logger(__name__)


def load_bins(path):
    """
    Load the redshift bins from a given path.

    :param path: path to the redshift bins
    :return: list of redshift bins and total redshift distribution
    """
    nz = []
    bins_exists = True
    i = 1
    while bins_exists:
        try:
            nz.append(np.loadtxt(f"{path}_{i}.txt"))
            i += 1
        except Exception:
            LOGGER.info(f"Totally {i-1} bins were found")
            bins_exists = False
    try:
        z_tot = np.loadtxt(f"{path}_tot.txt")
    except Exception:
        LOGGER.warning(f"No total distribution with path {path} found")
        z_tot = None

    assert len(nz) > 0, f"No bins were found at path {path}."
    return nz, z_tot


def lensing_kernel(nz, nz_tot=None, cosmo=None):
    """
    Compute the lensing kernel for a given redshift distribution.

    :param nz: list of redshift distributions
    :param nz_tot: total redshift distribution
    :param cosmo: PyCosmo cosmology instance
    :return: list of lensing kernels for each redshift distribution and total lensing kernel
    """
    return_tot = True
    if nz_tot is None:
        n_tot = rt.manipulate.compute_n_tot(nz)
        nz_tot = np.vstack((nz[0][:, 0], n_tot)).T
        return_tot = False
    if cosmo is None:
        LOGGER.warning("no cosmology specified, standard cosmology is used")
        cosmo = PyCosmo.build()

    w_tot = _get_w(nz_tot, cosmo)
    norm = np.trapz(w_tot, nz_tot[:, 0])
    w_tot = w_tot / norm
    wz_tot = np.vstack((nz_tot[:, 0], w_tot)).T

    wz = []
    for i in range(len(nz)):
        w = _get_w(nz[i], cosmo)
        w = w / norm
        wz.append(np.vstack((nz[i][:, 0], w)).T)

    if return_tot:
        return wz, wz_tot
    return wz


def _get_w(nz, cosmo):
    """
    Compute the lensing kernel for a given redshift distribution.

    :param nz: redshift distribution
    :param cosmo: PyCosmo cosmology instance
    :return: lensing kernel
    """
    obs = PyCosmo.Obs()
    z = nz[:, 0]
    n = nz[:, 1]
    n_call = interp1d(z, n, bounds_error=False, fill_value=0.0)
    a = 1 / (1 + z)
    w = obs._weight_function_lensing(np.flip(a), cosmo, n_call)
    return np.flip(w)
