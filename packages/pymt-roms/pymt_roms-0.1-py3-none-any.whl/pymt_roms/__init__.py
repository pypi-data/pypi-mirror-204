#! /usr/bin/env python
import pkg_resources

__version__ = pkg_resources.get_distribution("pymt_roms").version


from .bmi import Roms

__all__ = [
    "Roms",
]
