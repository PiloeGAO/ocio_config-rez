name = "ocio_config"

version = "2.1.0"

authors = ["ASWF"]

description = """
    A OCIO Config rez package.
    """

tools = []

requires = []

variants = [
    [".ocio-2.3.0"],
]

uuid = "aswf.ocio-config"

build_command = "python {root}/build.py {install}"


def commands():
    env.OCIO = "{root}/ocio-config.ocio"
