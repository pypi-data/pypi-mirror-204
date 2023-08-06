"""
This module defines the Vertices and Edges that are related to registry activity.
"""

from ...logger import logger
from typing import Any, Optional, Union
from ..colors import Color
from ..graph import Arrow, Edge, UniqueVertex, Vertex
from .execution import Call, CallHandler, Process
from .network import Host
from .filesystem import File, Directory
from ..utils import chrono
from ..build import BuildingPhase

__all__ = ["Key", "KeyEntry", "HasEntry", "HasSubKey"]





logger.debug("Loading registry library.")

class Key(UniqueVertex):

    """
    A registry key vertex. Represents a key without its associated value(s).
    """

    __slots__ = {
        "__name" : "The local name of the registry key int the registry tree."
    }

    __pickle_slots__ = {
        "name"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional["Vertex"] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.__name : str = ""

    @property
    def name(self) -> str:
        """
        The (local) name of the registry key.
        """
        return self.__name
    
    @name.setter
    def name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("Expected str, got " + repr(type(value).__name__))
        if "\\" in value:
            raise ValueError("'\\' not permitted in a registry key name")
        if len(value) > 255:
            raise ValueError("Key name is too long to be allowed by registry")
        self.__name = value.lower().title().replace("\x00", "\uFFFD")
        if not self.printable:
            from ..config import ColorMap
            from ...logger import logger
            logger.info("Got an unprintable registry key.")
            self.color = ColorMap.get_config().registry.UnprintableKey
    
    @property
    def path(self) -> str:
        """
        The global key name (path from root key and all sub-keys to reach this key included).
        """
        if not self.parent_key:
            return self.name
        return self.parent_key.path + "\\" + self.name

    @property
    def printable(self) -> bool:
        """
        True if the (relative) key name is printable.
        """
        return self.name.isprintable() and "\uFFFD" not in self.name

    @property
    def parent_key(self) -> Union["Key", None]:
        """
        The parent key of this registry key if any (None for root keys).
        """
        for e in self.edges:
            if isinstance(e, HasSubKey) and e.destination is self and isinstance(e.source, Key):
                return e.source
    
    @property
    def entries(self) -> list["KeyEntry"]:
        """
        All the known entries of this key.
        """
        return [e.destination for e in self.edges if isinstance(e, HasEntry)]
    
    @property
    def label(self) -> str:
        """
        The label of this node.
        """
        return "Key " + self.name





class HasSubKey(Arrow):

    """
    This kind of arrow indicates that a key has a sub-key.
    """

    label : str = ""

    source : Host | Key
    destination : Key





class KeyEntry(UniqueVertex):

    """
    A registry key entry vertex. This represents a value (with name, type and actual value) that a registry key has.
    """

    __slots__ = {
        "__name" : "The name of the registry key entry",
        "__type" : "The type of value for this entry",
        "__value" : "The actual value stored in this entry"
    }

    __pickle_slots__ = {
        "name",
        "reg_type",
        "value"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional["Vertex"] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.__name : str = ""
        self.__type : str = ""
        self.__value = None
        self.reg_type = "REG_NONE"

    @property
    def name(self) -> str:
        """
        The name of this registry key entry.
        """
        return self.__name
    
    @name.setter
    def name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("Expected str, got " + repr(type(value).__name__))
        if len(value) > 16383:
            raise ValueError("Registry key value name is too long.")
        self.__name = value
    
    @property
    def reg_type(self) -> str:
        """
        The type of data stored in the registry key entry.
        """
        return self.__type

    @reg_type.setter
    def reg_type(self, value : str):
        if not isinstance(value, str):
            raise TypeError("Expected str, got " + repr(type(value).__name__))
        if value not in {"REG_BINARY", "REG_DWORD", "REG_DWORD_LITTLE_ENDIAN", "REG_DWORD_BIG_ENDIAN", "REG_EXPAND_SZ", "REG_LINK", "REG_MULTI_SZ", "REG_NONE", "REG_QWORD", "REG_QWORD_LITTLE_ENDIAN", "REG_SZ"}:
            raise ValueError("Not a valid type fr registry key : " + str(value))
        self.__type = value
        if self.__type == "REG_NONE":
            self.__value = None
    
    def __setstate__(self, state: dict[str, Any]):
        state = {"reg_type" : state["reg_type"]} | state        # Attribute "reg_type" should be loaded before attribute "value"
        return super().__setstate__(state)
            
    @property
    def value(self) -> bytes | int | str | list[str] | None:
        match self.__type:
            case "REG_BINARY":
                return self.__value
            case "REG_QWORD_LITTLE_ENDIAN" | "REG_DWORD_BIG_ENDIAN" | "REG_DWORD" | "REG_DWORD_LITTLE_ENDIAN" | "REG_QWORD":
                return self.__value
            case "REG_LINK":
                return self.__value
            case "REG_NONE":
                return None
            case "REG_EXPAND_SZ":
                return self.__value
            case "REG_SZ":
                return self.__value
            case "REG_MULTI_SZ":
                return self.__value
            case _:
                raise RuntimeError("Got a KeyEntry with an unknown type : '{}'".format(self.__type))

    @value.setter
    def value(self, val : bytes | int | str | list[str] | None):
        match self.__type:
            case "REG_BINARY":
                if not isinstance(val, bytes):
                    raise TypeError("Expected bytes for key entry of type '{}'".format(self.__type))
            case "REG_QWORD_LITTLE_ENDIAN" | "REG_DWORD_BIG_ENDIAN" | "REG_DWORD" | "REG_DWORD_LITTLE_ENDIAN" | "REG_QWORD":
                if not isinstance(val, int):
                    raise TypeError("Expected int for key entry of type '{}'".format(self.__type))
            case "REG_LINK":
                if not isinstance(val, str):
                    raise TypeError("Expected str for key entry of type '{}'".format(self.__type))
            case "REG_NONE":
                if val != None:
                    raise TypeError("Expected None for key entry of type '{}'".format(self.__type))
            case "REG_EXPAND_SZ":
                if not isinstance(val, str):
                    raise TypeError("Expected str for key entry of type '{}'".format(self.__type))
            case "REG_SZ":
                if not isinstance(val, str):
                    raise TypeError("Expected str for key entry of type '{}'".format(self.__type))
            case "REG_MULTI_SZ":
                if not isinstance(val, list):
                    raise TypeError("Expected list for key entry of type '{}'".format(self.__type))
                for vi in val:
                    if not isinstance(vi, str):
                        raise TypeError("Expected list of str, got an element of type " + repr(type(vi).__name__))
            case _:
                raise RuntimeError("Got a KeyEntry with an unknown type : '{}'".format(self.__type))
        self.__value = val
    
    def process_value(self, val : str | int):
        match self.__type:
            case "REG_LINK" | "REG_EXPAND_SZ" | "REG_SZ":
                if not isinstance(val, str):
                    raise TypeError("Expected str, got " + repr(type(val).__name__))
                self.__value = val
            case "REG_BINARY":
                if not isinstance(val, str):
                    raise TypeError("Expected str, got " + repr(type(val).__name__))
                self.__value = val.encode()
            case "REG_MULTI_SZ":
                if not isinstance(val, str):
                    raise TypeError("Expected str, got " + repr(type(val).__name__))
                if val.endswith("\x00"):
                    v = val[:-1]
                else:
                    v = val
                self.__value = v.split("\x00")
            case "REG_QWORD_LITTLE_ENDIAN" | "REG_DWORD_BIG_ENDIAN" | "REG_DWORD" | "REG_DWORD_LITTLE_ENDIAN" | "REG_QWORD":
                if not isinstance(val, int):
                    raise TypeError("Expected int, got " + repr(type(val).__name__))
                self.__value = val
            case "REG_NONE":
                if not isinstance(val, str):
                    raise TypeError("Expected str, got " + repr(type(val).__name__))
                if val:
                    raise ValueError("Expected empty string, got " + str(val))
                self.__value = None
            case _:
                raise RuntimeError("Got a KeyEntry with an unknown type : '{}'".format(self.__type))
                    
    @property
    def key(self) -> Key:
        """
        The registry Key that this entry is part of.
        """
        for e in self.edges:
            if isinstance(e, HasEntry):
                return e.source
        raise RuntimeError("Found a KeyEntry that has not been affected to a Key")





class HasEntry(Edge):

    """
    This kind of edge indicates that a registry key has one registry entry.
    """

    label : str = ""

    source : Key
    destination : KeyEntry





class Handle(UniqueVertex):

    """
    A handle vertex. Represents a registry key handle, used when a program opens a registry key.
    """

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
    
    @property
    def key(self) -> Key:
        """
        Returns the key node that this handle is working on.
        """
        for e in self.edges:
            if isinstance(e, UsesKey):
                return e.destination
        raise RuntimeError("Key handle with no attached key")
            




class UsesKey(Edge):

    """
    This kind of edge indicates that a handle uses a registry key.
    """

    label : str = ""

    source : Handle
    destination : Key





class HasHandle(Edge):

    """
    This kind of edge indicates that a process owns a registry key handle.
    """

    label : str = ""

    source : Process
    destination : Handle





class Discovered(Arrow):

    """
    This kind of arrow indicates that a key handle discovered a sub-key throught enumeration.
    """

    source : Handle
    destination : Key





class QueriesEntry(Arrow):

    """
    This kind of arrow indicates that a key entry was queried by a key handle. 
    """

    source : KeyEntry
    destination : Handle





class SetsEntry(Arrow):

    """
    This kind of arrow indicates that a key handle set the value of key entry.
    """

    source : Handle
    destination : KeyEntry





class DeletesEntry(Edge):

    """
    This kind of edge indicates that a key handle deleted a key entry.
    """

    source : Handle
    destination : KeyEntry





class ChangesTowards(Arrow):

    """
    This kind of arrow indicates that a key entry's content changed to another.
    """

    label : str = ""

    source : KeyEntry
    destination : KeyEntry





class ReferencesFileSystem(Edge):
    
    """
    This kind of edge indicates that a key's entry references a file or a folder.
    """

    source : KeyEntry
    destination : File | Directory





_existing_keys : dict[str, Key] = {}
_inverted_handles : dict[str, Handle] = {}
_active_handles : dict[Handle, str] = {}
_existing_entries : dict[Key, dict[str, KeyEntry]] = {}
_deleted_entries : dict[Key, dict[str, KeyEntry]] = {}

@chrono
def create_key_tree(key : str) -> Key:
    """
    Creates all the missing keys in leading to the final key and returns the leaf Key node.
    """
    from ..graph import find_or_create
    from .network import Host

    k = None
    last = find_or_create(Host, domain = "host")[0]
    for name in key.replace("\x00", "\uFFFD").split("\\"):
        name = name.lower().title()
        k = None
        for e in last.edges:
            if isinstance(e, HasSubKey) and e.source is last and e.destination.name == name:
                k = e.destination
                break
        if not k:
            k = Key()
            k.name = name
            HasSubKey(last, k)
            _existing_keys[k.path.lower()] = k
        last = k
    
    if not k:
        raise RuntimeError("Trying to create an unnamed registry key!")

    return k

@chrono
def split_key_and_entry_names(path : str) -> tuple[str, str]:       # Might evolve later
    """
    Splits the given key entry path into the path of the last subkey and the name of the entry.
    """
    i = None
    for j, c in enumerate(reversed(path)):
        if c == "\\":
            i = -j - 1
            break
    if i == None:
        raise ValueError("Expected at least one '\\', got " + repr(path))
    return path[:i], path[i + 1:]

@chrono
def find_last_key_entry(key : Key, name : str) -> KeyEntry | None:
    """
    Given a registry key and an entry name, returns the last entry known with this name.
    """
    if key in _existing_entries and name in _existing_entries[key]:
        return _existing_entries[key][name]

    



@chrono
def integrate_key_opening(c : Call):
    """
    Creates a new Key node if necessary when a key is opened.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Opening registry key.")
        if c.arguments.regkey.lower() in _existing_keys:
            k = _existing_keys[c.arguments.regkey.lower()]
        else:
            k = create_key_tree(c.arguments.regkey)
        h = Handle()
        UsesKey(h, k)
        HasHandle(c.thread.process, h)
        if c.arguments.key_handle.lower() in _inverted_handles:
            logger.warning("Opening an already existing registry key handle.")
            return
        _inverted_handles[c.arguments.key_handle.lower()] = h
        _active_handles[h] = c.arguments.key_handle.lower()
        
@chrono
def integrate_key_enumeration(c : Call):
    """
    Finds the enumerated Key and sub-Key. Creates the sub-Key if it does not exist. Links the sub-Key to the Handle.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Enumerating from registry key.")
        k : Key
        sk : Key
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to enumerate a registry key with no known handle.")
            return
        h = _inverted_handles[c.arguments.key_handle.lower()]
        k = h.key
        if c.name != "NtEnumerateKey":
            sk = create_key_tree(k.path + "\\" + c.arguments.key_name)
        else:
            sk = create_key_tree(k.path + "\\" + c.arguments.buffer.encode("utf-8").decode("utf-16", errors="replace"))     # Cuckoo tried its best...which is quite bad!
        Discovered(h, sk)

@chrono
def integrate_key_closing(c : Call):
    """
    Closes a Handle associated with a Key.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Closing key handle.")
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to close unseen key handle.")
            return
        h = _inverted_handles.pop(c.arguments.key_handle.lower())
        _active_handles.pop(h)

@chrono 
def integrate_key_deleting(c : Call):
    """
    Marks a registry Key as deleted.
    """
    from ...logger import logger
    from ..config import ColorMap
    if c.status == 1:
        logger.debug("Deleting registry key.")
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to delete key from unseen handle.")
            return
        k = create_key_tree(c.arguments.regkey)
        k.color = ColorMap.get_config().Deleted
        _existing_keys.pop(k.path.lower())
        if k not in _deleted_entries:
            _deleted_entries[k] = {}
        if k in _existing_entries:
            _deleted_entries[k].update(_existing_entries.pop(k))

@chrono
def integrate_key_value_querying(c : Call):
    """
    Creates a KeyEntry node and marks it as read by thea key Handle.
    """
    from ...logger import logger
    from ..graph import Graph
    if c.status == 1:
        logger.debug("Querying key entry.")
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to query value with unseen key handle.")
            return
        
        # Finding the open key handle :
        h = _inverted_handles[c.arguments.key_handle.lower()]
        k = h.key

        # Finding the last key in the path to the entry :
        if c.name == "NtEnumerateValueKey":
            sk_path, name = split_key_and_entry_names(c.arguments.regkey + "\\" + c.arguments.key_name)
        else:
            sk_path, name = split_key_and_entry_names(c.arguments.regkey)
        sk = create_key_tree(sk_path)

        skp = sk
        while skp:
            if skp is k:
                break
            skp = skp.parent_key
            if not skp:
                logger.warning("There might be an unkown symbolic link in the registry or there is a problem:\nQuerying key '{}' from open key '{}'.".format(sk.path, k.path))

        # Creating a new KeyEntry object
        nv = KeyEntry()
        nv.reg_type = c.flags.reg_type
        nv.process_value(c.arguments.value)
        nv.name = name

        # Looking for an olod value for this entry
        ov = find_last_key_entry(sk, nv.name)
        if not ov or ov.reg_type != nv.reg_type or ov.value != nv.value or (k in _deleted_entries and ov.name in _deleted_entries[k] and _deleted_entries[k][ov.name] is ov):    # New value is the first or is different : link to previous if there is one.
            v = nv
            if ov:
                ChangesTowards(ov, nv)
        else:                                                       # Old value is still good : delete new value.
            v = ov
            for g in Graph.active_graphs():
                g.remove(nv)
        
        if k not in _existing_entries:
            _existing_entries[k] = {}
        _existing_entries[k][v.name] = v
        if v not in sk.neighbors():
            HasEntry(sk, v)
        QueriesEntry(v, h)

@chrono
def integrate_key_value_setting(c : Call):
    """
    Creates a KeyEntry node and marks it as written by a key Handle.
    """
    from ...logger import logger
    from ..graph import Graph
    if c.status == 1:
        logger.debug("Setting key entry.")
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to set value with unseen key handle.")
            return
        
        # Finding the open key handle :
        h = _inverted_handles[c.arguments.key_handle.lower()]
        k = h.key

        # Finding the last key in the path to the entry :
        sk_path, name = split_key_and_entry_names(c.arguments.regkey)
        sk = create_key_tree(sk_path)

        skp = sk
        while skp:
            if skp is k:
                break
            skp = skp.parent_key
            if not skp:
                logger.warning("There might be an unkown symbolic link in the registry or there is a problem:\nSetting key '{}' from open key '{}'.".format(sk.path, k.path))

        # Creating a new KeyEntry object
        nv = KeyEntry()
        nv.reg_type = c.flags.reg_type
        nv.process_value(c.arguments.value)
        nv.name = name

        # Looking for an olod value for this entry
        ov = find_last_key_entry(sk, nv.name)
        if not ov or ov.reg_type != nv.reg_type or ov.value != nv.value or (k in _deleted_entries and ov.name in _deleted_entries[k] and _deleted_entries[k][ov.name] is ov):    # New value is the first or is different : link to previous if there is one.
            v = nv
            if ov:
                ChangesTowards(ov, nv)
        else:                                                       # Old value is still good : delete new value.
            v = ov
            for g in Graph.active_graphs():
                g.remove(nv)
        
        if k not in _existing_entries:
            _existing_entries[k] = {}
        _existing_entries[k][v.name] = v
        if v not in sk.neighbors():
            HasEntry(sk, v)
        SetsEntry(h, v)

@chrono
def integrate_key_value_deleting(c : Call):
    """
    Creates a KeyEntry node and marks it as deleted by a key Handle.
    """
    from ...logger import logger
    from ..graph import Graph
    from ..config import ColorMap
    if c.status == 1:
        logger.debug("Deleting key entry.")
        if c.arguments.key_handle.lower() not in _inverted_handles:
            logger.warning("Trying to set value with unseen key handle.")
            return
        
        # Finding the open key handle :
        h = _inverted_handles[c.arguments.key_handle.lower()]
        k = h.key

        # Finding the last key in the path to the entry :
        sk_path, name = split_key_and_entry_names(c.arguments.regkey)
        sk = create_key_tree(sk_path)

        skp = sk
        while skp:
            if skp is k:
                break
            skp = skp.parent_key
            if not skp:
                logger.warning("There might be an unkown symbolic link in the registry or there is a problem:\nDeleting key '{}' from open key '{}'.".format(sk.path, k.path))

        # Creating a new KeyEntry object
        nv = KeyEntry()
        nv.name = name

        # Looking for an old value for this entry
        ov = find_last_key_entry(sk, nv.name)
        if not ov:                                                  # New value is the first.
            v = nv
        else:                                                       # Old value : link to new value and delete new.
            v = nv
            ChangesTowards(ov, nv)
            nv.reg_type = ov.reg_type
            nv.process_value(ov.value)
            for g in Graph.active_graphs():
                g.remove(nv)
        
        if k not in _existing_entries:
            _existing_entries[k] = {}
        _existing_entries[k][v.name] = v
        if k not in _deleted_entries:
            _deleted_entries[k] = {}
        _deleted_entries[k][v.name] = v
        v.color = ColorMap.get_config().Deleted
        if v not in sk.neighbors():
            HasEntry(sk, v)
        DeletesEntry(h, v)





# Key opening
CallHandler(lambda c : c.name in {"RegOpenKeyExA", "NtOpenKeyEx", "NtOpenKey", "RegOpenKeyExW"}, integrate_key_opening)

# Key creation
CallHandler(lambda c : c.name in {"NtCreateKey", "RegCreateKeyExW", "RegCreateKeyExA"}, integrate_key_opening)

# Key enumeration
CallHandler(lambda c : c.name in {'RegEnumKeyW', 'NtEnumerateKey', 'RegEnumKeyExW', 'RegEnumKeyExA'}, integrate_key_enumeration)

# Key closing
CallHandler(lambda c : c.name in {'RegCloseKey'}, integrate_key_closing)

# Key deleting
CallHandler(lambda c : c.name in {'NtDeleteKey', 'RegDeleteKeyW', 'RegDeleteKeyA'}, integrate_key_deleting)

# Key entry querying
CallHandler(lambda c : c.name in {'NtQueryValueKey', 'RegQueryValueExW', 'RegQueryValueExA', "RegEnumValueW", 'RegEnumValueA', 'NtEnumerateValueKey'}, integrate_key_value_querying)

# Key entry setting
CallHandler(lambda c : c.name in {'RegSetValueExW', 'RegSetValueExA', 'NtSetValueKey'}, integrate_key_value_setting)

# Key entry deleting
CallHandler(lambda c : c.name in {'RegDeleteValueW', 'RegDeleteValueA', 'NtDeleteValueKey'}, integrate_key_value_deleting)





__N_referencing_phase = BuildingPhase.request_finalizing_phase()

def find_filesystem_references(ev : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause all KeyEntry nodes to link to File or Folder nodes that their value reference if these entries were modified.
    """
    from ...logger import logger
    from ..utils import is_path, path_factory, parse_command_line
    from .network import Host
    from .filesystem import File, Directory, Contains, HasDrive
    if ev.major == "Finalizer" and ev.minor == __N_referencing_phase:
        logger.debug("Finding references to filesystem in {} registry key entries.".format(len(KeyEntry)))
        for ke in KeyEntry:

            if ke.reg_type not in {"REG_SZ", "REG_MULTI_SZ"}:
                continue

            ok = False

            for e in ke.edges:
                if isinstance(e, SetsEntry | DeletesEntry):
                    ok = True
                    break
            if not ok:
                continue

            ok = False
            
            if ke.reg_type == "REG_SZ":
                base_possibilities : list[str] = [ke.value]
            else:
                base_possibilities : list[str] = ke.value

            possibilities = []
            for p in base_possibilities:
                try:
                    args = parse_command_line(p)
                    possibilities.extend(args)
                except KeyboardInterrupt:
                    raise
                finally:
                    possibilities.append(p)
            
            for p in possibilities:
                if is_path(p) and p:
                    p = path_factory(p)
                    current : Host | Directory | File = Host.current
                    next : Directory | File | None
                    parts = list(p.parts)
                    if ":" in parts[0]:
                        parts[0] = parts[0].replace("\\", "")
                    for pi in parts:
                        next = None
                        for e in current.edges:
                            if isinstance(e, HasDrive | Contains) and e.source is current and e.destination.name.lower() == pi.lower():
                                next = e.destination
                                break
                        if next is None:
                            break
                        current = next
                    else:
                        ReferencesFileSystem(ke, current)
        
        logger.debug("Got {} references to filesystem points.".format(len(ReferencesFileSystem)))

BuildingPhase.add_callback(find_filesystem_references)




del logger, Optional, Union, Color, Arrow, UniqueVertex, Vertex, Call, CallHandler, Host, Process, File, Directory, Any, chrono, integrate_key_opening, integrate_key_enumeration, integrate_key_closing, integrate_key_deleting, integrate_key_value_querying, integrate_key_value_setting, integrate_key_value_deleting, find_filesystem_references