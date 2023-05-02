# -*- coding: utf-8 -*-
"""
Handlers for CRUD operators and other actions for the endpoints defined in the visible
imagery API.

:copyright:
    2023, the AVERT System Team.
:license:
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.html)

"""

from datetime import datetime as dt
import io
import zipfile

from flask import (
    abort,
    current_app as app,
    make_response,
    send_file,
    send_from_directory,
)
from flask.wrappers import Response

from avert_api import db
from .models import Image, ImageSchema


def create(image: Image) -> int:
    """
    Handler for POST requests to the '/api/admin/visible/c' endpoint.

    A new image is defined by a JSON payload containing:
        - A unique image identifier (`image_id`) as a string.
        - A Uniform Resource Locator (`url`) pointing at the image's location in the
          local system, as a string.

    An example request (using the Python `requests` library) to this endpoint looks
    something like:

    ```
    import requests


    image = {"image_id": image_id, "url": url}

    r = requests.post(url="http://localhost:8081/api/admin/visible/c", json=image)
    ```

    Parameters
    ----------
    image: An image to add to the database.

    Returns
    -------
    response_code: 201 on success, 400 on invalid ID, 406 on image exists.

    """

    # Validate posted image ID
    image_id = image.get("image_id")
    if not _valid(image_id):
        abort(400, f"{image_id} is not a valid image ID.")
    vnum, site, *_ = image_id.split(".")[0:4]
    image.setdefault("vnum", vnum)
    image.setdefault("site", site)
    image.setdefault("quality", 0)

    # Check whether image already in database
    existing_image = Image.query.filter(Image.image_id == image_id).one_or_none()
    if existing_image is not None:
        abort(406, f"Image with {image_id} already exists!")

    # Create an Image and add to the database
    new_image = Image(**image)
    db.session.add(new_image)
    db.session.commit()

    return make_response(f"Image with ID {image_id} added successfully.", 201)


def retrieve_image(image_id: str, download=None) -> any:
    """
    Handler for GET requests to the '/api/visible/r/{image_id}' endpoint.

    By default, the image is delivered within the response JSON payload. There is an
    option to download the image directly to the local file storage system.

    Parameters
    ----------
    image_id: ID of the image to retrieve from the database.
    download: Toggle to also download the image.

    Returns
    -------
    image: JSON payload containing the requested image.

    """

    # Validate requested image ID
    if not _valid(image_id):
        abort(400, f"{image_id} is not a valid image ID.")
    vnum, site, year, julday = image_id.split(".")[0:4]
    julday = julday.split("_")[0]

    # Retrieve requested image from database using the image ID
    image = Image.query.filter(Image.image_id == image_id).one_or_none()
    if image is None:
        abort(404, f"No image with ID {image_id} in database!")

    # Configure return payload for direct download, if requested
    kwargs = (
        {"download_name": f"{image_id}.jpg", "as_attachment": True}
        if download == "true"
        else {}
    )

    return send_from_directory(
        directory=(
            f"{app.config['DATA_ARCHIVE_PATH']}/imagery"
            f"/visible/{vnum}/{year}/{site}/{julday}"
        ),
        path=f"{image_id}.jpg",
        mimetype="image/jpeg",
        **kwargs,
    )


def query(**kwargs) -> Response:
    """
    Handler for GET requests to the '/api/visible/r' endpoint.

    By default, the images are delivered within the response JSON payload. There is an
    option to download the images directly to the local file storage system as a zipped
    file.

    Parameters
    ----------
    image_id: ID of the image to retrieve from the database.
    download: Toggle to also download the image.

    Returns
    -------
    zip: JSON payload containing the requested image.

    """

    images = Image.query
    available_keys = Image.__table__.columns.keys()
    available_keys.extend(["search_from", "search_to"])
    for key, value in kwargs.items():
        if key not in available_keys:
            continue
        if key == "search_from":
            filter_time = dt.strptime(value, "%Y-%m-%dT%H:%M")
            images = images.filter(getattr(Image, "timestamp") > filter_time)
        elif key == "search_to":
            filter_time = dt.strptime(value, "%Y-%m-%dT%H:%M")
            images = images.filter(getattr(Image, "timestamp") < filter_time)
        else:
            images = images.filter(getattr(Image, key) == value)

    if kwargs.get("page") is not None:
        images = images.paginate(
            page=kwargs.get("page", 1),
            per_page=kwargs.get("image_count", 12)
        )
        return ImageSchema(many=True).dump(images.items)

    if kwargs.get("download") is None:
        return ImageSchema(many=True).dump(images.all())

    # Set a maximum number of images?
    if images.count() > 100:
        print("Many images - try a more specific query!")

    # Build .zip file with all files that match these criteria
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zf:
        for image in images[:100]:
            # Do some sort of time-stamping here?
            arcname = (
                f"avert_imagery_request/{image.vnum}/"
                f"{image.site}/{image.image_id}.jpg"
            )
            zf.write(image.url, arcname=arcname)
    memory_file.seek(0)

    return send_file(memory_file, download_name="images.zip", as_attachment=True)


def update(image_id: str, image: Image) -> int:
    pass


def delete(image_id: str) -> int:
    """
    Handler for DELETE requests to the '/api/admin/visible/d/{image_id}' endpoint.

    An example request (using the Python `requests` library) to this endpoint looks
    something like:

    ```
    import requests


    image_id = <some_valid_image_id>

    r = requests.delete(url=f"http://localhost:8081/api/admin/visible/d/{image_id}")
    ```

    Parameters
    ----------
    image_id: ID of the image to delete from the database.

    Returns
    -------
    response_code: 200 on success, 400 on invalid ID format, 404 if image not found.

    """

    # Validate requested image ID
    if not _valid(image_id):
        abort(400, f"{image_id} is not a valid image ID.")

    # Retrieve requested image from database using the image ID
    image = Image.query.filter(Image.image_id == image_id).one_or_none()
    if image is None:
        abort(404, f"No image with ID {image_id} in database!")

    db.session.delete(image)
    db.session.commit()

    return make_response(f"Image with ID {image_id} deleted successfully.", 200)


def _valid(image_id: str) -> bool:
    """
    Validates image IDs conform to defined format:

        NN.SSS[SS].YYYY.DDD_hhmmss

    where:
        N: a 6-digit, numeric volcano identifier, e.g. 311240
        S: a 3-,4-, or 5-character, alphanumeric site identifier, e.g. CLNE
        Y: a 4-digit year.
        D: a 3-digit Julian day (day of the year counting from January 1 = 1).
        h: a 2-digit hour.
        m: a 2-digit minute.
        s: a 2-digit second.

    Parameters
    ----------
    image_id: Unique image identifier to be validated.

    Returns
    -------
    valid: True/False assessment of ID validity.

    """

    try:
        vnum, site, year, julday = image_id.split(".")[0:4]
    except ValueError:
        return False

    valid_id = True

    # Validate vnum portion of string
    valid_id &= vnum.isdigit()
    valid_id &= len(vnum) == 6

    # Validate site portion of string
    valid_id &= site.isalnum()
    valid_id &= len(site) == 3 or len(site) == 4 or len(site) == 5

    # Validate year portion of string
    valid_id &= year.isdigit()
    valid_id &= len(year) == 4

    # Validate julday portion of string
    julday = julday.split("_")[0]
    valid_id &= julday.isdigit()
    valid_id &= len(julday) == 3

    return valid_id
