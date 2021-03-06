"""
WPS Client library imports.
"""
from __future__ import absolute_import

import logging

import urllib3

urllib3.disable_warnings()

logging.captureWarnings(True)

__version__ = 'devel'

from .errors import *
from .parameter import *
from .dimension import *
from .domain import *
from .gridder import *
from .mask import *
from .named_parameter import *
from .process import *
from .variable import *
from .wps_client import *

NorthernHemisphere = Dimension('latitude', 0, 90)
SouthernHemisphere = Dimension('latitude', -90, 0)
Tropics = Dimension('latitude', -23.4, 23.4)
ArticZone = Dimension('latitude', 66.6, 90.0)
AntarcticZone = Dimension('latitude', -90, -66.6)

T21 = Gridder(grid='gaussian~32')
T42 = Gridder(grid='gaussian~64')
T63 = Gridder(grid='gaussian~96')

UQuart = Gridder(grid='uniform~.25x.25')
UHalf = Gridder(grid='uniform~.5x.5')
U1 = Gridder(grid='uniform~1x1')
U2 = Gridder(grid='uniform~2x2')
