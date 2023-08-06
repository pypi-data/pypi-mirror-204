"""
This package defines all the node types for building the graph.
"""

from os.path import dirname, basename, isfile, join
import glob
from importlib import import_module
modules = glob.glob(join(dirname(__file__), "*.py"))

__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

l = {}
for m in __all__:
    l[m] = import_module("." + m, "baguette.bakery.source.types")
    del m
locals().update(l)

del glob, dirname, basename, isfile, join, modules, import_module, l