# -*- coding: utf-8 -*-
"""
Spin up the imagery API.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from imagery_api import init_app, config


application = init_app()
