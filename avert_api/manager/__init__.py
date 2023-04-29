# -*- coding: utf-8 -*-
"""
Collection of utility scripts for management of the imagery API. Primarily a repository
of entry points for the imagery API command-line utility.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

import argparse

from .crud import _create, _retrieve, _update, _delete  # NOQA
from .database import _init, _populate  # NOQA


fn_map = {
    "create": _create,
    "retrieve": _retrieve,
    "update": _update,
    "delete": _delete,
    "init": _init,
    "populate": _populate,
}


def main(args=None):
    """Main entry point for the imagery API management CLI tool."""

    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="Specify the mode to run in.",
    )

    # --- Database control section ---
    # Init command
    init_cmd = sub_parser.add_parser("init", help="")
    init_cmd.add_argument(
        "-p",
        "--path",
        help="Path to store initialised database.",
        default="./data/",
    )
    init_cmd.add_argument(
        "-n",
        "--name",
        help="Name for initialised database.",
        default="default",
    )

    # Populate command
    populate_cmd = sub_parser.add_parser("populate", help="")
    populate_cmd.add_argument(
        "-p",
        "--path",
        help="Path to data archive.",
        required=True,
    )
    populate_cmd.add_argument(
        "-d",
        "--database",
        help="Path to database.",
        required=True,
    )

    # --- CRUD operations section ---
    # Create command
    create_cmd = sub_parser.add_parser("create", help="")
    create_cmd.add_argument(
        "-i",
        "--image_id",
        help="Unique identifier for image to be added.",
        required=True,
    )
    create_cmd.add_argument(
        "-u",
        "--url",
        help="Path to image file to be added.",
        required=True,
    )

    # Parse arguments and execute relevant function
    args = parser.parse_args(args)
    fn_map[args.command](args)


if __name__ == "__main__":
    main()
