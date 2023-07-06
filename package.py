name = "ocio_config"

version = "1.0.0"

authors = [
    "ASWF"
]

description = \
    """
    A OCIO Config rez package.
    """

tools = []

requires = []

uuid = "aswf.ocio-config"

build_command = 'python {root}/build.py {install}'

def commands():
    env.OCIO = "{root}/ocio-config.ocio"
