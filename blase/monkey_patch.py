# A monkey patch module to add support for blender file io
# potentially need to load blase after ase

from ase.io.formats import define_io_format, ioformats
from importlib import import_module
import sys

# Step 1: define a new format
define_io_format("blender", "Blender exporter", "1F", module="blender")

# Step 2: dynamically load io
_monkey_mod = import_module("blase.ase_io")

# Step 3: patch system modules
sys.modules["ase.io.blender"] = _monkey_mod
