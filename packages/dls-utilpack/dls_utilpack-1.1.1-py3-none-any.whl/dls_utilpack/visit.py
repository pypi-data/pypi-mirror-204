import logging
import os
import re
from datetime import datetime
from pathlib import Path


class VisitNotFound(Exception):
    pass


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
def get_visit_year(beamline, visit):
    # Get the visit's year.
    date = datetime.now()
    earliest_year = 2000
    found = False
    for year in range(date.year, earliest_year - 1, -1):
        visit_directory = f"/dls/{beamline}/data/{year}/{visit}"
        if os.path.isdir(visit_directory):
            found = True
            break
    if not found:
        raise VisitNotFound(
            f"could not find visit {visit}"
            f" for any year between {date.year} back to {earliest_year}"
        )

    logger.info(f"visit directory determined to be {visit_directory}")

    return year


# ----------------------------------------------------------------------------------------
def get_xchem_subdirectory(visit):

    # This is the pattern all visits must have.
    pattern = r"^([a-z][a-z][0-9][0-9][0-9][0-9][0-9])[-]([0-9]+)([_].*)?$"

    match = re.search(pattern, visit)

    if not match:
        raise ValueError(
            f'the visit name "{visit}" does not conform to the visit naming convention'
        )

    part1 = match.group(1)
    part2 = match.group(2)

    subdirectory = f"{part1}/{part1}-{part2}"

    return subdirectory


# ----------------------------------------------------------------------------------------
def get_xchem_directory(parent, visit):

    subdirectory = get_xchem_subdirectory(visit)

    full_path = Path(parent) / subdirectory

    if not full_path.is_dir():
        raise RuntimeError(f"the visit directory {str(full_path)} does not exist")

    return str(full_path)
