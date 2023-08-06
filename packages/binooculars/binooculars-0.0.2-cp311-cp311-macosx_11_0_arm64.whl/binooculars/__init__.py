"""Binooculars: A Python package for machine learning models."""
# ruff: disable=F403
# ruff: disable=F405
from .binooculars import *

__doc__ = binooculars.__doc__
if hasattr(binooculars, "__all__"):
    __all__ = binooculars.__all__
