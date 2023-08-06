from libc.stdlib cimport free, malloc
from libcpp.string cimport string

import os


cdef extern from "recombination.Recfast.h":

    int Xe_frac(double *, double *, double *, double *, double *, double *, int, int)


__doc__ = "A module to compute the recombination.\n"


# see https://stackoverflow.com/questions/19225188/what-method-can-i-use-instead-of-file-in-python
from . import __file__ as __file

here = os.path.dirname(os.path.abspath(__file))

if bytes is not str:
    # for python 3
    here = bytes(here, "utf-8")

cdef public string installPath
installPath = here

cdef int DEBUG = (os.environ.get("DEBUG_RECFAST", "") != "")


def recombination(double Yp, double T0, double Om, double Ob, double OL, double Ok, double h100,
                  double Nnu, double F, double fDM, int flag, int npz, double zstart, double zend):

    cdef double[14] params

    params[0] = npz
    params[1] = zstart
    params[2] = zend
    params[3] = Yp
    params[4] = T0
    params[5] = Om
    params[6] = Ob
    params[7] = OL
    params[8] = Ok
    params[9] = h100
    params[10] = Nnu
    params[11] = F
    params[12] = fDM
    params[13] = flag

    cdef double * results[5]
    cdef double * results_array
    cdef int i

    results_array = <double *>malloc(npz * 5 * sizeof(double))
    if results_array == NULL:
        raise MemoryError()

    for i in range(5):
        results[i] = results_array + i * npz

    cdef err_code = Xe_frac(params, results[0], results[1], results[2], results[3], results[4], 1, DEBUG)

    if err_code:
        raise RuntimeError("Xe_frac returned code %s" % err_code)

    # arrays to lists
    result = tuple([results[i][j] for j in range(npz)] for i in range(5))

    free(results_array)

    return result
