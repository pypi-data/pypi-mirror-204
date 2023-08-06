"""
This is the MetaLib! It is a library for MetaGraphs, a pattern storage.

All existing MetaGraphs are loaded with the package.
To create new MetaGraphs, use the module croutons.metalib.interactive.
"""

from ...bakery.logger import logger
from .utils import entries, load

logger.info("Loading MetaGraph library.")

__all__ = []





g = globals()
for name in entries():
    g[name] = load(name)
    __all__.append(name)
    del name





del logger, load, entries, g