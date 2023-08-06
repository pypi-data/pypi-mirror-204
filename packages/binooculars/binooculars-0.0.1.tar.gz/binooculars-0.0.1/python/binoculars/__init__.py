"""Binoculars: A Python package for machine learning models."""
# ruff: disable=F403
# ruff: disable=F405
from .binoculars import *

__doc__ = binoculars.__doc__
if hasattr(binoculars, "__all__"):
    __all__ = binoculars.__all__
