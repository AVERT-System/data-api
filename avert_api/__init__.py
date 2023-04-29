# -*- coding: utf-8 -*-
"""
Application factory for the AVERT Data API.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

import pathlib

import connexion
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Globally accessible libraries
db = SQLAlchemy()
ma = Marshmallow()

basedir = pathlib.Path(__file__).parent.absolute()


def init_app():
    """Initialize the core application."""

    # Create the connexion application instance
    connex_app = connexion.App(
        __name__, specification_dir=pathlib.Path(__file__).parent.absolute()
    )
    connex_app.add_api("api.yml")

    # Get the underlying Flask app instance
    app = connex_app.app

    # Load config from .env and .flaskenv
    _ = load_dotenv(pathlib.Path(__file__).parent / ".env")
    _ = load_dotenv(pathlib.Path(__file__).parent / ".flaskenv")
    app.config.from_prefixed_env()

    # Initialize Plugins
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        return connex_app
