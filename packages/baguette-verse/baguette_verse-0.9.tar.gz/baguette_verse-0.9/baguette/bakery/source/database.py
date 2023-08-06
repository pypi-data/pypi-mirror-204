from threading import RLock
from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, Optional, Set, Tuple, Type, TypeVar, Union


Scheme = type(List)

T = TypeVar("T")
K = TypeVar("K")


def _check_structure(s : Scheme, t : Any) -> bool:
    if s == t:
        return True
    if not hasattr(s, "__origin__") or s.__origin__ not in (list, tuple, set, Union):
        return False
    return all(_check_structure(si, t) for si in s.__args__)



class View(Generic[K, T]):


    def __init__(self, database : "Database", map : Optional[Callable[[T], K]]) -> None:
        if not isinstance(database, Database):
            raise TypeError("Expected Database type for database, got " + repr(database.__class__.__name__))
        if map != None and not callable(map):
            raise TypeError(repr(map.__class__.__name__) + " object is not callable.")
        self.entries : Dict[K, Tuple[List[T], Set[T]]] = {}
        self.database : Database = database
        self.map = map
        self.refresh()
    

    def close(self):
        self.database = None
    

    def __str__(self) -> str:
        if self.entries:
            for k in self.entries:
                break
            return "View[" + type(k).__name__ + "]"
        return "View[]"
    

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, "database") and self.database == None:
            raise RuntimeError("View has been closed.")
        return super().__setattr__(name, value)
    

    def __delattr__(self, name: str) -> None:
        if name == "database":
            raise AttributeError("Cannot delete reference database.")
        return super().__delattr__(name)
        

    def refresh(self):
        if self.database == None:
            raise RuntimeError("View has been closed.")
        with self.database.lock:
            self.entries = {}
            if self.map != None:
                for t in self.database:
                    try:
                        k = self.map(t)
                    except:
                        from traceback import format_exc
                        raise ValueError("Given mapping function raised an exception for entry {} :\n{}".format(t, format_exc()))
                    if k not in self.entries:
                        try:
                            self.entries[k] = ([], set())
                        except:
                            from traceback import format_exc
                            raise ValueError("Could not use key {} as an entry. It must be hashable :\n{}".format(k, format_exc()))
                    try:
                        self.entries[k][1].add(t)
                    except:
                        self.entries[k][0].append(t)


    def __getitem__(self, i : T) -> K:
        for k, (l, s) in self.entries.items():
            if i in s or i in l:
                return k
        return None
    

    def __setitem__(self, i : T, v : K):
        for k, (l, s) in self.entries.items():
            if i in s:
                s.remove(i)
            elif i in l:
                l.remove(i)
        if v not in self.entries:
            try:
                self.entries[v] = ([], set())
            except:
                raise ValueError("Unhashable type : " + repr(v.__class__.__name__))
        try:
            self.entries[v][1].add(i)
        except:
            self.entries[v][0].append(i)
    

    def values(self):
        return self.entries.keys()
    

    def by_value(self, v : K) -> Iterator[T]:
        if v not in self.entries:
            return iter(())
        from itertools import chain
        return chain(self.entries[v][0], self.entries[v][1])
    

    def by_values(self) -> Iterator[Tuple[K, T]]:
        for k in self.entries:
            for t in self.by_value(k):
                yield k, t





class _Toolbox:
        
        """
        Just a generic function container.
        """



    

class Database(Generic[T]):


    def __init__(self, cls : Type[T], storage_structure : Scheme) -> None:
        if not _check_structure(storage_structure, cls):
            raise TypeError("Structure can only be made of List, Tuple, Set, Union and Target type")
        self.scheme = storage_structure
        self.target = cls
        self.database : Scheme = storage_structure.__origin__()
        self.lock = RLock()
        self.views : Dict[str, View[Any, cls]] = {}
        self.__tools : _Toolbox = _Toolbox()
    

    def clear(self):
        """
        Clears the database.
        """
        with self.lock:
            self.database = self.scheme.__origin__()
            self.views = {}

        
    @property
    def toolbox(self) -> _Toolbox:
        """
        A toolbox full of functions designed to handle this particular database.
        """
        return self.__tools
    

    def __str__(self) -> str:
        return "Database[" + str(self.target) + "]"


    def __iter__(self) -> Iterator[T]:
        def deep_iter(s : Iterable):
            with self.lock:
                for si in s:
                    if isinstance(si, self.target):
                        yield si
                    elif isinstance(si, Iterable):
                        for sii in deep_iter(si):
                            yield sii
        
        return deep_iter(self.database)
    

    def __len__(self) -> int:

        def deep_dumb_iter(s : Iterable):
            if isinstance(s, self.target):
                return 1
            else:
                return sum(deep_dumb_iter(si) for si in s)

        def deep_len(s : Iterable, structure : Scheme):
            with self.lock:
                if structure == self.target:
                    return 1
                if structure.__origin__ in (list, set):
                    if structure.__args__[0] == self.target:
                        return len(s)
                    else:
                        return sum(deep_len(li, structure.__args__[0]) for li in s)
                elif structure.__origin__ == tuple:
                    return sum(deep_len(si, ai) for si, ai in zip(s, structure.__args__))
                else:
                    return deep_dumb_iter(s)
        
        return deep_len(self.database, self.scheme)


    def __dir__(self) -> Iterable[str]:
        return super().__dir__() + list(self.views)
    

    def refresh(self):
        with self.lock:
            for v in self.views.values():
                v.refresh()

    
    def create_view(self, name : str, map : Optional[Callable[[T], K]] = None) -> View[K, T]:
        if not isinstance(name, str):
            raise TypeError("Expected str for view's name, got " + repr(name.__class__.__name__))
        try:
            with self.lock:
                v = View(self, map)
        except:
            raise
        self.views[name] = v
        return v
    

    def remove_view(self, name : str) -> View:
        if name not in self.views:
            raise KeyError("No such view : " + repr(name))
        v = self.views.pop(name)
        v.close()
        return v
    

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name in self.views:
                return self.views[name]
            raise
    

    def __reduce__(self) -> str | tuple[Any, ...]:
        return Database, (self.target, self.scheme), (self.database, self.views, self.__tools)
    
    
    def __setstate__(self, state : Tuple[Scheme, Dict[str, View], toolbox]):
        self.database, self.views, self.__tools = state
