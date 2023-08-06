"""
This module defines the Vertices and Edges that focus on data interpretation.
"""

from ..config import CompilationParameters
from ...logger import logger
from abc import ABCMeta
from typing import Iterator, Optional
from ..colors import Color
from ..graph import Arrow, Edge, UniqueVertex, Vertex
from ..utils import chrono
from .filesystem import File, Handle
from .network import Socket, Connection
from ..build import BuildingPhase
from typing import Sequence, Hashable, TypeVar

__all__ = ["levenshtein_similarity", "levenshtein_subset_similarity", "entropy", "Data", "IsSimilarTo", "IsAlmostIn", "register_read_operation", "register_write_operation"]





logger.debug("Loading data library.")

S = TypeVar("S", bound=Sequence[Hashable])

@chrono
def levenshtein_similarity(s1 : S, s2 : S, threshold : float = 1.0) -> float:
    """
    Returns the normalized Levenshtein distance (float between 0 and 1) between two strings, where the weight of insertion and deletion operation is the same than the one of substitution.
    If threshold is given, it must be a float representing the minimum value of similarity required to push the calculation to the end. If similarity gets lower, 0 is returned.
    """
    from typing import Sequence
    if not isinstance(s1, Sequence):
        raise TypeError("Expected two Sequences of Hashables, got " + repr(type(s1).__name__) + " and " + repr(type(s2).__name__))
    if not isinstance(s2, type(s1)):
        raise TypeError("Expected two {}s, got {} and {}".format(type(s1).__name__, repr(type(s1).__name__), repr(type(s2).__name__)))
    if not isinstance(threshold, float):
        try:
            threshold = float(threshold)
        except:
            raise TypeError("Expected float for threshold, got " + repr(type(threshold).__name__)) from None
    if not (0 <= threshold <= 1):
        raise ValueError("Threshold must be between zero and one, got " + repr(threshold))
    if not s1 and not s2:
        return 0.0
    if hash(s1) == hash(s2) and s1 == s2:
        return 1.0
    if threshold >= 1.0:
        score_threshold = None
    else:
        score_threshold = round((1 - threshold) * max(len(s1), len(s2)))
    modifier = 1
    from Levenshtein import distance
    s = 1.0 - (distance(s1, s2, weights = (1, 1, modifier), score_cutoff = score_threshold) / max(len(s1), len(s2)))
    if s <= threshold:
        return 0.0
    return s

@chrono
def levenshtein_subset_similarity(s1 : S, s2 : S, threshold : float = 1.0) -> float:
    """
    Returns the normalized Levenshtein distance (float between 0 and 1) between two strings, where the weight of insertion and deletion operation is lower than the one of substitution.
    If threshold is given, it must be a float representing the minimum value of similarity required to push the calculation to the end. If similarity gets lower, 0 is returned.
    """
    from typing import Sequence
    if not isinstance(s1, Sequence):
        raise TypeError("Expected two Sequences of Hashables, got " + repr(type(s1).__name__) + " and " + repr(type(s2).__name__))
    if not isinstance(s2, type(s1)):
        raise TypeError("Expected two {}s, got {} and {}".format(type(s1).__name__, repr(type(s1).__name__), repr(type(s2).__name__)))
    if not isinstance(threshold, float):
        try:
            threshold = float(threshold)
        except:
            raise TypeError("Expected float for threshold, got " + repr(type(threshold).__name__)) from None
    if not (0 <= threshold <= 1):
        raise ValueError("Threshold must be between zero and one, got " + repr(threshold))
    if not s1 and not s2:
        return 0.0
    if hash(s1) == hash(s2) and s1 == s2:
        return 1.0
    if threshold >= 1.0:
        score_threshold = None
    else:
        score_threshold = round((1 - threshold) * max(len(s1), len(s2)))
    modifier = 3
    from Levenshtein import distance
    s = 1.0 - (distance(s1, s2, weights = (1, 1, modifier), score_cutoff = score_threshold) / max(len(s1), len(s2)))
    if s <= threshold:
        return 0.0
    return s

@chrono
def entropy(s : str | bytes | bytearray) -> float:
    """
    Computes the character entropy of the given string.
    """
    if not s:
        return 0.0
    from math import log2
    from collections import Counter
    probabilities = {c : nc / len(s) for c, nc in Counter(s).items()}
    return sum(-p * log2(p) for p in probabilities.values())

@chrono
def printable_rate(s : bytes | bytearray) -> tuple[float, str]:
    """
    Computes the ratio of printable bytes (which can be decoded to the best endoding). Also returns the best probale encoding.
    """
    if not s:
        return 1.0, "raw"

    import codecs
    n_err = 0

    def count(err : UnicodeError) -> tuple[str, int]:
        """
        Adds one to the decoding errors counter and resume normal decoding.
        """
        nonlocal n_err
        n_err += 1
        if isinstance(err, UnicodeDecodeError | UnicodeTranslateError | UnicodeEncodeError):
            return "", err.start + 1
        else:
            raise ValueError("Unknown UnicodeError")
    
    codecs.register_error("count", count)

    best = float("inf")
    best_enc = ""

    # ("utf-8", "ascii", "utf-16", "utf-32", "gbk")

    for enc in ("ascii", ):
        n_err = 0
        codecs.decode(s, enc, "count")
        if n_err < best:
            best = n_err
            best_enc = enc
    
    return (len(s) - best) / len(s), best_enc if best == 0 else "raw"





class Data(UniqueVertex):
    
    """
    A data vertex. Represents data read, written or appended to a file.
    """

    similarity_threshold = 0.75

    __slots__ = {
        "data" : "The bytes data exchanged through the handle",
        "length" : "The length of the data in bytes",
        "entropy" : "The byte-wise entropy of the message",
        "time" : "The time at which this message was seen",
        "isprintable" : "Indicates if a message can be converted to a UTF-8 str and contains only printable characters",
        "__initialized" : "Indicates if this Vertex can be compared to other Data Vertices"
    }

    __pickle_slots__ = {
        "data",
        "length",
        "entropy",
        "time",
        "isprintable"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.__initialized = False
        self.data : bytes = b""
        self.length : int = 0
        self.entropy : float = 0.0
        self.time : float = 0.0
        self.isprintable : bool = False
    
    @property
    def vector(self) -> Handle | Socket:
        """
        The Handle or Socket Vertex that this Data node is Conveying data to or from.
        """
        from .filesystem import Handle
        from .network import Socket
        for u in self.neighbors():
            if isinstance(u, Handle | Socket):
                return u
        raise RuntimeError("Got a data node without vector.")
    
    @chrono
    def set_data(self, data : str):
        """
        Writes the corresponding data to the node.
        Also computes all related metrics.
        """
        self.data = data.encode("utf-8")
        self.length = len(self.data)
        self.entropy = entropy(self.data)
        self.isprintable = data.isprintable()
    
    def compare(self):
        """
        Links the node to other similar nodes.
        """
        self.__initialized = True
        for d in Data:
            if (1 - Data.similarity_threshold) * max(len(d.data), len(self.data)) < abs(len(d.data) - len(self.data)):      # Size difference is too high, similarity will be below threshold
                continue
            if d is not self and d.__initialized:
                s1 = levenshtein_similarity(d.data, self.data, Data.similarity_threshold)
                if s1 < Data.similarity_threshold:
                    continue
                if self.time < d.time:
                    l1 = IsSimilarTo(self, d)
                else:
                    l1 = IsSimilarTo(d, self)
                l1.weight = s1
                # s2 = levenshtein_subset_similarity(d.data, self.data)
                # if self.time < d.time:
                #     l2 = IsAlmostIn(self, d)
                # else:
                #     l2 = IsAlmostIn(d, self)
                # l2.weight = s2

__N_data_comparison_phase = BuildingPhase.request_finalizing_phase()

@chrono
def finalize_data_nodes(e : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause all Data nodes to link themselves to similar Data nodes.
    """
    from ...logger import logger
    from ..config import CompilationParameters
    from time import time_ns
    from Viper.format import duration
    if e.major == "Finalizer" and e.minor == __N_data_comparison_phase:
        if CompilationParameters.get_config().SkipLevenshteinForDataNodes:
            return
        logger.debug("Finalizing {} Data nodes.".format(len(Data)))
        d : Data
        n = len(Data)
        t0 = time_ns()
        t = t0
        for i, d in enumerate(Data):
            d.compare()
            if (time_ns() - t) / 1000000000 > 15:
                t = time_ns()
                logger.debug("Finalizing {} Data nodes : {:.2f}%. ETA : {}".format(len(Data), (i + 1) / n * 100, duration(round((t - t0) / (i + 1) * (n - i - 1)))))

BuildingPhase.add_callback(finalize_data_nodes)





class IsSimilarTo(Arrow):

    """
    This kind of arrow indicates two Data nodes have a similar content. The direction of the arrow indicates the order of apparition.
    """

    label : str = ""

    source : Data
    destination : Data





class IsAlmostIn(Arrow):

    """
    This kind of arrow indicates that a Data node's content might be contained in another's one. The direction of the arrow indicates the order of apparition.
    """

    label : str = ""

    source : Data
    destination : Data





class DiffFile:

    """
    These objects are abstract/virtual files in which you can perform IO operations at any place.
    """

    def __init__(self) -> None:
        self.__offsets : list[int] = list()
        self.__arrays : list[bytearray] = list()
        self.__last_dump : bytes | None = None
        self.__computation_index : int = 0
        self.__last_computation_index : int = -1
    
    def arrays(self) -> Iterator[tuple[int, bytes]]:
        """
        Yields all the successives entries in the DiffFile in the form (offset, buffer).
        """
        yield from zip(self.__offsets, self.__arrays)

    @chrono
    def write(self, data : bytes, offset : int):
        """
        Writes a new block of data in the virtual diff file.
        """
        if not isinstance(data, bytes | bytearray | memoryview) or not isinstance(offset, int):
            raise TypeError("Expected readable buffer and int, got " + repr(type(data).__name__) + " and " + repr(type(offset).__name__))
        # First, insert the new block in the right place
        data = bytearray(data)
        for i, (o, a) in enumerate(self.arrays()):
            if offset <= o:
                break
        else:
            i = len(self.__offsets)
        self.__offsets.insert(i, offset)
        self.__arrays.insert(i, data)
        # Second, operate all the possible merges
        end = offset + len(data)
        old_data = bytearray(len(data))
        j = i + 1
        while j < len(self.__offsets):
            o, a = self.__offsets[j], self.__arrays[j]
            if o > end:
                break
            old_data[o - offset : o - offset + len(a)] = a
            j += 1
        old_data[:len(data)] = data
        self.__arrays[i] = old_data
        # Delete useless upcoming blocks
        for k in range(i + 1, j):
            self.__offsets.pop(i + 1)
            self.__arrays.pop(i + 1)
        # Eventually merge with previous block
        if i > 0 and self.__offsets[i - 1] + len(self.__arrays[i - 1]) >= offset:
            self.__offsets.pop(i)
            self.__arrays.pop(i)
            o, a = self.__offsets[i - 1], self.__arrays[i - 1]
            a[offset - o : offset - o + len(old_data)] = old_data
        self.__computation_index += 1
    
    @chrono
    def dump(self) -> bytes:
        """
        Returns a dump of the file content. Any empty space will be represented by '[N bytes]'.
        """
        if self.__last_computation_index != self.__computation_index:
            last_end = self.__offsets[0] if self.__offsets else 0
            d = bytearray()
            for o, a in self.arrays():
                if last_end < o:
                    d.extend("[{} bytes]".format(o - (last_end + len(a))).encode("utf-8"))
                d.extend(a)
                last_end = o + len(a)
            self.__last_computation_index = self.__computation_index
            self.__last_dump = bytes(d)
            return self.__last_dump
        else:
            if self.__last_dump is None:
                raise RuntimeError("Got an empty DiffFile dump, whereas it was marked as updated")
            return self.__last_dump





class IOOperation(metaclass = ABCMeta):

    """
    This class represents a Diff vertex atomic operation in its operation log.
    """

    def __init__(self, offset : int, data : bytes) -> None:
        self.__offset = offset
        self.__data = data
    
    @property
    def start(self) -> int:
        """
        The place in the file where this buffer starts.
        """
        return self.__offset
    
    @property
    def stop(self) -> int:
        """
        The place in the file where this buffer ends.
        """
        return self.__offset + len(self.__data)
    
    @property
    def data(self) -> bytes:
        """
        The content of the buffer.
        """
        return self.__data

    



class Read(IOOperation):

    """
    This is a single read operation in a Diff Vertex log.
    """





class Write(IOOperation):

    """
    This is a single write operation in a Diff Vertex log.
    """

    



class Diff(UniqueVertex):

    """
    A diff vertex. This represents all the information gathered on a file's content during the lifetime of a handle.
    """

    similarity_threshold = 0.90

    __slots__ = {
        "read" : "The content of the read diff file",
        "read_type" : "The file type determined by libmagic from what has been read",
        "written" : "The content of the write diff file",
        "written_type" : "The file type determined by libmagic from what has been written",
        "glob" : "The content of the global diff file",
        "glob_type" : "The file type determined by libmagic from the final state of the file",
        "read_total" : "The total amount of bytes that were read",  # Counts double if you read twice the same byte
        "read_space" : "The amount of bytes that were read in the file",    # This one only counts one
        "written_total" : "The total amount of bytes that were written",
        "written_space" : "The amount of bytes that were written in the file",
        "glob_space" : "The amount of bytes that were accessed in the file",
        "read_entropy" : "The amount of entropy that was read from the file",
        "written_entropy" : "The amount of entropy that was written to the file",
        "glob_entropy" : "The entropy that resulted in the file from all operations",
        "printable_rate" : "Indicates how much of the final state of the file only contains printable characters",
        "encoding" : "A valid encoding for the final file",
        "__initialized" : "Indicates if this Vertex can be compared to other Diff Vertices",
        "__reader_difffile" : "The DiffFile that will store the result of all reading operations",
        "__writer_difffile" : "The DiffFile that will store the result of all writing operations",
        "__glob_difffile" : "The DiffFile that will store the result of all IO operations",
        "__operations" : "The list of all operations that appear in the Diff node"
    }

    __pickle_slots__ = {
        "read",
        "read_type",
        "written",
        "written_type",
        "glob",
        "glob_type",
        "read_total",
        "read_space",
        "written_total",
        "written_space",
        "glob_space",
        "read_entropy",
        "written_entropy",
        "glob_entropy",
        "printable_rate",
        "encoding",
    }

    _active_target_diff : dict[File | Connection, "Diff"] = {}
    _active_vector_diff : dict[Handle | Socket, "Diff"] = {}

    def __init__(self, *, c: Color | None = None, parent: Optional["Vertex"] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.__initialized : bool = False
        self.__reader_difffile = DiffFile()
        self.__writer_difffile = DiffFile()
        self.__glob_difffile = DiffFile()
        self.__operations : list[IOOperation] = []
        self.read : bytes = b""
        self.read_type : list[str] = []
        self.written : bytes = b""
        self.written_type : list[str] = []
        self.glob : bytes = b""
        self.glob_type : list[str] = []
        self.read_total : int = 0
        self.read_space : int = 0
        self.written_total : int = 0
        self.written_space : int = 0
        self.glob_space : int = 0
        self.read_entropy : float = 0.0
        self.written_entropy : float = 0.0
        self.glob_entropy : float = 0.0
        self.printable_rate : float = 0.0
        self.encoding : str = "raw"

    @property
    def read_buffer(self) -> bytes:
        """
        The current content of the read diff file.
        """
        return self.__reader_difffile.dump()
    
    @property
    def write_buffer(self) -> bytes:
        """
        The current content of the write diff file.
        """
        return self.__writer_difffile.dump()
    
    @property
    def glob_buffer(self) -> bytes:
        """
        The current content of the global diff file.
        """
        return self.__glob_difffile.dump()
    
    @property
    def content(self) -> tuple[bytes, bytes, bytes]:
        """
        The current content of the read, write and global diff files.
        """
        return self.read_buffer, self.write_buffer, self.glob_buffer
        
    def last_pos(self) -> int:
        """
        Returns the offset after the las operation performed in this Diff node.
        """
        if self.__operations:
            return self.__operations[-1].stop
        else:
            return 0
    
    @chrono
    def add_operation(self, op : IOOperation):
        """
        Registers a new IO operation to this Diff node.
        """
        self.__operations.append(op)
        self.__glob_difffile.write(op.data, op.start)
        if isinstance(op, Read):
            self.__reader_difffile.write(op.data, op.start)
        elif isinstance(op, Write):
            self.__writer_difffile.write(op.data, op.start)
    
    @chrono
    def compute_data(self):
        """
        Computes the values of all the attributes given the state of operations and DiffFiles.
        """
        from magic import Magic
        from ...logger import logger
        from ..config import CompilationParameters
        from ..graph import Graph

        analyzer = Magic(keep_going=True, uncompress=True)
        r, w, g = self.content
        self.read, self.written, self.glob = r, w, g
        self.read_type = analyzer.from_buffer(r).split("\\012- ")
        self.written_type = analyzer.from_buffer(w).split("\\012- ")
        self.glob_type = analyzer.from_buffer(g).split("\\012- ")
        self.read_total = sum(len(op.data) for op in self.__operations if isinstance(op, Read))
        self.written_total = sum(len(op.data) for op in self.__operations if isinstance(op, Write))
        self.read_space = len(r)
        self.written_space = len(w)
        self.glob_space = len(g)
        self.read_entropy = entropy(r)
        self.written_entropy = entropy(w)
        self.glob_entropy = entropy(g)
        self.printable_rate, self.encoding = printable_rate(g)

        if not r and w:
            for e in self.edges:
                if isinstance(e, IsDiffOf):
                    WritesInto(e.source, e.destination)
                    e.delete()
                    for G in Graph.active_graphs():
                        G.remove(e)
        elif not w and r:
            for e in self.edges:
                if isinstance(e, IsDiffOf):
                    IsReadBy(e.destination, e.source)
                    e.delete()
                    for G in Graph.active_graphs():
                        G.remove(e)

        if CompilationParameters.get_config().SkipLevenshteinForDiffNodes:
            return
        
        for u in Diff:
            if u not in self.neighbors() and u is not self:
                lw, ls, ld = 0.0, "", ""
                for sn, sb in zip(("read_buffer", "write_buffer", "global_buffer"), (r, w, g)):
                    if sb:
                        for un, ub in zip(("read_buffer", "write_buffer", "global_buffer"), u.content):
                            if (1 - Diff.similarity_threshold) * max(len(sb), len(ub)) < abs(len(sb) - len(ub)):      # Size difference is too high, similarity will be below threshold
                                continue
                            if ub:
                                s = levenshtein_similarity(sb, ub, Diff.similarity_threshold)
                                if s >= lw:
                                    lw = s
                                    ls = sn
                                    ld= un
                if ls and lw >= Diff.similarity_threshold:      # Heuristic is not perfect : checking that the threshold has indeed been reached!
                    l = HasSimilarContent(self, u)
                    l.weight = lw
                    l.source_buffer = ls
                    l.destination_buffer = ld
    
    @property
    def label(self) -> str:
        """
        The name of the node to display. It is the global data type.
        """
        if len(self.glob_type) == 1:
            return self.glob_type[0]
        return " | ".join(t for t in self.glob_type if t != "data")

    @property
    def vectors(self) -> Iterator[Handle | Socket]:
        """
        The Handle or Socket Vertices that this Diff node is interacting with.
        """
        from .filesystem import Handle
        from .network import Socket
        for u in self.neighbors():
            if isinstance(u, Handle | Socket):
                yield u
    
    @property
    def targets(self) -> Iterator[File | Connection]:
        """
        The File or Connection Vertices that this Diff node is interacting with.
        """
        from .filesystem import File
        from .network import Connection
        for u in self.neighbors():
            if isinstance(u, File | Connection):
                yield u





class IsDiffOf(Edge):

    """
    This kind of edge indicates that a Diff node sums up operations performed on the destination node.
    """

    label : str = ""

    source : File | Connection | Handle | Socket
    destination : Diff





class IsReadBy(Arrow):

    """
    This kind of arrow indicates that a Diff node only read from a vector.
    """

    source : Diff
    destination : File | Connection | Handle | Socket





class WritesInto(Arrow):

    """
    This kind of arrow indicates that a Diff node only wrote to a vector.
    """

    source : File | Connection | Handle | Socket
    destination : Diff





class HasSimilarContent(Edge):

    """
    This kind of arrow indicates that two Diff nodes have buffers with a certain similarity rate.
    """

    __slots__ = {
        "__source_buffer" : "The name of the buffer of the source node that the similarity was computed with.",
        "__destination_buffer" : "The name of the buffer of the destination node that the similarity was computed with."
    }

    __pickle_slots__ = {
        "source_buffer",
        "destination_buffer"
    }

    label : str = ""

    source : Diff
    destination : Diff

    def __init__(self, source: Vertex, destination: Vertex, *, c: Color | None = None, auto_write: bool = True) -> None:
        super().__init__(source, destination, c=c, auto_write=auto_write)
        self.__source_buffer = "global_buffer"
        self.__destination_buffer = "global_buffer"
        
    @property
    def source_buffer(self) -> str:
        """
        Returns the name of the content selected for comparison in the source node.
        """
        return self.__source_buffer
    
    @source_buffer.setter
    def source_buffer(self, name : str):
        if name not in ("read_buffer", "write_buffer", "global_buffer"):
            raise ValueError("Diff node buffers can only be set to one of ('read_buffer', 'write_buffer', 'global_buffer')")
        self.__source_buffer = name
    
    @property
    def destination_buffer(self) -> str:
        """
        Returns the name of the content selected for comparison in the destination node.
        """
        return self.__destination_buffer
    
    @destination_buffer.setter
    def destination_buffer(self, name : str):
        if name not in ("read_buffer", "write_buffer", "global_buffer"):
            raise ValueError("Diff node buffers can only be set to one of ('read_buffer', 'write_buffer', 'global_buffer')")
        self.__destination_buffer = name





@chrono
def register_read_operation(target : File | Connection, vector : Handle | Socket, content : bytes | bytearray | memoryview | str, offset : int | None = None):
    """
    Registers a read operation to be added to the corresponding DiffNodes.
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    if target not in Diff._active_target_diff:
        t = Diff()
        IsDiffOf(t, target)
        Diff._active_target_diff[target] = t
    else:
        t = Diff._active_target_diff[target]
    if vector not in Diff._active_vector_diff:
        v = Diff()
        IsDiffOf(v, vector)
        Diff._active_vector_diff[vector] = v
    else:
        v = Diff._active_vector_diff[vector]
    
    if offset == None:
        t.add_operation(Read(t.last_pos(), content))
        v.add_operation(Read(v.last_pos(), content))
    else:
        t.add_operation(Read(offset, content))
        v.add_operation(Read(offset, content))

@chrono
def register_write_operation(target : File | Connection, vector : Handle | Socket, content : bytes | bytearray | memoryview | str, offset : int | None = None):
    """
    Registers a write operation to be added to the corresponding DiffNodes.
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    if target not in Diff._active_target_diff:
        t = Diff()
        IsDiffOf(t, target)
        Diff._active_target_diff[target] = t
    else:
        t = Diff._active_target_diff[target]
    if vector not in Diff._active_vector_diff:
        v = Diff()
        IsDiffOf(v, vector)
        Diff._active_vector_diff[vector] = v
    else:
        v = Diff._active_vector_diff[vector]
    
    if offset == None:
        t.add_operation(Write(t.last_pos(), content))
        v.add_operation(Write(v.last_pos(), content))
    else:
        t.add_operation(Write(offset, content))
        v.add_operation(Write(offset, content))

__N_diff_comparison_phase = BuildingPhase.request_finalizing_phase()
__N_diff_normalization_phase = BuildingPhase.request_finalizing_phase()
__N_diff_fusion_phase = BuildingPhase.request_finalizing_phase()
        

@chrono
def finalize_diff_nodes(e : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause all Diff nodes to compute their data attributes.
    """
    from ...logger import logger
    from time import time_ns
    from ..config import CompilationParameters
    from Viper.format import duration
    if e.major == "Finalizer" and e.minor == __N_diff_comparison_phase:
        logger.debug("Finalizing{} {} Diff nodes.".format(" and comparing" if not CompilationParameters.get_config().SkipLevenshteinForDiffNodes else "",len(Diff)))
        n = len(Diff)
        t0 = time_ns()
        t = t0
        for i, d in enumerate(Diff):
            d.compute_data()
            if (time_ns() - t) / 1000000000 > 15:
                t = time_ns()
                logger.debug("Finalizing {} Diff nodes : {:.2f}%. ETA : {}".format(len(Data), (i + 1) / n * 100, duration(round((t - t0) / (i + 1) * (n - i - 1)))))

@chrono
def normalize_diff_nodes(e : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause all Diff nodes to compare their diff file sizes and change their size accordingly.
    """
    from typing import Type
    from ..graph import Vertex
    from ...logger import logger
    from .filesystem import File, Handle
    from .network import Socket, Connection
    from ..config import ColorMap, SizeMap
    from ..colors import Color

    def project_range(x : float, sa : float, sb : float, da : float, db : float) -> float:
        if sa == sb:
            return (da + db) / 2
        p = (x - sa) / (sb - sa)
        return p * (db - da) + da

    def normalize_neighbor(cls : Type[Vertex]):
        if len(cls) > 0:
            logger.debug("Normalizing {} {} nodes.".format(len(cls), cls.__name__))
            a, b = min(sum(v.size for v in u.neighbors() if isinstance(v, Diff)) for u in cls), max(sum(v.size for v in u.neighbors() if isinstance(v, Diff)) for u in cls)
            minsize = SizeMap.get_config().get_size(cls) * 0.75
            maxsize = SizeMap.get_config().get_size(cls) * 1.25
            for u in cls:
                u.size = project_range(sum(v.size for v in u.neighbors() if isinstance(v, Diff)), a, b, minsize, maxsize)

    if e.major == "Finalizer" and e.minor == __N_diff_normalization_phase:
        logger.debug("Normalizing sizes of {} Diff nodes.".format(len(Diff)))
        if len(Diff) == 0:
            return
        a, b = min(len(d.glob) for d in Diff), max(len(d.glob) for d in Diff)
        minsize = 0.5
        maxsize = 3.0
        for d in Diff:
            d.size = project_range(len(d.glob), a, b, minsize, maxsize)
    
        for cls in (File, Handle, Socket, Connection):
            normalize_neighbor(cls)
        
        logger.debug("Normalizing colors of {} Diff nodes.".format(len(Diff)))
        a, b = min(d.glob_entropy for d in Diff), max(d.glob_entropy for d in Diff)
        for d in Diff:
            d.color = Color.linear((ColorMap.get_config().data.DiffLowEntropy, ColorMap.get_config().data.DiffHighEntropy), (1 - d.glob_entropy / 8, d.glob_entropy / 8))

@chrono
def fuse_diff_nodes(e : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause all identical Diff nodes to be merged with their size increasing.
    """
    from ...logger import logger
    from ..graph import Graph

    groups : dict[Diff, int] = {}

    def merge(u : Diff, v : Diff):
        """
        Merges vertex v into vertex u (v gets deleted at the end).
        """
        for e in v.edges:
            if e.source is v:
                e.source = u
            if e.destination is v:
                e.destination = u
        v.edges.clear()
        for g in Graph.active_graphs():
            g.remove(v)
        groups[u] += 1

    if e.major == "Finalizer" and e.minor == __N_diff_fusion_phase:
        logger.debug("Fusing {} Diff nodes.".format(len(Diff)))
        for u in Diff:
            merged = False
            for v in filter(lambda v : v in groups, Diff):
                if u.content == v.content:
                    merge(v, u)
                    merged = True
                    break
            if not merged:
                groups[u] = 1
        
        resize_work = [u for u, n in groups.items() if n > 1]
        if resize_work:
            logger.debug("Resizing {} fused Diff nodes. Actually lost {} Diff nodes.".format(len(resize_work), len(Diff) - len(groups)))
            for u in resize_work:
                u.size *= groups[u] ** 0.5

        
BuildingPhase.add_callback(finalize_diff_nodes)
BuildingPhase.add_callback(normalize_diff_nodes)
BuildingPhase.add_callback(fuse_diff_nodes)


del ABCMeta, Iterator, Optional, Color, Arrow, UniqueVertex, Vertex, chrono, logger, File, Connection, Handle, Socket, BuildingPhase, finalize_data_nodes, finalize_diff_nodes, normalize_diff_nodes, fuse_diff_nodes, CompilationParameters, Sequence, Hashable, TypeVar, S