"""
This module contains configuration objects for execution graphs.
"""

from typing import Any, Type
from .colors import Color
from .graph import Vertex, Edge
from Viper.meta.decorators import hybridmethod





class ColorMap:

    """
    Just a class to hold all basic colors for the graph.
    Create instances to customize!
    """

    __current = None

    default = Color.white

    Deleted = Color(100, 100, 100)

    class execution:
        Process = Color(255, 255, 50)
        Thread = Color(255, 204, 0)
        Call = Color(255, 153, 0)
        HasChildProcess = Color.black
        HasThread = Color.black

    class network:
        Host = Color(255, 255, 255)
        Connection = Color(100, 50, 255)
        Socket = Color.white
        HasProcess = Color.black
        SpawnedProcess = Color.black
    
    network.Socket = Color.average(network.Connection, execution.Process)

    class filesystem:
        File = Color(0, 255, 50)
        Directory = Color(0, 100, 0)
        Handle = Color.white
    
    filesystem.Handle = Color.average(filesystem.File, execution.Process)

    class data:
        Data = Color(0, 255, 150) + Color(150, 0, 255)
        Diff = Color(50, 150, 255)
        DiffLowEntropy = Color(50, 150, 255)
        DiffHighEntropy = Color(255, 50, 150)
    
    class imports:
        Import = Color(150, 150, 0)
        SuspiciousImport = Color(255, 150, 0)
    
    class registry:
        Key = Color(0, 150, 255)
        UnprintableKey = Color(255, 0, 50)
        KeyEntry = Color(0, 255, 255)
        Handle = Color.white

    registry.Handle = Color.average(registry.Key, execution.Process)

    @hybridmethod
    def get_color(self, cls : Type[Vertex] | Type[Edge]) -> Color:
        """
        This function returns the color corresponding to the given class of Vertex or Edge.
        """
        from inspect import getmodule
        try:
            return getattr(getattr(self, getmodule(cls).__name__.split(".")[-1]), cls.__name__)
        except AttributeError:
            return self.default
    
    @hybridmethod
    def has_color(self, cls : Type[Vertex] | Type[Edge]) -> bool:
        """
        This function returns True if the given class of Vertex or Edge has a special color.
        """
        from inspect import getmodule
        try:
            getattr(getattr(self, getmodule(cls).__name__.split(".")[-1]), cls.__name__)
            return True
        except AttributeError:
            return False
        
    @staticmethod
    def get_config() -> Type["ColorMap"] | "ColorMap":
        """
        Returns the globally set ColorMap configuration object.
        """
        return ColorMap.__current
    
    @hybridmethod
    def set_config(self):
        """
        Sets the calling object (class or instance) as the globally used configuration for ColorMap.
        """
        ColorMap.__current = self

ColorMap.set_config()





class SizeMap:

    """
    Just a class to hold all basic sizes for the graph.
    Create instances to customize!
    """

    __current = None

    default = 2.0

    class execution:
        Process = 5.0
        Thread = 2.0
        Call = .3
    
    class network:
        Host = 10.0
        Socket = 2.5
        Connection = 1.5

    class filesystem:
        File = 2.5
        Directory = 2.5
        Handle = 1.5
    
    class data:
        Data = .5
        Diff = 1.5

    class imports:
        Import = 0.75
    
    class registry:
        Key = 1.5
        KeyEntry = 1.0
        Handle = 1.0

    @hybridmethod
    def get_size(self, cls : Type[Vertex]) -> float:
        """
        This function returns the size corresponding to the given class of Vertex.
        """
        from inspect import getmodule
        try:
            return getattr(getattr(self, getmodule(cls).__name__.split(".")[-1]), cls.__name__)
        except AttributeError:
            return self.default
    
    @hybridmethod
    def has_size(self, cls : Type[Vertex]) -> bool:
        """
        This function returns True if the given class of Vertex has a special size.
        """
        from inspect import getmodule
        try:
            getattr(getattr(self, getmodule(cls).__name__.split(".")[-1]), cls.__name__)
            return True
        except AttributeError:
            return False
        
    @staticmethod
    def get_config() -> Type["SizeMap"] | "SizeMap":
        """
        Returns the globally set SizeMap configuration object.
        """
        return SizeMap.__current
    
    @hybridmethod
    def set_config(self):
        """
        Sets the calling object (class or instance) as the globally used configuration for SizeMap.
        """
        SizeMap.__current = self

SizeMap.set_config()





class CompilationParameters:

    """
    This class describes some compilations parameters that some modules may want to use.
    """

    __current = None

    SkipLevenshteinForDataNodes = False
    SkipLevenshteinForDiffNodes = False

    @hybridmethod
    def get_param(self, name : str) -> Any:
        """
        This function returns the parameter corresponding to the given name.
        Raises AttributeError if the parameter does not exist.
        """
        try:
            return getattr(self, name)
        except AttributeError:
            raise AttributeError("No such parameter : " + repr(name))
    
    @hybridmethod
    def has_color(self, name : str) -> bool:
        """
        This function returns True if the given parameter exists.
        """
        try:
            getattr(self, name)
            return True
        except AttributeError:
            return False
    
    @staticmethod
    def get_config() -> Type["CompilationParameters"] | "CompilationParameters":
        """
        Returns the globally set CompilationParameters configuration object.
        """
        return CompilationParameters.__current
    
    @hybridmethod
    def set_config(self):
        """
        Sets the calling object (class or instance) as the globally used configuration for CompilationParameters.
        """
        CompilationParameters.__current = self

CompilationParameters.set_config()