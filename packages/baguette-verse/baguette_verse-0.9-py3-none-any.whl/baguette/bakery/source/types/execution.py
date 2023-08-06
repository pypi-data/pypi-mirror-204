"""
This module defines the Vertices and Edges that are related to execution.
"""

from pathlib import PurePath
from ...logger import logger
from typing import Any, Callable, Dict, Iterator, List, Optional, Set
from ..colors import Color
from Viper.meta.iterable import InstancePreservingClass
from ..graph import UniqueVertex, Arrow, Edge, Vertex
from ..utils import chrono
from ..build import BuildingPhase

__all__ = ["Process", "Thread", "Call", "CallHandler", "HasChildProcess", "UsesAsArgument", "HasThread", "HasFirstCall", "FollowedBy", "NextSignificantCall", "StartedProcess", "InjectedThread", "StartedThread"]





logger.debug("Loading execution library.")

CommandTree = list[tuple[str, "CommandTree"]]

class Process(UniqueVertex):

    """
    A process vertex. Holds information to identify a process.
    """

    __slots__ = {
        "PID" : "The PID of the process during its execution",
        "__command" : "The command that this process is running",
        "executable" : "The file system path that the process was started in",
        "start" : "The time at which the process was started",
        "stop" : "The time at chich the process was stopped",
        "__sub_commands" : "The tree of commands executed by all chile processes"
    }

    __pickle_slots__ = {
        "PID",
        "command",
        "executable",
        "start",
        "stop",
        "sub_commands"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.PID : int = 0
        self.__command : tuple[str] = tuple()
        self.executable : str = ""
        self.start : float = 0.0
        self.stop : float = 0.0
        self.__sub_commands : CommandTree | None = None

        from .filesystem import NewFile
        from argparse import ArgumentParser
        from pathlib import PurePath
        from ..utils import is_path, path_factory

        def to_absolute(p : PurePath, cwd : PurePath) -> PurePath:
            if p.is_absolute():
                return p
            return cwd / p
        
        p = ArgumentParser()
        
        def link(e : NewFile):
            from .filesystem import File
            f = e.file
            if not f.name:
                return
            # print("New file :", repr(f.path))
            # # print("Process :", repr(self.command))
            # print("Process #{} : '{}'".format(self.PID, self.executable))
            # print("Splitting command : {}".format(self.__command))
            for i, arg in enumerate(self.__command):
                if not i:
                    arg = self.executable
                while arg.endswith(" "):
                    arg = arg[:-1]
                while arg.startswith(" "):
                    arg = arg[1:]
                if arg.startswith("\"") and arg.endswith("\""):
                    arg = arg[1:-1]
                if arg.startswith("'") and arg.endswith("'"):
                    arg = arg[1:-1]
                # print(">>>", f.name.lower(), arg.lower())
                if (is_path(arg) and f.name.lower() == to_absolute(path_factory(arg), path_factory(self.executable)).name.lower()) or f.name.lower() in arg.lower():
                # if (f.name in arg and len(f.name) / len(arg) > 0.9) or (str(f.path) in arg and len(str(f.path)) / len(arg) > 0.9):        # You need to work with a process cwd
                    if i > 0:
                        UsesAsArgument(self, f)
                        break
                    else:
                        Runs(self, f)

        NewFile.add_callback(link)

    @property
    def label(self) -> str:
        """
        Returns a label for the Process node.
        """
        return "Process #" + str(self.PID)
        
    @property
    def threads(self) -> list["Thread"]:
        """
        List of all the threads that this process had.
        """
        return [e.destination for e in self.edges if isinstance(e, HasThread)] 
    
    @property
    def children_processes(self) -> list["Process"]:
        """
        List of all the children processes that this process created.
        """
        return [e.destination for e in self.edges if isinstance(e, HasChildProcess) and e.source is self]
    
    @property
    def parent_process(self) -> Optional["Process"]:
        """
        Returns the parent process node if one exists in the graph.
        """
        for e in self.edges:
            if isinstance(e, HasChildProcess) and e.destination is self:
                return e.source
            
    @property
    def command(self) -> str:
        """
        The command ran by this Process.
        """
        return " ".join(self.__command)
    
    @command.setter
    def command(self, cmd : str):
        from ..utils import parse_command_line
        if not isinstance(cmd, str):
            raise TypeError("Expected str, got " + repr(type(cmd).__name__))
        self.__command = tuple(parse_command_line(cmd))
        if not self.__command and self.executable:
            self.__command = (self.executable, )
        
    def parsed_command(self) -> list[str]:
        """
        Returns the argument vector used for starting this process.
        """
        return list(self.__command)

    @property
    def sub_commands(self) -> CommandTree:
        """
        Returns a dict structure that represents the commands executed by all child processes.
        """
        if self.__sub_commands != None:
            return self.__sub_commands
        sc = []
        for e in self.edges:
            if isinstance(e, HasChildProcess) and e.source is self:
                sc.append((e.destination.command, e.destination.sub_commands))
        self.__sub_commands = sc
        return sc
    
    @sub_commands.setter
    def sub_commands(self, value : CommandTree):
        self.__sub_commands = value





class Thread(UniqueVertex):

    """
    A thread vertex. Holds information to identify a thread.
    """

    __slots__ = {
        "TID" : "The TID of the thread during its execution",
        "Ncalls" : "The number of system calls that the thread made",
        "first" : "The first system call that this thread made",
        "last" : "the last system call that this thread made",
        "start" : "The time at which the thread was started",
        "stop" : "The time at chich the thread was stopped"
    }

    __pickle_slots__ = {
        "TID",
        "Ncalls",
        "first",
        "last",
        "start",
        "stop"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.TID : int = 0
        self.Ncalls : int = 0
        self.first : Optional["Call"] = None
        self.last : Optional["Call"] = None
        self.start : float = 0.0
        self.stop : float = 0.0

    @property
    def label(self) -> str:
        """
        Returns a label for the Thread node.
        """
        return "Thread #" + str(self.TID)
    
    @property
    def process(self) -> Process:
        """
        The Process Vertex that runs this Thread.
        """
        for e in self.edges:
            if isinstance(e, HasThread):
                return e.source
        raise RuntimeError("Got a Thread without a parent Process.")





class Call(UniqueVertex):

    """
    A system call vertex. Holds information about a specific system call.
    Don't forget to call c.integrate() after setup of Call c is finished to integrate the call in the graph.
    """

    __slots__ = {
        "name" : "The name of the system call",
        "category" : "The family of the system call",
        "stacktrace" : "The stacktrace of the call",
        "status" : "Indicates if the call ran succesfully",
        "arguments" : "The arguments that the call received",
        "return_value" : "The value that the call returned",
        "time" : "The timestamp at which the call was detected",
        "flags" : "The flags of the call",
        "__thread" : "A shortcut to the Thread vertex that made this call"
    }

    __pickle_slots__ = {
        "name",
        "category",
        "stacktrace",
        "status",
        "arguments",
        "return_value",
        "time",
        "flags",
        "thread"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        from ..record import record
        super().__init__(c=c, parent=parent)
        self.name : str = ""
        self.category : str = ""
        self.stacktrace : tuple = ()
        self.status : int = 0
        self.arguments : record = record()
        self.return_value : Any = None
        self.time : float = 0.0
        self.flags : record = record()
        self.__thread : Thread | None = None
    
    @property
    def thread(self) -> Thread:
        """
        The Thread that made this Call.
        """
        if self.__thread is None:
            raise RuntimeError("Got a Call without a calling Thread.")
        return self.__thread
    
    @thread.setter
    def thread(self, value : Thread):
        if not isinstance(value, Thread):
            raise TypeError("Expected Thread, got " + repr(type(value).__name__))
        self.__thread = value

    __seen : Set["CallHandler"] = set()             # The individual system call handlers already seen
    __cache : Dict[str, List["CallHandler"]] = {}   # Used to speed up access to the correct handlers for next calls to an already seen system call (with the same name)

    @chrono
    def integrate(self):
        """
        Integrates the call to the graph.
        Finds the correct handler(s) for this call and executes them.
        """
        if self.name not in Call.__cache:   # Add the system call name in cache if not present
            Call.__cache[self.name] = []
        if self.name in Call.__cache:       # Some handlers have already been matched
            for CH in Call.__cache[self.name]:
                if self in CH:
                    CH(self)
        if len(Call.__seen) < len(CallHandler):  # There might be unmatched handlers
            for CH in filter(lambda CH : CH not in Call.__seen, CallHandler):
                if self in CH:
                    Call.__cache[self.name].append(CH)
                    Call.__seen.add(CH)
                    CH(self)
    
    @property
    def label(self) -> str:
        """
        The label for this node.
        """
        return self.name





class CallHandler(metaclass = InstancePreservingClass):

    """
    The class for all handlers of system calls.
    Upon creation, a system call vertex will look into the instances of this class to find a valid handler and execute its integration function.
    """

    def __init__(self, matcher : Callable[[Call], bool], integrator : Callable[[Call], None]) -> None:
        self.__matcher = matcher
        self.__integrator = integrator
    

    def __repr__(self) -> str:
        """
        Implements repr(self).
        """
        return "CallHandler(" + repr(self.__matcher) + ", " + repr(self.__integrator) + ")"
    

    def match(self, c : Call) -> bool:
        """
        Returns True if given Call c should be handled by this CallHandler
        """
        if self.__matcher(c):
            return True
        return False
    

    def integrate(self, c : Call):
        """
        Integrates Call c into the graph
        """
        self.__integrator(c)
    

    def __contains__(self, c : Any) -> bool:
        """
        Implements c in self.
        Equivalent to self.match(c).
        """
        if not isinstance(c, Call):
            return False
        return self.match(c)
    
    
    def __call__(self, c : Call):
        """
        Implements self(c).
        Equivalent to self.integrate(c)
        """
        self.integrate(c)





class HasChildProcess(Arrow):

    """
    This kind of arrow indicates that a process created another one.
    """

    source : Process
    destination : Process





class UsesAsArgument(Edge):

    """
    This kind of edge indicates that a process used a file or directory in its command line.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .filesystem import File, Directory
    del TYPE_CHECKING

    source : Process
    destination : "File | Directory"




class Runs(Edge):
    
    """
    This kind of edge indicates process ran a file as its program.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .filesystem import File
    del TYPE_CHECKING

    source : Process
    destination : "File"





class HasThread(Edge):

    """
    This kind of edge indicates that a process hosts a thread.
    """

    label : str = ""

    source : Process
    destination : Thread





class HasFirstCall(Edge):

    """
    This kind of edge indicates what was the first system call of a thread.
    """

    label : str = ""

    source : Thread
    destination : Call





class FollowedBy(Arrow):

    """
    This kind of arrow indicates that a system call was followed by another one.
    """

    label : str = ""

    source : Call
    destination : Call





class NextSignificantCall(Arrow):
    
    """
    This kind of arrows links two Call nodes that happened one after the other in the same thread both nodes are linked to other types of nodes.
    """

    label : str = ""

    source : Call
    destination : Call





class StartedThread(Edge):

    """
    This kind of edge indicates that a system call started a new thread.
    """

    __slots__ = {
        "remote" : "Indicates if the started thread was started in another process (remote thread)"
    }

    __pickle_slots__ = {
        "remote"
    }

    label : str = ""

    source : Call
    destination : Thread

    def __init__(self, source: Vertex, destination: Vertex, *, c: Color | None = None, auto_write: bool = True) -> None:
        super().__init__(source, destination, c=c, auto_write=auto_write)
        self.remote : bool = False
    




class InjectedThread(Arrow):

    """
    This kind of arrow indicates a process created a remote thread.
    """

    source : Process
    destination : Thread





class StartedProcess(Edge):

    """
    This kind of edge indicates that a system call started a new process.
    """

    label : str = ""

    source : Call
    destination : Process





@chrono
def integrate_thread_creation(c : Call):
    """
    Links a Thread vertex to the Call vertex (from another thread) that created it.
    """
    from ...logger import logger
    from ..graph import find_or_create
    if c.arguments.thread_identifier != 0:      # Should indicate that the call failed
        logger.debug("New thread detected.")
        t : Thread
        t, ok = find_or_create(Thread, TID = c.arguments.thread_identifier)
        l = StartedThread(c, t)
        if c.name in {"CreateRemoteThread", "CreateRemoteThreadEx"}:
            logger.info("Detected thread injection.")
            l.remote = True
            p = c.thread.process
            InjectedThread(p, t)

@chrono
def integrate_process_creation(c : Call):
    """
    Links a Process vertex to the Call vertex (from another process) that created it.
    """
    from ...logger import logger
    from ..graph import find_or_create
    if c.arguments.process_identifier != 0:
        logger.debug("New process detected.")
        p : Process
        p, ok = find_or_create(Process, PID = c.arguments.process_identifier)
        l = StartedProcess(c, p)
        




# Thread creation handlers
CallHandler(lambda c : c.name == "CreateThread", integrate_thread_creation)          # Basic thread creation
CallHandler(lambda c : c.name in {"CreateRemoteThread", "CreateRemoteThreadEx"}, integrate_thread_creation)    # Remote thread creation (into another process)

# Process creation handlers
CallHandler(lambda c : "CreateProcess" in c.name, integrate_process_creation)


__N_phase = BuildingPhase.request_finalizing_phase()

@chrono
def remove_cuckoo_phantom_processes(ev : BuildingPhase):
    """
    When called with the right finalizing phase event, will cause Process nodes which represent Cuckoo process (inital processes with no info available) to be erased.
    """
    from ...logger import logger
    from ..graph import Graph
    from .network import SpawnedProcess, Host
    if ev.major == "Finalizer" and ev.minor == __N_phase:
        logger.debug("Erasing Cuckoo phantom processes.")
        n = 0
        h = Host.current
        for e in h.edges.copy():
            p = e.destination
            if isinstance(p, Process) and not p.parent_process and not p.executable:
                for pi in p.children_processes:
                    SpawnedProcess(h, pi)
                for ei in p.edges.copy():
                    if isinstance(e, SpawnedProcess):
                        h = e.source
                    ei.delete()
                    for g in Graph.active_graphs():
                        g.remove(ei)
                for g in Graph.active_graphs():
                    g.remove(p)
                n += 1
        if n:
            logger.debug("Actually removed {} Cuckoo process{}.".format(n, "es" if n > 1 else ""))



BuildingPhase.add_callback(remove_cuckoo_phantom_processes)

del logger, Any, Callable, Dict, Iterator, List, Optional, Set, Color, InstancePreservingClass, UniqueVertex, Arrow, Vertex, PurePath, chrono, integrate_process_creation, integrate_thread_creation, remove_cuckoo_phantom_processes