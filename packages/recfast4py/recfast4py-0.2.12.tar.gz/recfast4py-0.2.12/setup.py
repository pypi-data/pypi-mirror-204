#!/usr/bin/env python
# encoding: utf-8

import re
import sys

from setuptools import Extension, setup
from Cython.Build import cythonize

ext = cythonize(
    [
        Extension(
            "recfast4py._recfast",
            sources=[
                "src/recfast4py/_recfast.pyx",
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
            language="c++",
        )
    ]
)

for p in ext[0].sources:
    if p.endswith("/_recfast.cpp"):
        with open(p) as fh:
            content = fh.read()
        content = re.sub(
            r"__PYX_EXTERN_C DL_EXPORT\(std::string\) installPath",
            "extern DL_EXPORT(std::string) installPath",
            content,
        )
        with open(p, "w") as fh:
            fh.write(content)


setup(ext_modules=ext, long_description="")
