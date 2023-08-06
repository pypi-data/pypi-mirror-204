# read version from installed package
from importlib.metadata import version
__version__ = version("testapp_ualsg")

from .testapp_ualsg import *