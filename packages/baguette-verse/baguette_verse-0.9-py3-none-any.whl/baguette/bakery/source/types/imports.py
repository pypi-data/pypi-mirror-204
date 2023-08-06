"""
This module defines the Vertices and Edges that are related to importations.
"""

from ...logger import logger
from typing import Optional
from ..colors import Color
from ..graph import Edge, UniqueVertex, Vertex
from .filesystem import NewFile, File
from .execution import Process
from ..utils import chrono

__all__ = ["Import", "HasImport", "IsFile"]





logger.debug("Loading imports library.")

class Import(UniqueVertex):
    
    """
    An import vertex. Shows the use of a DLL or equivalent.
    """

    __slots__ = {
        "__name" : "The name of the import file.",
        "path" : "The path to the file.",
        "length" : "The size in bytes of the file."
    }

    __pickle_slots__ = {
        "name",
        "path",
        "length"
    }

    __suspicious_keyword_names = {
        "crypt",
        "advapi",
        "kernel",
        "sock"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.__name : str = ""
        self.path : str = ""
        self.length : int = 0

    @property
    def name(self) -> str:
        """
        The name of the imported library.
        """
        return self.__name

    @name.setter
    def name(self, n : str):
        from ..config import ColorMap
        if not isinstance(n, str):
            raise TypeError("Expected str, got " + repr(type(n).__name__))
        self.__name = n
        self.color = ColorMap.get_config().imports.Import
        for kw in self.__suspicious_keyword_names:
            if kw in n.lower():
                self.color = ColorMap.get_config().imports.SuspiciousImport
                break
    
    @property
    def label(self) -> str:
        """
        Returns a label for this Import node.
        """
        return "Import {}".format(self.__name.lower())
    




class HasImport(Edge):

    """
    This kind of edge indicates that a process imported something.
    """

    label : str = ""

    source : Process
    destination : Import





class IsFile(Edge):

    """
    This kind of edge indicates that an import corresponds to an existing file object.
    """

    label : str = ""

    source : Import
    destination : File





@chrono
def link(e : NewFile):
    from ..graph import find_or_create
    if e.file.path.suffix.lower().endswith(".dll"):
        I, ok = find_or_create(Import, path = e.file.name)
        if not ok:
            import re
            expr1 = re.compile(r"([a-zA-Z0-9_.]+)(\..*?)$")
            match = expr1.search(e.file.name)
            if match:
                I.name = match.group(1).lower()
            else:
                I.name = e.file.name
        IsFile(I, e.file)

NewFile.add_callback(link)


del logger, Optional, Color, UniqueVertex, Vertex, NewFile, chrono, link