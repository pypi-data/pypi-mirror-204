# Copyright (C) 2016 ETH Zurich

"""
Tests for `recfast4py` module.
"""

import numpy as np

from recfast4py import recfast


def test_xe_frac(regtest):
    Yp = 0.24
    T0 = 2.725

    Om = 0.26
    Ob = 0.044
    OL = 0.0
    Ok = 0.0
    h100 = 0.71
    Nnu = 3.04
    F = 1.14
    fDM = 0.0

    zarr, Xe_H, Xe_He, Xe, TM = recfast.Xe_frac(
        Yp, T0, Om, Ob, OL, Ok, h100, Nnu, F, fDM
    )
    assert zarr is not None
    assert Xe_H is not None
    assert Xe_He is not None
    assert Xe is not None
    assert TM is not None

    def print_stat(name, values):
        array = np.array(values)
        print("stats for", name, file=regtest)
        print("   shape is %s" % (array.shape,), file=regtest)
        print("   min   is %.5f" % np.min(array), file=regtest)
        print("   max   is %.5f" % np.max(array), file=regtest)
        print("   mean  is %.5f" % np.mean(array), file=regtest)
        print("   std   is %.5f" % np.std(array), file=regtest)

    print_stat("zarr", zarr)
    print_stat("Xe_H", Xe_H)
    print_stat("Xe_He", Xe_He)
    print_stat("Xe", Xe)
    print_stat("TM", TM)
