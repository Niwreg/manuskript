#!/usr/bin/env python
# --!-- coding: utf8 --!--

# The loadSave file calls the proper functions to load and save file
# trying to detect the proper file format if it comes from an older version
import os
import zipfile

import manuskript.load_save.version_0 as v0
import manuskript.load_save.version_1 as v1

import logging
LOGGER = logging.getLogger(__name__)

def saveProject(version=None):

    # While debugging, we don't save the project
    # return

    if version == 0:
        return v0.saveProject()
    else:
        return v1.saveProject()


def clearSaveCache():
    v1.cache = {}


def loadProject(project):

    # Detect version
    isZip = False
    version = 0

    # Is it a zip?
    try:
        zf = zipfile.ZipFile(project)
        isZip = True
    except zipfile.BadZipFile:
        isZip = False

    # Does it have a VERSION in zip root?
    # Was used in transition between 0.2.0 and 0.3.0
    # So VERSION part can be deleted for manuskript 0.4.0
    if isZip and "VERSION" in zf.namelist():
        version = int(zf.read("VERSION"))

    # Does it have a MANUSKRIPT in zip root?
    elif isZip and "MANUSKRIPT" in zf.namelist():
        version = int(zf.read("MANUSKRIPT"))

    # Zip but no VERSION/MANUSKRIPT: oldest file format
    elif isZip:
        version = 0

    # Not a zip
    else:
        with open(project, "r", encoding="utf-8") as f:
            version = int(f.read())

    LOGGER.info("Loading: %s", project)
    LOGGER.info("Detected file format version: {}. Zip: {}.".format(version, isZip))

    if version == 0:
        return v0.loadProject(project)
    else:
        return v1.loadProject(project, zip=isZip)
