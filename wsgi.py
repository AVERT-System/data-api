# -*- coding: utf-8 -*-
"""
Spin up the imagery API.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from avert_api import init_app


application = init_app()

if __name__ == "__main__":
    application.run(
        host=application.app.config["API_DEV_HOST"],
        port=application.app.config["API_DEV_PORT"],
        debug=True,
    )
