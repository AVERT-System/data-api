# -*- coding: utf-8 -*-
"""
Define database Models (tables) for the infrared spectrum imagery.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from avert_api import db, ma


class Image(db.Model):
    __tablename__ = "infrared"
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(32), unique=True)
    url = db.Column(db.String(32))
    vnum = db.Column(db.Integer)
    site = db.Column(db.String(32))
    quality = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, image_id, url, vnum, site, quality, timestamp):
        self.image_id = image_id
        self.url = url
        self.vnum = vnum
        self.site = site
        self.quality = quality
        self.timestamp = timestamp


class ImageSchema(ma.Schema):
    class Meta:
        fields = ("id", "image_id", "url", "vnum", "site", "quality", "timestamp")
