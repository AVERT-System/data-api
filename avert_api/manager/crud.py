# -*- coding: utf-8 -*-
"""
Utility for peforming CRUD operations on the imagery API from the command line.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

import os
import pathlib

from dotenv import load_dotenv
import requests


_ = load_dotenv(pathlib.Path(__file__).parent.parent / ".flaskenv")

def _create(args):
    image = {"image_id": args.image_id, "url": args.url}

    r = requests.post(
        url=(
            f"http://{os.environ['FLASK_DEV_HOST']}:{os.environ['FLASK_DEV_PORT']}"
            "/api/admin/imagery/infrared/c"
        ),
        json=image
    )

    print(f"{r.json()['status']}: {r.json()['detail']}")


def _retrieve():
    pass


def _update():
    pass


def _delete():
    pass
