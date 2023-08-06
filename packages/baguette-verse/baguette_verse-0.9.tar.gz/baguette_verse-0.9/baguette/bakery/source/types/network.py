"""
This module defines the Vertices and Edges that are related to network activity.
"""

from collections import defaultdict
from ...logger import logger
from typing import Any, Optional
from ..colors import Color
from ..graph import Arrow, Edge, UniqueVertex, Vertex
from .execution import Call, CallHandler, Process
from ..utils import chrono
from Viper.meta.decorators import staticproperty

__all__ = ["Socket", "Connection", "Host", "SpawnedProcess", "HasConnection", "HasSocket", "Communicates", "CreatesSocket", "Binds", "Connects", "Sends", "Receives", "Conveys", "Closes", "CloseSocket", "ListensOn", "Shutdown", "Accepts", "Duplicates"]





logger.debug("Loading network library.")

class Connection(UniqueVertex):

    """
    A connection vertex. This is a link vertex between two socket. It might only exist for a part of the lifetime of both its connected sockets.
    """

    __slots__ = {
        "duration" : "The duration that the connection was maintained for",
        "volume" : "The amount of data transfered through the connection",
        "src" : "The source address",
        "dest" : "The destination address"
    }

    __pickle_slots__ = {
        "duration",
        "volume",
        "src",
        "dest"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.duration : float = 0.
        self.volume : int = 0
        self.src : Any = None
        self.dest : Any = None

    @property
    def socket(self) -> "Socket":
        """
        The local Socket that this connection was made through.
        """
        for e in self.edges:
            if isinstance(e, HasConnection):
                return e.source
        raise RuntimeError("Got a Connection bound to no Socket.")





class Socket(UniqueVertex):

    """
    A socket vertex. Represents a handle given by the system to allow some kind of communication.
    """

    __slots__ = {
        "family" : "The socket address family. For example, 'InterNetwork' is for IP V4 addresses. Refer to Socket.families for documentation",
        "protocol" : "The transport protocol used by the socket. For example, Tcp. Refer to Socket.protocols for documentation",
        "type" : "The type of socket. For exemple, Dgram is a socket that supports datagrams. Refer to Socket.types for documentation"
    }

    __pickle_slots__ = {
        "family",
        "protocol",
        "type"
    }

    families = defaultdict(lambda : ("Uncharted", "The value does not correspond to any known address family"), {
        16 : ('AppleTalk', 'AppleTalk address.'),
        22 : ('Atm', 'Native ATM services address.'),
        21 : ('Banyan', 'Banyan address.'),
        10 : ('Ccitt', 'Addresses for CCITT protocols, such as X.25.'),
        5 : ('Chaos', 'Address for MIT CHAOS protocols.'),
        24 : ('Cluster', 'Address for Microsoft cluster products.'),
        65537 : ('ControllerAreaNetwork', 'Controller Area Network address.'),
        9 : ('DataKit', 'Address for Datakit protocols.'),
        13 : ('DataLink', 'Direct data-link interface address.'),
        12 : ('DecNet', 'DECnet address.'),
        8 : ('Ecma', 'European Computer Manufacturers Association (ECMA) address.'),
        19 : ('FireFox', 'FireFox address.'),
        15 : ('HyperChannel', 'NSC Hyperchannel address.'),
        1284425 : ('Ieee', 'IEEE 1284.4 workgroup address.'),
        3 : ('ImpLink', 'ARPANET IMP address.'),
        2 : ('InterNetwork', 'Address for IP version 4.'),
        623 : ('InterNetworkV', 'Address for IP version 6.'),
        6 : ('Ipx', 'IPX or SPX address.'),
        26 : ('Irda', 'IrDA address.'),
        7 : ('Iso', 'Address for ISO protocols.'),
        14 : ('Lat', 'LAT address.'),
        29 : ('Max', 'MAX address.'),
        17 : ('NetBios', 'NetBios address.'),
        28 : ('NetworkDesigners', 'Address for Network Designers OSI gateway-enabled protocols.'),
        6 : ('NS', 'Address for Xerox NS protocols.'),
        7 : ('Osi', 'Address for OSI protocols.'),
        65536 : ('Packet', 'Low-level Packet address.'),
        4 : ('Pup', 'Address for PUP protocols.'),
        11 : ('Sna', 'IBM SNA address.'),
        1 : ('Unix', 'Unix local to host address.'),
        -1 : ('Unknown', 'Unknown address family.'),
        0 : ('Unspecified', 'Unspecified address family.'),
        18 : ('VoiceView', 'VoiceView address.'),
    })

    protocols = defaultdict(lambda : ("Uncharted", "The value does not correspond to any known protocol"), {
        3 : ('Ggp', 'Gateway To Gateway Protocol.'),
        1 : ('Icmp', 'Internet Control Message Protocol.'),
        58 : ('IcmpV6', 'Internet Control Message Protocol for IPv6.'),
        22 : ('Idp', 'Internet Datagram Protocol.'),
        2 : ('Igmp', 'Internet Group Management Protocol.'),
        0 : ('IP', 'Internet Protocol.'),
        51 : ('IPSecAuthenticationHeader', 'IPv6 Authentication header. For details'),
        50 : ('IPSecEncapsulatingSecurityPayload', 'IPv6 Encapsulating Security Payload header.'),
        4 : ('IPv4', 'Internet Protocol version 4.'),
        41 : ('IPv6', 'Internet Protocol version 6 (IPv6).'),
        60 : ('IPv6DestinationOptions', 'IPv6 Destination Options header.'),
        44 : ('IPv6FragmentHeader', 'IPv6 Fragment header.'),
        0 : ('IPv6HopByHopOptions', 'IPv6 Hop by Hop Options header.'),
        59 : ('IPv6NoNextHeader', 'IPv6 No next header.'),
        43 : ('IPv6RoutingHeader', 'IPv6 Routing header.'),
        1000 : ('Ipx', 'Internet Packet Exchange Protocol.'),
        77 : ('ND', 'Net Disk Protocol (unofficial).'),
        12 : ('Pup', 'PARC Universal Packet Protocol.'),
        255 : ('Raw', 'Raw IP packet protocol.'),
        1256 : ('Spx', 'Sequenced Packet Exchange protocol.'),
        1257 : ('SpxII', 'Sequenced Packet Exchange version 2 protocol.'),
        6 : ('Tcp', 'Transmission Control Protocol.'),
        17 : ('Udp', 'User Datagram Protocol.'),
        -1 : ('Unknown', 'Unknown protocol.'),
        0 : ('Unspecified', 'Unspecified protocol.'),
    })

    types = defaultdict(lambda : ("Uncharted", "The value does not correspond to any known socket type"), {
        2 : ('Dgram', 'Supports datagrams, which are connectionless, unreliable messages of a fixed (typically small) maximum length. Messages might be lost or duplicated and might arrive out of order. A Socket of type Dgram requires no connection prior to sending and receiving data, and can communicate with multiple peers. Dgram uses the Datagram Protocol (ProtocolType.Udp) and the AddressFamily. InterNetwork address family.'),
        3 : ('Raw', 'Supports access to the underlying transport protocol. Using Raw, you can communicate using protocols like Internet Control Message Protocol (ProtocolType.Icmp) and Internet Group Management Protocol (ProtocolType.Igmp). Your application must provide a complete IP header when sending. Received datagrams return with the IP header and options intact.'),
        4 : ('Rdm', 'Supports connectionless, message-oriented, reliably delivered messages, and preserves message boundaries in data. Rdm (Reliably Delivered Messages) messages arrive unduplicated and in order. Furthermore, the sender is notified if messages are lost. If you initialize a Socket using Rdm, you do not require a remote host connection before sending and receiving data. With Rdm, you can communicate with multiple peers.'),
        5 : ('Seqpacket', 'Provides connection-oriented and reliable two-way transfer of ordered byte streams across a network. Seqpacket does not duplicate data, and it preserves boundaries within the data stream. A Socket of type Seqpacket communicates with a single peer and requires a remote host connection before communication can begin.'),
        1 : ('Stream', 'Supports reliable, two-way, connection-based byte streams without the duplication of data and without preservation of boundaries. A Socket of this type communicates with a single peer and requires a remote host connection before communication can begin. Stream uses the Transmission Control Protocol (ProtocolType.Tcp) and the AddressFamily.InterNetwork address family.'),
        -1 : ('Unknown', 'Specifies an unknown Socket type.'),
    })

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.family : str = ""
        self.protocol : str = ""
        self.type : str = ""





class Host(UniqueVertex):

    """
    A machine vertex. It represents a physical machine.
    """

    __current : Optional["Host"] = None

    @staticproperty
    def current() -> "Host":
        """
        The currently active Host node. This is used to indicate which Host node is the machine running the sample.
        """
        if Host.__current is None:
            raise AttributeError("Host class has no attribute 'current'.")
        return Host.__current

    @current.setter
    def current(value : "Host"):
        if not isinstance(value, Host):
            raise TypeError("Cannot set attribute 'current' of class 'Host' to object of type '{}'".format(type(value).__name__))
        Host.__current = value

    __slots__ = {
        "address" : "The IP address of the machine",
        "domain" : "The URL the machine is known as if any",
        "name" : "The machine's name",
        "platform" : "The operating system the host is running on"
    }

    __pickle_slots__ = {
        "address",
        "domain",
        "name",
        "platform"
    }

    def __init__(self, *, c: Color | None = None, parent: Optional[Vertex] = None) -> None:
        super().__init__(c=c, parent=parent)
        self.address : str = ""
        self.domain : str = ""
        self.name : str = ""
        self.platform : str = "Unknown"
    
    @property
    def label(self) -> str:
        """
        Returns a label for this Host node.
        """
        if self.name:
            return "Host " + repr(self.name)
        return "Host at " + self.address





class SpawnedProcess(Edge):
    
    """
    This kind of edge indicates that a machine hosts a process.
    """

    source : Host
    destination : Process





class HasSocket(Edge):

    """
    This kind of edge indicates that a process opened a socket.
    """

    label : str = ""

    source : Process
    destination : Socket





class HasConnection(Edge):

    """
    This kind of edge indicates that a socket makes a connection.
    """

    label : str = ""

    source : Socket
    destination : Connection





class Communicates(Edge):

    """
    This kind of edge indicates that two hosts communicate via a connection
    """

    source : Connection
    destination : Host





class CreatesSocket(Edge):

    """
    This kind of edge indicates that a system call created a socket.
    """

    label : str = ""

    source : Call
    destination : Socket





class Binds(Edge):

    """
    This kind of edge indicates that a system call bound a connection to a local address.
    """

    __slots__ = {
        "src" : "The source (local) address of the connection",
    }

    __pickle_slots__ = {
        "src"
    }

    label : str = ""

    source : Call
    destination : Connection

    def __init__(self, source: Vertex, destination: Vertex, *, c: Color | None = None, auto_write: bool = True) -> None:
        super().__init__(source, destination, c=c, auto_write=auto_write)
        self.src : Any = None





class Connects(Edge):

    """
    This kind of edge indicates that a system call connected a connection to a remote address.
    """

    __slots__ = {
        "dest" : "The destination (remote) address of the connection"
    }

    __pickle_slots__ = {
        "dest"
    }

    label : str = ""

    source : Call
    destination : Connection

    def __init__(self, source: Vertex, destination: Vertex, *, c: Color | None = None, auto_write: bool = True) -> None:
        super().__init__(source, destination, c=c, auto_write=auto_write)
        self.dest : Any = None





class Sends(Arrow):

    """
    This kind of arrow indicates that a system call sent data through a connection.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : Call
    destination : "Data"





class Receives(Arrow):

    """
    This kind of arrow indicates that a system call received data through a connection.
    """

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : "Data"
    destination : Call





class Conveys(Arrow):
    
    """
    This kind of arrow indicates that a connection conveyed a message.
    """

    label : str = ""

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .data import Data
    del TYPE_CHECKING

    source : "Connection | Data"
    destination : "Connection | Data"





class Closes(Edge):

    """
    This kind of edge indicates that a system call closed a connection.
    """
    
    label : str = ""

    source : Call
    destination : Connection





class CloseSocket(Edge):

    """
    This kind of edge indicates that a system call closed a socket object.
    """

    label : str = ""

    source : Call
    destination : Socket





class ListensOn(Edge):

    """
    This kind of edge indicates that a system call set a socket to listening mode.
    """

    source : Call
    destination : Socket





class Shutdown(Edge):

    """
    This kind of edge indicates that a connection was shutdown by a system call.
    """

    label : str = ""

    source : Call
    destination : Connection





class Accepts(Edge):

    """
    This kind of arrow indicates that a system call accepted a connection from a remote address.
    """

    __slots__ = {
        "dest" : "The destination (remote) address of the connection"
    }

    __pickle_slots__ = {
        "dest"
    }

    source : Call
    destination : Connection

    def __init__(self, source: Vertex, destination: Vertex, *, c: Color | None = None, auto_write: bool = True) -> None:
        super().__init__(source, destination, c=c, auto_write=auto_write)
        self.dest : Any = None





class Duplicates(Arrow):

    """
    This kind of arrow indicates that a socket was duplicated to form a similar socket (example: after a call to accept()).
    """

    source : Socket
    destination : Socket





_active_connections : dict[Socket, Connection] = {}
_active_handles : dict[Socket, int] = {}
_inverted_handles : dict[int, Socket] = {}

@chrono
def integrate_socket_creation(c : Call):
    """
    Creates a Socket vertex and links it to the call that created it.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Socket created.")
        s = Socket()
        _active_handles[s] = c.arguments.socket
        _inverted_handles[c.arguments.socket] = s
        s.family = Socket.families[c.arguments.af][0]
        s.protocol = Socket.protocols[c.arguments.protocol][0]
        s.type = Socket.types[c.arguments.type][0]
        if s in _active_connections:
            _active_connections.pop(s)
        CreatesSocket(c, s)
        HasSocket(c.thread.process, s)

@chrono
def integrate_socket_binding(c : Call):
    """
    Creates a Connection vertex and binds it to a local address.
    """
    from ...logger import logger
    from ..graph import find_or_create
    if c.status == 1:
        logger.debug("Socket bound.")
        l = Connection()
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Binding to non-existing socket.")
            return
        _active_connections[s] = l
        HasConnection(s, l)
        Communicates(l, find_or_create(Host, domain = "host")[0])
        b = Binds(c, l)
        if s.family == "InterNetwork":
            b.src = (c.arguments.ip_address, c.arguments.port)
            l.src = b.src
        else:
            logger.error("I don't know how to handle this type of address:\n{}".format(s))

@chrono
def integrate_socket_connection(c : Call):
    """
    Sets the remote address of a connection.
    """
    from ...logger import logger
    from ..graph import find_or_create
    if c.status == 1:
        logger.debug("Socket connected.")
        try:
            sock = c.arguments.socket
        except AttributeError:
            sock = c.arguments.s
        if sock in _inverted_handles:
            s = _inverted_handles[sock]
        else:
            logger.warning("Connecting from non-existing socket.")
            return
        if s in _active_connections:
            l = _active_connections[s]
            logger.warning("Trying to connect an unbound socket...")
        else:
            l = Connection()
        HasConnection(s, l)
        Communicates(l, find_or_create(Host, domain = "host")[0])
        _active_connections[s] = l
        b = Connects(c, l)
        Communicates(l, find_or_create(Host, address = c.arguments.ip_address)[0])
        if s.family == "InterNetwork":
            b.dest = (c.arguments.ip_address, c.arguments.port)
            l.dest = b.dest
        else:
            logger.error("I don't know how to handle this type of address:\n{}".format(s))


@chrono
def integrate_socket_listening(c : Call):
    """
    Sets the socket in listening mode.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Socket listening.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Listening from non-existing socket.")
            return
        ListensOn(c, s)

@chrono
def integrate_socket_accepting(c : Call):
    """
    Sets a connection remote address through an accept system call. Also creates a new socket object.
    """
    from ...logger import logger
    from ..graph import find_or_create
    if c.status == 1:
        logger.debug("Socket accepting connection.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Accepting from non-existing socket.")
            return
        s1 = Socket()
        l1 = Connection()
        s1.family = s.family
        s1.protocol = s.protocol
        s1.type = s.type
        _active_handles[s1] = c.return_value
        _inverted_handles[c.return_value] = s1
        if s not in _active_connections:
            logger.warning("Accepting from unbound socket...")
        else:
            l = _active_connections[s]
            l1.src = l.src
        b = Accepts(c, l1)
        HasConnection(s1, l1)
        Duplicates(s, s1)
        Communicates(l1, find_or_create(Host, address = c.arguments.ip_address)[0])
        if s1.family == "InterNetwork":
            b.dest = (c.arguments.ip_address, c.arguments.port)
            l1.dest = b.dest

@chrono
def integrate_socket_close(c : Call):
    """
    Closes a socket and the connection linked to it.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Closing socket.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Closing non-existing socket.")
            return
        CloseSocket(c, s)
        handle = _active_handles.pop(s)
        _inverted_handles.pop(handle)
        if s in _active_connections:
            l = _active_connections.pop(s)
            Closes(c, l)
        else:
            logger.warning("Closing down unbound socket...")

@chrono
def integrate_socket_shutdown(c : Call):
    """
    Closes a connection.
    """
    from ...logger import logger
    if c.status == 1:
        logger.debug("Closing socket.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Shuting down non-existing socket")
            return
        if s in _active_connections:
            l = _active_connections.pop(s)
            Shutdown(c, l)
        else:
            logger.warning("Shuting down unbound socket...")

@chrono
def integrate_socket_send(c : Call):
    """
    Sends data through a connection.
    """
    from ...logger import logger
    from .data import Data, register_write_operation
    if c.status == 1:
        logger.debug("Sending data.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Sending through non-existing socket.")
            return
        if s not in _active_connections:
            logger.warning("Sending through unbound socket.")
        else:
            l = _active_connections[s]
            d = Data()
            d.time = c.time
            d.set_data(c.arguments.buffer)
            Sends(c, d)
            Conveys(d, l)
            l.volume += len(d.data)
            register_write_operation(l, s, c.arguments.buffer)

@chrono
def integrate_socket_recv(c : Call):
    """
    Receives data through a connection.
    """
    from ...logger import logger
    from .data import Data, register_read_operation
    if c.status == 1:
        logger.debug("Receiving data.")
        if c.arguments.socket in _inverted_handles:
            s = _inverted_handles[c.arguments.socket]
        else:
            logger.warning("Receiving through non-existing socket.")
            return
        if s not in _active_connections:
            logger.warning("Receiving through unbound socket.")
        else:
            l = _active_connections[s]
            d = Data()
            d.time = c.time
            d.set_data(c.arguments.buffer)
            Receives(d, c)
            Conveys(l, d)
            l.volume += len(d.data)
            register_read_operation(l, s, c.arguments.buffer)





# Socket creation
CallHandler(lambda c : c.name in ("socket", "WSASocketW"), integrate_socket_creation)

# Socket binding
CallHandler(lambda c : c.name == "bind", integrate_socket_binding)

# Socket connecting
CallHandler(lambda c : c.name in ("connect", "WSAConnect"), integrate_socket_connection)

# Socket listening
CallHandler(lambda c : c.name == "listen", integrate_socket_listening)

# Socket accepting
CallHandler(lambda c : c.name == "accept", integrate_socket_accepting)

# Socket closing
CallHandler(lambda c : c.name == "closesocket", integrate_socket_close)

# Socket shuting down
CallHandler(lambda c : c.name == "shutdown", integrate_socket_shutdown)

# Socket sending
CallHandler(lambda c : c.name == "send", integrate_socket_send)

# Socket receiving
CallHandler(lambda c : c.name == "recv", integrate_socket_recv)


del defaultdict, logger, Any, Optional, Color, Arrow, UniqueVertex, Vertex, Call, CallHandler, chrono, integrate_socket_accepting, integrate_socket_binding, integrate_socket_close, integrate_socket_connection, integrate_socket_creation, integrate_socket_listening, integrate_socket_recv, integrate_socket_send, integrate_socket_shutdown