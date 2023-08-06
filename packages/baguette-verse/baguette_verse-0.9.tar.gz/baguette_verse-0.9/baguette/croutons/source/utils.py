from types import UnionType




class MetaMatch:

    """
    This class encapsulates all the information about a given metagraph match in a specific graph.
    """

    __slots__ = {
        "file" : "The Python graph file that the match was made in.",
        "meta" : "The name of the metagraph that matched.",
        "graph" : "The subgraph that matched the metagraph." 
    }

    def __init__(self, file, meta, graph):
        self.file = file
        self.meta = meta
        self.graph = graph





def class_union(*cls : type) -> type | UnionType:
    """
    Creates the union of classes, as sum operator but for the "|" operator.
    """
    for c in cls:
        if not isinstance(c, type):
            raise TypeError("Expected types, got " + repr(type(c).__name__))
    l = list(cls)
    if not l:
        raise ValueError("Expected at least one type.")
    c = l.pop()
    while l:
        c = c | l.pop()
    return c