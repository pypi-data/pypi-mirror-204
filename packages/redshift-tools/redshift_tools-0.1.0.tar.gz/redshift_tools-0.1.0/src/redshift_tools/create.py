#! /usr/bin/env python

# Copyright (C) 2022 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

# package import
import numpy as np
from astropy.convolution import Gaussian1DKernel, convolve_fft
from cosmic_toolbox import logger

LOGGER = logger.get_logger(__name__)


def smail(z, alpha=2.0, beta=2.0, z0=1.13, normalization=1):
    """
    Smail-type function for the overall redshift distribution
    z**alpha * np.exp( -(z/z0)**beta) * normalization

    :param z: redshift
    :param alpha: parameter of the Smail-type distribution
    :param beta: parameter of the Smail-type distribution
    :param z0: parameter of the Smail-type distribution
    :param normalization: normalization of the Smail-type distribution
    :return: Smail-type redshift distribution
    """
    return z**alpha * np.exp(-((z / z0) ** beta)) * normalization


def normalize(y, x):
    """
    Normalize a function to 1

    :param y: function values
    :param x: x values
    :return: normalized function
    """
    return y / np.trapz(y, x)


def find_z_threshold(distribution, n_bins, z_max=5, num_z=10000, **dist_params):
    """
    find redshift thresholds given the overall redshift distribution to split
    the redshift distribution in equally populated bins

    :param distribution: function of redshift for the overall redshift distribution
    :param n_bins: number of bins in which the overall redshift distribution is cut
    :param z_max: maximum redshift
    :param num_z: number of points used for the interpolation
    :param dist_params: parameters of the distribution
    :return: list with the threshold values starting including
        start value (0) and final value (z_max)
    """

    z = np.linspace(0, z_max, num_z)
    nz = normalize(distribution(z, **dist_params), z)
    n_per_bin = 1 / n_bins
    z_threshold = [0]
    i_last_threshold = 0
    for i in range(num_z):
        current_fraction = np.trapz(nz[i_last_threshold:i], z[i_last_threshold:i])
        if current_fraction > n_per_bin:
            z_threshold.append(z[i])
            i_last_threshold = i
    z_threshold.append(z_max)
    return z_threshold


def create_bins(
    n_bins,
    sigma_z,
    max_z=5,
    min_z=0,
    num_z=1000,
    redshift_dep=False,
    z_t=None,
    normalize_bins=True,
    **smail_parameters,
):
    """
    Creates redshift bins following an overall Smail-type distribution

    :param bins: number of bins
    :param sigma_z: array with the photometric_scatter per bin
    :param max_z: maximum redshift
    :param min_z: minimum redshift
    :param num_z: size of the returned redshift array
    :param redshift_dep: boolean if the photometric scatter has a
                         redshift dependence sigma_z*(1+z)
    :param z_t: thresholds for the different bins.
                If None, the thresholds are computed
    :param normalize_bins: If returned bins should be normalized
    :param smail_parameters: paramters that specify the
                             Smail-type distribution
    :return nz: list with num_zx2 arrays with redshift on [:,0]
                and n(z) on [:,1]
    """
    z = np.linspace(min_z, max_z, num_z)
    n_tot = smail(z, **smail_parameters)

    if z_t is None:
        z_t = find_z_threshold(smail, n_bins, max_z, num_z=num_z, **smail_parameters)
        LOGGER.info(
            "No z thresholds given, bins are cut into equally"
            f"populated bins at {z_t}"
        )

    if normalize_bins:
        norm = np.trapz(n_tot, z)
    else:
        norm = 1

    nz = []
    for i in range(n_bins):
        n_i = np.where(np.logical_and(z >= z_t[i], z < z_t[i + 1]), n_tot, 0)
        if redshift_dep:
            n = z_dep_width_convolution(n_i, z, sigma_z[i])
        else:
            n = fixed_width_convolution(n_i, z, sigma_z[i])

        nz.append(np.vstack((z, n / norm)).T)

    nz_tot = np.vstack((z, n_tot / norm)).T

    if normalize_bins:
        norm = np.trapz(n_tot, z)
    return nz, nz_tot


def fixed_width_convolution(n, z, sigma):
    """
    Convolve a redshift distribution with a Gaussian kernel with no redshift dependence.

    :param n: redshift distribution
    :param z: redshift array
    :param sigma: width of the Gaussian kernel
    :return: convolved redshift distribution
    """
    min_z = z[0]
    max_z = z[-1]
    num_z = len(z)

    dz = (max_z - min_z) / num_z
    g = Gaussian1DKernel(sigma / dz)
    n = convolve_fft(n, g)
    return n


def z_dep_width_convolution(n, z, sigma):
    """
    Convolve a redshift distribution with a Gaussian kernel with a redshift dependent width.

    :param n: redshift distribution
    :param z: redshift array
    :param sigma: width of the Gaussian kernel
    :return: convolved redshift distribution
    """
    min_z = z[0]
    max_z = z[-1]
    num_z = len(z)

    new_z = z * (1 + z)
    new_n = np.interp(new_z, z, n)

    dz = (max_z - min_z) / num_z
    g = Gaussian1DKernel(sigma / dz)
    new_n = convolve_fft(new_n, g)

    n = np.interp(z, new_z, new_n)
    return n


def save_bins(nz, path, nz_tot=None):
    """
    Saves redshift bins separetely in .txt files

    :param nz: list of redshift bins with z and n(z)
    :param path: path where to save the file
    """
    n_bins = len(nz)
    for i in range(n_bins):
        np.savetxt(f"{path}_{i+1}.txt", nz[i])
    if nz_tot is not None:
        np.savetxt(f"{path}_tot.txt", nz_tot)
