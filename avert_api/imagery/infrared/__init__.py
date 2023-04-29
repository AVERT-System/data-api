# -*- coding: utf-8 -*-
"""
Module defining the back-end ReSTful API for the infrared imagery database.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from .operations import (
    create,  # NOQA
    retrieve_image,  # NOQA
    query,  # NOQA
    delete,  # NOQA
)
