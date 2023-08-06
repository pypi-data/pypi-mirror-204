import hyclib as lib
from addict import Dict

options = Dict(lib.config.load_package_config('dfdb'))
options.freeze()

del Dict, lib

from .defs import *
from .triggers import *
from .alter import *
from .database import *
from .types import *