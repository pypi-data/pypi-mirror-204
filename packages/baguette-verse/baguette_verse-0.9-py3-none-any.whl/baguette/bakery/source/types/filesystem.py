"""
This module defines the Vertices and Edges that are related to filesystem activity.
"""

from ...logger import logger
from typing import Optional, Type
from ..colors import Color
from ..graph import Arrow, Edge, UniqueVertex, Vertex, Graph
from .execution import Call, CallHandler, Process
from .network import Host
from ..utils import chrono
from ..event import Event
from ..build import BuildingPhase
import pathlib

__all__ = ["File", "NewFile", "Directory", "Handle", "UsesFile", "UsesDirectory", "Opens", "Closes", "CreatesFile", "CreatesDirectory", "DeletesFile", "DeletesDirectory", "Reads", "Writes", "Conveys", "HasDrive", "HasHandle", "Contains", "IsCopyiedInto"]





logger.debug("Loading file system library.")

class File(UniqueVertex):

    """
    A file vertex. Represents a (real) file opened during execution.
    """

    __slots__ = {
        "__path" : "The path to the file in the file system",
    }

    __pickle_slots__ = {
        "path"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        from pathlib import PurePath
        super().__init__(c=c, parent=parent)
        self.__path : PurePath | None = None

    @property
    def path(self) -> pathlib.PurePath:
        """
        The absolute path to the file.
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        return self.__path

    @path.setter
    def path(self, value : str):
        from ..utils import path_factory
        self.__path = path_factory(value)
    
    @property
    def name(self) -> str:
        """
        The name of the file (tail of the path).
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        return self.__path.name
    
    @property
    def extension(self) -> str:
        """
        The file extention (lowercased without '.').
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        return self.__path.suffix.lower().replace(".", "")
    
    @property
    def label(self) -> str:
        """
        Returns a label for this File node.
        """
        return 'File "' + self.name + '"'
    




class NewFile(Event):

    """
    This is an Event thrown when a File Vertex is created.
    """

    __slots__ = {
        "file" : "The File Vertex of the file that was created"
    }

    def __init__(self, file : File) -> None:
        self.file = file





class Directory(UniqueVertex):

    """
    A directory vertex. Represents a (real) directory opened during execution.
    """

    __slots__ = {
        "__path" : "The path to the directory in the file system",
    }

    __pickle_slots__ = {
        "path"
        }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        from pathlib import PurePath
        super().__init__(c=c, parent=parent)
        self.__path : PurePath | None = None

    @property
    def path(self) -> pathlib.PurePath:
        """
        The absolute path to the directory.
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        return self.__path

    @path.setter
    def path(self, value : str):
        from ..utils import path_factory
        self.__path = path_factory(value)
    
    @property
    def name(self) -> str:
        """
        The name of the directory (tail of the path).
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        return self.__path.name if self.__path.name else self.__path.drive
    
    @property
    def label(self) -> str:
        """
        Returns a label for this Directory node.
        """
        if self.__path is None:
            raise RuntimeError("Got a File without path.")
        if not self.__path.name:
            return 'Drive "' + self.name.replace(":", "") + '"'
        return 'Directory "' + self.name + '"'
    




class Handle(UniqueVertex):

    """
    A handle vertex. Represents a file handle, used when a program opens a file.
    """

    __slots__ = {
        # For all objects:
        "synchronize" : "If the handle can perform synchronization operations on the object",

        # For file objects:
        "read" : "If the handle has the right to read the file",
        "write" : "If the handle has the right to write to the file",
        "append" : "If the handle has the right to append to the file",
        "execute" : "If the handle has the right to execute the file",
        "read_attributes" : "If the handle has the right to read file attributes",
        "write_attributes" : "If the handle can change the file attributes",
        "read_extended_attributes" : "If the handle can read the extended file attributes",
        "write_extended_attributes" : "If the handle can change the extended file attributes",

        # For directory objects:
        "list_directory" : "If the handle has the right to list the items in the given directory",
        "traverse" : "If the handle has the right to traverse the directory and use it to access subforlders/files"
    }

    __pickle_slots__ = {
        "synchronize",
        "read",
        "write",
        "append",
        "execute",
        "read_attributes",
        "write_attributes",
        "read_extended_attributes",
        "write_extended_attributes",
        "list_directory",
        "traverse"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)

        self.synchronize : bool = False

        self.read : bool = False
        self.write : bool = False
        self.append : bool = False
        self.execute : bool = False
        self.read_attributes : bool = False
        self.write_attributes : bool = False
        self.read_extended_attributes : bool = False
        self.write_extended_attributes : bool = False

        self.list_directory : bool = False
        self.traverse : bool = False
    
    @property
    def file(self) -> File | Directory:
        """
        Returns the file (or directory) node that this handle is working on.
        """
        for e in self.edges:
            if isinstance(e, UsesFile | UsesDirectory):
                return e.destination
        raise RuntimeError("Got a Handle working on no File or Directory.")
    




class UsesFile(Edge):

    """
    This kind of edge indicates that a handle uses a file.
    """

    label : str = ""

    source : Handle
    destination : File





class UsesDirectory(Edge):

    """
    This kind of edge indicates that a handle uses a directory.
    """

    label : str = ""

    source : Handle
    destination : Directory





class Opens(Edge):

    """
    This kind of edge indicates that a system call opened a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class Closes(Edge):

    """
    This kind of edge indicates that a system call closed a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class CreatesFile(Edge):

    """
    This kind of edge indicates that a system call created a file through a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class CreatesDirectory(Edge):

    """
    This kind of edge indicates that a system call created a directory through a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class DeletesFile(Edge):

    """
    This kind of edge indicates that a system call deleted a file through a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class DeletesDirectory(Edge):

    """
    This kind of edge indicates that a system call deleted a directory through a handle.
    """

    label : str = ""

    source : Call
    destination : Handle





class Reads(Arrow):

    """
    This kind of arrow indicates that a system call read data from a file.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : "Data"
    destination : Call





class Writes(Arrow):

    """
    This kind of arror indicates that a system call wrote data to a file.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : Call
    destination : "Data"





class Conveys(Arrow):

    """
    This kind of arrow indicates a data flux with a file handle.
    """

    label : str = ""

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : "Handle | Data"
    destination : "Handle | Data"





class HasDrive(Edge):

    """
    This kind of edge indicates that a machine owns a disk drive/partition(/root directory).
    """

    label : str = ""

    source : Host
    destination : Directory





class HasHandle(Edge):

    """
    This kind of edge indicates that a process owns a file handle.
    """

    label : str = ""

    source : Process
    destination : Handle





class Contains(Arrow):

    """
    This kind of arrow indicates that a directory contains a file or another directory.
    """

    label : str = ""

    source : Directory
    destination : Directory | File





class IsCopyiedInto(Arrow):

    """
    This kind indicates that the destination file is a copy of the source file.
    """

    source : File
    destination : File





namespace = locals().copy()
_file_to_dir_cls_table : dict[Type[Arrow | Edge], Type[Arrow | Edge]] = {}
for name, cls in filter(lambda c : isinstance(c[1], type) and issubclass(c[1], Arrow), namespace.items()):
    if name.endswith("File") and name[:-4] + "Directory" in namespace:
        _file_to_dir_cls_table[cls] = namespace[name[:-4] + "Directory"]

_active_handles : dict[Handle, str] = {}
_inverted_handles : dict[str, Handle] = {}
_existing_files : dict[str, File] = {}
_all_files : dict[str, list[File]] = {}

def declare_existing_file(path : str):
    """
    Declares an existing file in the execution environment.
    """
    from ..utils import is_path
    if not isinstance(path, str):
        raise TypeError("Expected str, got " + repr(type(path).__name__))
    if not is_path(path):
        raise ValueError("Expected a valid file path for the execution platform, got " + repr(path))
    f = File()
    f.path = path
    if path not in _all_files:
        _all_files[path] = []
    _all_files[path].append(f)
    _existing_files[path] = f
    NewFile(f).throw()
    

@chrono
def integrate_file_creation(c : Call):
    """
    Creates a File/Directory vertex if it does not exists.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("File created.")
        if c.arguments.file_handle in _inverted_handles:
            h = _inverted_handles[c.arguments.file_handle]
        else:
            h = Handle()
            HasHandle(c.thread.process, h)
        if c.arguments.filepath in _existing_files:
            f = _existing_files[c.arguments.filepath]
            existed = True
        else:
            f = File()
            f.path = c.arguments.filepath
            existed = False
        CreatesFile(c, h)
        if not f in set(h.neighbors()):
            UsesFile(h, f)
        _inverted_handles[c.arguments.file_handle] = h
        _active_handles[h] = c.arguments.file_handle
        _existing_files[c.arguments.filepath] = f
        if c.arguments.filepath not in _all_files:
            _all_files[c.arguments.filepath] = []
        if not existed:
            _all_files[c.arguments.filepath].append(f)
        
        NewFile(f).throw()
        # if "FILE_LIST_DIRECTORY"
        # if "DELETE"
        # if "WRITE_DAC"
        # if "FILE_WRITE_ATTRIBUTES"
        # if "READ_CONTROL"
        # if "FILE_READ_EA"
        # if "FILE_WRITE_DATA"
        # if "FILE_WRITE_EA"
        # if "FILE_APPEND_DATA"
        # if "FILE_READ_ATTRIBUTES"
        # if "GENERIC_WRITE"
        # if "SYNCHRONIZE"
        # if "GENERIC_ALL"
        # if "FILE_READ_DATA" in c.flags.desired_access.split("|"):
        #     h.read = True
        # if "FILE_READ"

@chrono
def integrate_file_opening(c : Call):
    """
    Creates an File/Directory vertex.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("File opened.")
        if c.arguments.file_handle in _inverted_handles:
            h = _inverted_handles[c.arguments.file_handle]
        else:
            h = Handle()
            HasHandle(c.thread.process, h)
        if c.arguments.filepath in _existing_files:
            f = _existing_files[c.arguments.filepath]
            existed = True
        else:
            f = File()
            f.path = c.arguments.filepath
            existed = False
        Opens(c, h)
        if not f in set(h.neighbors()):
            UsesFile(h, f)
        _inverted_handles[c.arguments.file_handle] = h
        _active_handles[h] = c.arguments.file_handle
        _existing_files[c.arguments.filepath] = f
        if c.arguments.filepath not in _all_files:
            _all_files[c.arguments.filepath] = []
        if not existed:
            _all_files[c.arguments.filepath].append(f)

        NewFile(f).throw()

@chrono
def integrate_file_closing(c : Call):
    """
    Connects a closing system call to the corresponding Handle.
    """
    from ...logger import logger
    if c.status == 1 and c.arguments.handle in _inverted_handles:
        logger.debug("File closed.")
        h = _inverted_handles.pop(c.arguments.handle)
        _active_handles.pop(h)
        Closes(c, h)

@chrono
def integrate_file_reading(c : Call):
    """
    Creates a Data vertex, and links it to the Handle and Call vertices.
    """
    from ...logger import logger
    from .data import Data, register_read_operation
    if c.status == 1 and c.arguments.file_handle in _inverted_handles:
        logger.debug("Reading from file.")
        h = _inverted_handles[c.arguments.file_handle]
        d = Data()
        d.time = c.time
        d.set_data(c.arguments.buffer)
        f = h.file
        Reads(d, c)
        Conveys(h, d)
        if isinstance(f, File):
            register_read_operation(f, h, d.data, c.arguments.offset)

@chrono
def integrate_file_writing(c : Call):
    """
    Creates a Data vertex, and links it to the Handle and Call vertices.
    """
    from ...logger import logger
    from .data import Data, register_write_operation
    if c.status == 1 and c.arguments.file_handle in _inverted_handles:
        logger.debug("Writing to file.")
        h = _inverted_handles[c.arguments.file_handle]
        d = Data()
        d.time = c.time
        d.set_data(c.arguments.buffer)
        f = h.file
        Writes(c, d)
        Conveys(d, h)
        if isinstance(f, File):
            register_write_operation(f, h, d.data, c.arguments.offset)
    
@chrono
def integrate_file_copying(c : Call):
    """
    Creates a File vertex, and links it to the original file it was copied from.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Copying file.")
        if c.arguments.oldfilepath in _existing_files:
            fs = _existing_files[c.arguments.oldfilepath]
        else:
            fs = File()
            fs.path = c.arguments.oldfilepath
            _existing_files[c.arguments.oldfilepath] = fs
            if c.arguments.oldfilepath not in _all_files:
                _all_files[c.arguments.oldfilepath] = []
            _all_files[c.arguments.oldfilepath].append(fs)
            NewFile(fs).throw()
        if c.arguments.newfilepath in _existing_files:
            fd = _existing_files[c.arguments.newfilepath]
        else:
            fd = File()
            fd.path = c.arguments.newfilepath
            _existing_files[c.arguments.newfilepath] = fd
            if c.arguments.newfilepath not in _all_files:
                _all_files[c.arguments.newfilepath] = []
            _all_files[c.arguments.newfilepath].append(fd)
            NewFile(fd).throw()
        IsCopyiedInto(fs, fd)

@chrono
def integrate_file_deleting(c : Call):
    # You need to make it possible to have multiple times the same file name...
    from ...logger import logger
    from ..config import ColorMap
    if c.status == 1:
        logger.debug("Deleting file.")
        if c.arguments.filepath not in _existing_files:
            f = File()
            f.path = c.arguments.filepath
            _existing_files[c.arguments.filepath] = f
            if c.arguments.filepath not in _all_files:
                _all_files[c.arguments.filepath] = []
            _all_files[c.arguments.filepath].append(f)
            NewFile(f).throw()
        else:
            f = _existing_files[c.arguments.filepath]
        f.color = ColorMap.get_config().Deleted
        _existing_files.pop(c.arguments.filepath)





# File creation
CallHandler(lambda c : c.name == "NtCreateFile", integrate_file_creation)

# File closing
CallHandler(lambda c : c.name == "NtOpenFile", integrate_file_opening)

# File closing
CallHandler(lambda c : c.name == "NtClose", integrate_file_closing)

# File reading
CallHandler(lambda c : c.name == "NtReadFile", integrate_file_reading)

# File writing
CallHandler(lambda c : c.name == "NtWriteFile", integrate_file_writing)

# File copying
CallHandler(lambda c : c.name in {"CopyFileA", "CopyFileExW", "CopyFileW"}, integrate_file_copying)

# File deleting
CallHandler(lambda c : c.name in {"DeleteFileW", "NtDeleteFile"}, integrate_file_deleting)





_N_phase = BuildingPhase.request_finalizing_phase()

def build_fs_tree(e : BuildingPhase):
    """
    When all File nodes have been created, this will replace those which are actually directories into Directory nodes and build the file system tree.
    """
    # TODO : You will need to make a version of this which keeps track of when files/directories exists to make sure your file system tree is indeed a tree !!!
    from ...logger import logger
    from ..graph import find_or_create
    from .network import Host
    from .execution import Runs
    from ..graph import Graph, Edge
    from pathlib import PurePath
    from typing import Type

    disappearing : set[Type[Edge]] = {Runs}


    def mutate(f : File):
        d = Directory()
        d.path = str(f.path)
        d.size = f.size
        graphs = Graph.active_graphs()
        for e in f.edges.copy():
            src, dst = e.source if e.source is not f else d, e.destination if e.destination is not f else d
            e.delete()
            for g in graphs:
                g.remove(e)
            if type(e) in _file_to_dir_cls_table:
                T = _file_to_dir_cls_table[type(e)]
            else:
                T = type(e)
            if T not in disappearing:
                T(src, dst)
        for g in graphs:
            g.remove(f)
            g.append(d)
        return d
    

    if e.major == "Finalizer" and e.minor == _N_phase:
        logger.debug("Mutating up to {} File nodes.".format(len(File)))

        directories : dict[PurePath, list[Directory]] = {}
        files : dict[PurePath, list[File]] = {}
        for filelist in _all_files.values():
            path = filelist[0].path
            for file in filelist:
                paths = [path] + list(path.parents)
                p = paths.pop(0)
                if p not in files:
                    files[p] = []
                files[p].append(file)
                for dpath in paths:
                    if dpath not in directories:
                        directories[dpath] = []
                
        n = 0
        for path in files.copy():
            if path in directories:
                l = list(mutate(file) for file in files.pop(path))
                directories[path].extend(l)
                n += len(l)
        logger.debug("Actually mutated {} File nodes into Directory Nodes.".format(n))
    
        logger.debug("Creating missing directory nodes.")
        for path, filelist in directories.items():
            if not filelist:
                d = Directory()
                d.path = str(path)
                filelist.append(d)
            
        logger.debug("Building file system graph.")
        work : set[File | Directory] = {f for filelist in files.values() for f in filelist}

        while work:
            node = work.pop()
            path = node.path
            parent = path.parent
            if parent != path:
                for parent_node in directories[parent]:
                    Contains(parent_node, node)
                    work.add(parent_node)
            else:
                HasDrive(find_or_create(Host, domain = "host")[0], node)
        
        # Deleting references to irrelevent (mutated) File nodes
        _existing_files.clear()
        _all_files.clear()
                




# TODO : Add a backtracking phase for actual successive copies of files (those without modifications in between)!!!


BuildingPhase.add_callback(build_fs_tree)


del logger, Optional, Color, Arrow, UniqueVertex, Vertex, Call, CallHandler, BuildingPhase, build_fs_tree, chrono, Event, pathlib, Graph, integrate_file_creation, integrate_file_closing, integrate_file_opening, integrate_file_reading, integrate_file_writing, integrate_file_copying, integrate_file_deleting