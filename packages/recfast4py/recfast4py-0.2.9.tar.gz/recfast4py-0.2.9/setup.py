#!/usr/bin/env python
# encoding: utf-8

import sys

from setuptools import Extension, setup
from Cython.Build import cythonize

VERSION = "0.2.4"

ext = Extension(
    "recfast4py._recfast",
    sources=[
        "src/recfast4py/_recfast.cpp",
        "src/recfast4py/cosmology.Recfast.cpp",
        "src/recfast4py/evalode.Recfast.cpp",
        "src/recfast4py/recombination.Recfast.cpp",
        "src/recfast4py/ODE_solver.Recfast.cpp",
        "src/recfast4py/DM_annihilation.Recfast.cpp",
        "src/recfast4py/Rec_corrs_CT.Recfast.cpp",
    ],
    extra_compile_args=[
        "-stdlib=libc++",
    ]
    if sys.platform == "darwin"
    else [],
    language='c++',
)

setup(ext_modules=[ext], long_description="")
