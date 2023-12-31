#!/usr/bin/env python

import os
import os.path
import shutil
import sys
import urllib.request

DOWNLOAD_URL = "https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES/releases/download/v{MAJOR}.{MINOR}.{PATCH}/{filename}"

FILE_NAME = "{NAME}-config-v{MAJOR}.{MINOR}.{PATCH}_aces-v{ACES_MAJOR}.{ACES_MINOR}_ocio-v{OCIO_MAJOR}.{OCIO_MINOR}.ocio"


def build(source_path, build_path, install_path, targets):
    """Build/Install function.

    Args:
        source_path (str): Path to the rez package root.
        build_path (str): Path to the rez build directory.
        install_path (str): Path to the rez install directory.
        targets (str): Target run by the command, i.e. `build`, `install`...
    """
    package_major, package_minor, package_patch = os.environ.get(
        "REZ_BUILD_PROJECT_VERSION", "0.0.0"
    ).split(".")

    # Variants can be used later if required.
    aces_major, aces_minor = os.environ.get(
        "ACES_VERSION", "1.3"
    ).split(".")
    ocio_major, ocio_minor = os.environ.get(
        "OCIO_VERSION", "2.0"
    ).split(".")

    ocio_file = FILE_NAME.format(
        NAME=os.environ.get("OCIO_CONFIG_NAME", "studio"),
        MAJOR=package_major,
        MINOR=package_minor,
        PATCH=package_patch,
        ACES_MAJOR=aces_major,
        ACES_MINOR=aces_minor,
        OCIO_MAJOR=ocio_major,
        OCIO_MINOR=ocio_minor,
    )
    download_url = DOWNLOAD_URL.format(
        MAJOR=package_major,
        MINOR=package_minor,
        PATCH=package_patch,
        filename=ocio_file
    )
    build_filepath = os.path.join(build_path, "ocio-config.ocio")

    def _build():
        """Build the package locally."""
        with open(build_filepath, "wb") as file:
            with urllib.request.urlopen(download_url) as request:
                file.write(request.read())

    def _install():
        """Install the package."""
        shutil.copy2(build_filepath, install_path)

    _build()

    if "install" in (targets or []):
        _install()


if __name__ == '__main__':
    build(
        source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
        build_path=os.environ['REZ_BUILD_PATH'],
        install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
        targets=sys.argv[1:]
    )
