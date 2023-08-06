import json

import requests
from h3 import H3CellError
from h3.api.basic_int import h3_is_valid


API_URL = "https://europe-west1-windeurope72-private.cloudfunctions.net/elevations-api"
DEFAULT_RESOLUTION = 12


def get_h3_cell_elevations(cells):
    """Get the elevations of the given H3 cells. The database serving this function is lazily-loaded - an elevation is
    either returned for each cell if it's immediately available or the cell index is returned as part of a list of cell
    indexes to come back for later along with an estimated wait time.

    :param iter(int) cells: the integer indexes of the H3 cells to get the elevations of
    :return dict(int, float), list(int)|None, int|None: cell indexes mapped to their elevations in meters, any cell indexes to request again after the wait time, and the estimated wait time in seconds
    """
    if len(cells) == 0:
        raise ValueError("The number of cells cannot be zero.")

    for cell in cells:
        if not h3_is_valid(cell):
            raise H3CellError(f"{cell} is not a valid H3 cell.")

    response = _get_elevations_from_api({"h3_cells": list(cells)})
    elevations = {int(index): elevation for index, elevation in response["data"]["elevations"].items()}
    elevations_to_get_later = response["data"].get("later")
    estimated_wait_time = response["data"].get("estimated_wait_time")
    return elevations, elevations_to_get_later, estimated_wait_time


def get_coordinate_elevations(coordinates, resolution=DEFAULT_RESOLUTION):
    """Get the elevations of the given latitude/longitude coordinates.

    :param iter(iter(float, float)) coordinates: the latitude/longitude pairs to get the elevations of (in decimal degrees)
    :param int resolution: the H3 resolution level to get the elevations at
    :return dict(tuple(float, float)), float), list(list(float, float))|None, int|None: latitude/longitude coordinates mapped to their elevations in meters, any cell indexes to request again after the wait time, and the estimated wait time in seconds
    """
    _validate_coordinates(coordinates)
    response = _get_elevations_from_api({"coordinates": list(coordinates), "resolution": resolution})

    elevations = {
        tuple(json.loads(coordinate)): elevation for coordinate, elevation in response["data"]["elevations"].items()
    }

    later = response["data"].get("later")
    estimated_wait_time = response["data"].get("estimated_wait_time")
    return elevations, later, estimated_wait_time


def get_h3_cell_elevations_in_polygon(polygon, resolution=DEFAULT_RESOLUTION):
    """Get the elevations of the H3 cells at the given resolution whose centrepoints are within the polygon defined by
    the latitude/longitude coordinate pairs.

    :param iter(iter(float, float)) polygon: the latitude/longitude coordinates that define the points of a polygon (in decimal degrees)
    :param int resolution: the resolution of the cells to get within the polygon
    :return dict(int, float), list(int)|None, int|None: cell indexes mapped to their elevations in meters, any cell indexes to request again after the wait time, and the estimated wait time in seconds
    """
    polygon = list(polygon)
    _validate_coordinates(polygon, "polygon coordinates")

    response = _get_elevations_from_api({"polygon": polygon, "resolution": resolution})
    elevations = {int(index): elevation for index, elevation in response["data"]["elevations"].items()}
    elevations_to_get_later = response["data"].get("later")
    estimated_wait_time = response["data"].get("estimated_wait_time")
    return elevations, elevations_to_get_later, estimated_wait_time


def _get_elevations_from_api(data):
    """Get elevations from the API and raise any errors it returns.

    :param dict data: the data to send to the API
    :raise ValueError: if an error is returned by the API
    :return dict: if there are no errors, the API's response
    """
    response = requests.post(API_URL, json=data)

    if response.status_code != 200:
        raise ValueError(response.text)

    return response.json()


def _validate_coordinates(coordinates, coordinates_name="coordinates"):
    """Check that the given coordinates are not empty or invalid.

    :param list(list(float, float)) coordinates: the coordinates to validate
    :param str coordinates_name: the name to use for the coordinates in the error message
    :raise ValueError: if the coordinates are invalid
    :return None:
    """
    if len(coordinates) == 0 or any(len(coordinate) != 2 for coordinate in coordinates):
        raise ValueError(f"The {coordinates_name} must be an iterable of iterables of length 2 and cannot be empty.")
