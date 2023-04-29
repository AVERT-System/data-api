# -*- coding: utf-8 -*-
"""
Utility for managing the imagery API database from the command line.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from datetime import datetime as dt
import pathlib
import sqlite3


INFRARED_CONSTRUCTOR = """CREATE TABLE infrared (
                        id INTEGER PRIMARY KEY,
                        image_id TEXT NOT NULL UNIQUE,
                        url TEXT NOT NULL,
                        vnum INTEGER NOT NULL,
                        site TEXT NOT NULL,
                        quality INTEGER NOT NULL,
                        timestamp DATETIME NOT NULL);"""

VISIBLE_CONSTRUCTOR = """CREATE TABLE visible (
                        id INTEGER PRIMARY KEY,
                        image_id TEXT NOT NULL UNIQUE,
                        url TEXT NOT NULL,
                        vnum INTEGER NOT NULL,
                        site TEXT NOT NULL,
                        quality INTEGER NOT NULL,
                        timestamp DATETIME NOT NULL);"""

TABLES = {"INFRARED": INFRARED_CONSTRUCTOR, "VISIBLE": VISIBLE_CONSTRUCTOR}


def _create_connection(db_file: str) -> None:
    """
    Create a new database connection to the SQLite database specified by the
    db_file.

    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Error: {e}.")

    return conn


def _init(args):
    database = pathlib.Path(f"{args.path}") / f"{args.name}.db"

    # --- Create the tables ---
    for _, table_constructor in TABLES.items():
        conn = _create_connection(database)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(table_constructor)
                conn.commit()
                cursor.close()
        except sqlite3.OperationalError as e:
            print(f"Warning: {e} - continuing.")


def _populate(args):
    archive_path = pathlib.Path(args.path)

    conn = _create_connection(args.database)
    with conn:
        cursor = conn.cursor()

        infrared_archive = archive_path / "infrared"
        # Loop over <VNUM>/<YYYY>/<SITE>/<JJJ>/<IMAGE>
        images = infrared_archive.glob("*/*/*/*/*")
        for image in sorted(images):
            if image.is_dir():
                continue
            vnum, site, year, jday_time = image.stem.split(".")
            timestamp = dt.strptime(f"{year}-{jday_time}", "%Y-%j_%H%M%S")

            new_image = {
                "image_id": str(image.stem),
                "url": str(image),
                "vnum": vnum,
                "site": str(site),
                "quality": 0,
                "timestamp": timestamp,
            }
            try:
                print(f"Adding {image.stem} to database...")
                cursor.execute(
                    """
                    INSERT INTO infrared(image_id,url,vnum,site,quality,timestamp)
                    VALUES(?,?,?,?,?,?)
                    """,
                    tuple(new_image.values()),
                )
            except sqlite3.IntegrityError as e:
                if "UNIQUE" in str(e):
                    print("Image already in database, continuing.")
                continue

        visible_archive = archive_path / "visible"
        # Loop over <VNUM>/<YYYY>/<SITE>/hires/<JJJ>/<IMAGE>
        images = visible_archive.glob("*/*/*/*/*")
        for image in sorted(images):
            if image.is_dir():
                continue
            vnum, site, year, jday_time = image.stem.split(".")
            timestamp = dt.strptime(f"{year}-{jday_time}", "%Y-%j_%H%M%S")

            new_image = {
                "image_id": str(image.stem),
                "url": str(image),
                "vnum": vnum,
                "site": str(site),
                "quality": 0,
                "timestamp": timestamp,
            }
            try:
                print(f"Adding {image.stem} to database...")
                cursor.execute(
                    """
                    INSERT INTO visible(image_id,url,vnum,site,quality,timestamp)
                    VALUES(?,?,?,?,?,?)
                    """,
                    tuple(new_image.values()),
                )
            except sqlite3.IntegrityError as e:
                if "UNIQUE" in str(e):
                    print("Image already in database, continuing.")
                continue

        conn.commit()
        cursor.close()
