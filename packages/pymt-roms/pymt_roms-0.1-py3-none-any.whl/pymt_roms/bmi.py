from __future__ import absolute_import

import pkg_resources

from bmi_roms import BmiRoms as Roms

Roms.__name__ = "Roms"
Roms.METADATA = pkg_resources.resource_filename(__name__, "data/Roms")

__all__ = [
    "Roms",
]
