# Copyright (C) 2022 ETH Zurich,
# Institute for Particle Physics and Astrophysics

import redshift_tools as rt
import numpy as np
import os


def _get_abspath(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def test_load():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    assert len(nz) == 5


def test_plot():
    nz, nz_tot = rt.load_bins(_get_abspath("test_bins/example_bins"))
    nz2, nz_tot2 = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.plot_bins(nz)
    rt.plot_bins([nz, nz2])
    rt.plot_bins(nz, nz_tot)
    rt.plot_bins([nz, nz2], [nz_tot, nz_tot2])
    rt.plot_bins(_get_abspath("test_bins/example_bins"), nz_is_path=True)


def test_create():
    nz, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), redshift_dep=False)
    nz2, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), redshift_dep=True)
    nz3, nz_tot = rt.create_bins(5, 0.1 * np.ones(5), alpha=3, beta=0.5, z0=0.5)


def test_shift():
    nz, _ = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.manipulate.shift(nz, np.array([0.1, -0.1, 0, 0.2, -0.2]))
    nz0 = rt.manipulate.shift(nz, np.zeros(5))
    for i in range(len(nz)):
        assert np.all(nz[i] == nz0[i])


def test_stretch():
    nz, _ = rt.load_bins(_get_abspath("test_bins/example_bins"))
    rt.manipulate.stretch(nz, np.array([1.1, 0.9, 1, 1.2, 0.8]))
    nz1 = rt.manipulate.stretch(nz, np.ones(5), normalize=False)
    for i in range(len(nz)):
        assert np.all(nz[i] == nz1[i])
