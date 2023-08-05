# read version from installed package
from importlib.metadata import version
__version__ = version("testapp_winstonyym")

from .testapp_winstonyym import *