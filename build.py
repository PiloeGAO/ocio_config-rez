#!/usr/bin/env python

import os
import os.path
import re
import shutil
import sys
import urllib.request

DOWNLOAD_URL = "https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES/releases/download/{version_tag}/{filename}"

FILE_NAME = "{NAME}-config-v{MAJOR}.{MINOR}.{PATCH}_aces-v{ACES_MAJOR}.{ACES_MINOR}_ocio-v{OCIO_MAJOR}.{OCIO_MINOR}.ocio"

OCIO_VERSION_PACKAGE_REGEX = (
    r"\.?(?P<package>.+)-(?P<major>\d+).(?P<minor>\d+)(.(?P<patch>\d+))?"
)


def get_ocio_version():
    """Get the version of OCIO.

    This will first check for the ephemeral ocio package and then the `$OCIO_VERSION` environement variable.

    Returns:
        tuple(int, int, int): OCIO version numbers.
    """
    rez_variants = os.environ.get("REZ_BUILD_VARIANT_REQUIRES").split(" ")
    for variant in rez_variants:
        match = re.match(OCIO_VERSION_PACKAGE_REGEX, variant)

        if match.group("package") == "ocio":
            return match.group("major"), match.group("minor"), match.group("patch")

    return os.environ.get("OCIO_VERSION", "2.3").split(".")


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
    aces_major, aces_minor = os.environ.get("ACES_VERSION", "1.3").split(".")
    ocio_major, ocio_minor, _ = get_ocio_version()

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

    # This  fix is needed because the release tags are different for versions 2+.
    version_tag = f"v{package_major}-{package_minor}-{package_patch}"
    if int(package_major) == 2 and int(package_minor) in (0, 1):
        version_tag = "v2.0.0-v2.1.0"

    download_url = DOWNLOAD_URL.format(
        version_tag=version_tag,
        filename=ocio_file,
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


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:],
    )
