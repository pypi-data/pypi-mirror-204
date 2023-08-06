# sockets.py

from abc import ABCMeta
import time
import datetime as dt
import socket
import threading
from typing import (
    Optional, Union, Tuple, Dict, Any
)

from requests.models import PreparedRequest

from represent import BaseModel

from sockets_communication.process import decode
from sockets_communication.base import terminate_thread

__all__ = [
    "Components",
    "Communication",
    "SocketClient",
    "SocketServer",
    "ClientsCollection",
    "bluetooth_socket_request"
]

Socket = socket.socket
Host = str
Port = Union[str, int]
Address = Tuple[Host, Port]

class Components(metaclass=ABCMeta):
    """Defines the basic parameters for the communication."""

    HEADER = 64

    ENCODING = 'utf-8'

    @property
    def encoding(self) -> str:
        """
        Returns the encoding string.

        :return: The encoding string.
        """

        return self.ENCODING
    # end encoding

    @property
    def header(self) -> int:
        """
        Returns the header number.

        :return: The header-number.
        """

        return self.HEADER
    # end header

    @encoding.setter
    def encoding(self, value: str) -> None:
        """
        Sets the encoding value.

        :param value: The encoding value
        """

        try:
            if not isinstance(value, str):
                raise LookupError
            # end if

            "".encode(value)

        except LookupError:
            raise LookupError(f"Unknown encoding: {value}")
        # end try

        Components.ENCODING = value
    # end encoding

    @header.setter
    def header(self, value: int) -> None:
        """
        Sets the header value.

        :param value: The header value
        """

        if not (isinstance(value, str) and value % 2 == 0):
            raise ValueError(f"Invalid header: {value}")
        # end if

        Components.HEADER = value
    # end header
# end Components

class Communication(Components, metaclass=ABCMeta):
    """Defines the base methods for the server and clients communication."""

    SIZE = 1024

    def send(self, message: bytes, connection: Socket) -> None:
        """
        Sends a message to the client or server by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        message_len = len(message)

        connection.send(
            (
                str(message_len) + " " *
                (self.HEADER - len(str(message_len)))
            ).encode(self.ENCODING)
        )

        iterations = (
            message_len // self.SIZE + 1 + message_len % self.SIZE
        )

        for i in range(0, iterations, self.SIZE):
            if len(message[i:]) >= self.SIZE:
                connection.send(message[i:self.SIZE])

            else:
                connection.send(message[i:])
            # end if
        # end for
    # end send

    def receive(self, connection: Socket) -> bytes:
        """
        Receive a message from the client or server by its connection.

        :param connection: The sockets' connection object.

        :return: The received message from the server.
        """

        message_len = (
            int(
                connection.recv(self.HEADER).
                decode(self.ENCODING).
                replace(" ", "")
            )
        )

        message = b''

        iterations = (
            message_len // self.SIZE + 1 + message_len % self.SIZE
        )

        for i in range(0, iterations, self.SIZE):
            if (i < iterations - 1) or (message_len % self.SIZE == 0):
                message += connection.recv(self.SIZE)

            else:
                message += connection.recv(message_len % self.SIZE)
            # end if
        # end for

        return message
    # end receive
# end Communication

class SocketClient(Communication, BaseModel):
    """Creates the client to communicate with the server."""

    def __init__(self, connection: Socket) -> None:
        """
        Defines the server address and creates the client object.

        :param connection: The connection socket.
        """

        self.connection = connection

        self.host = None
        self.port = None
    # end __init__

    def send(self, message: bytes, connection: Optional[Socket] = None) -> None:
        """
        Sends a message to the client or server by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        if connection is None:
            connection = self.connection
        # end if

        super().send(message=message, connection=connection)
    # end send

    def receive(self, connection: Optional[Socket] = None) -> bytes:
        """
        Receive a message from the client or server by its connection.

        :param connection: The sockets' connection object.

        :return: The received message from the server.
        """

        if connection is None:
            connection = self.connection
        # end if

        return super().receive(connection=connection)
    # end receive

    def connect(self, host: Host, port: Port) -> None:
        """
        Creates the sockets' connection for the client object with the server.

        :param host: The ip address of the server.
        :param port: The port for the server connection.
        """

        self.host = host
        self.port = port

        self.connection.connect((self.host, self.port))
    # end connect

    def send_message_to_server(self, message: bytes) -> None:
        """
        Sends a message to the server through the sockets' connection.

        :param message: The message to send to the server.
        """

        return self.send(connection=self.connection, message=message)
    # end send_message_to_server

    # defines a method to receive a message form hte server
    def receive_message_from_server(self) -> bytes:
        """
        Gets the received message from the server.

        :return: The received response from the server.
        """

        return self.receive(connection=self.connection)
    # end receive_message_from_server
# end SocketClient

class ClientsCollection(BaseModel):
    """A data class to contain clients within the server data."""

    def __init__(self, clients: Optional[dict] = None) -> None:
        """
        Defines the base data class to contain the clients.

        :param clients: The base dictionary to contain the clients' data.
        """

        self.clients = clients or {}
    # end __init__

    # defines a method to set a client
    def set_client(
            self, address: Address, connection: Optional[Socket] = None
    ) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """

        self.clients[address] = connection
    # end add_client

    def get_client(self, address: Address) -> dict:
        """
        Returns the client object inside the data class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients[address]
    # end get_client

    def pop_client(self, address: Address) -> dict:
        """
        Pops out and returns the client object from the data  class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.pop(address)
    # end pop_client

    def remove_client(self, address: Address) -> None:
        """
        Removes the client object from the data class.

        :param address: The tuple of the ip address and the port of the connection
        """

        self.pop_client(address)
    # end remove_client
# end ClientsCollection

class SocketServer(Communication, BaseModel):
    """The server object to control the communication ith multiple clients."""

    def __init__(self) -> None:
        """Defines the server datasets for clients and client commands."""

        self.socket = None
        self.listening_process = None
        self.timeout_process = None

        self.host = None
        self.port = None

        self.block = False
        self._built = False

        self.clients = ClientsCollection()
    # end __init__

    def built(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return self._built
    # end built

    def created(self) -> bool:
        """
        Checks if the service was created.

        :return: The value for the service being created.
        """

        return self.listening_process is not None
    # end created

    def blocked(self) -> bool:
        """
        Returns the value of te execution being blocked by the service loop.

        :return: The blocking value.
        """

        return self.block
    # end blocked

    def running(self) -> bool:
        """
        Checks if the service is currently running.

        :return: The boolean value.
        """

        if not self.created():
            return False
        # end if

        return self.listening_process.is_alive()
    # end running

    def connect(self, connection: Socket, host: Host, port: Port) -> None:
        """
        Creates the sockets' connection of the server and listens to clients.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        """

        self.socket = connection

        self.socket.bind((host, port))

        self._built = True
    # end connect

    def respond(self, address: Address, connection: Socket) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """
    # end respond

    def handle(self) -> None:
        """Sends a message to the client by its connection."""

        connection, address = self.socket.accept()

        self.clients.set_client(address=address, connection=connection)

        self.respond(address=address, connection=connection)

        self.clients.pop_client(address=address)
    # end handle

    def listen(self) -> None:
        """Runs the threads to listen to clients with requests."""

        self.socket.listen()

        while self.running():
            threading.Thread(target=self.handle).start()
        # end while
    # end listen_to_clients

    def create(
            self,
            connection: Socket,
            host: Host,
            port: Port,
            daemon: Optional[bool] = True
    ) -> None:
        """
        Creates the process to run the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param daemon: The value to set the process as daemon.
        """

        if not self.built():
            self.connect(connection=connection, host=host, port=port)
        # end if

        self.listening_process = threading.Thread(
            target=self.listen, daemon=daemon
        )
    # end create

    def run(
            self,
            connection: Socket,
            host: Host,
            port: Port,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            timeout: Optional[Union[int, float, dt.timedelta, dt.datetime]] = None
    ) -> Optional[threading.Thread]:
        """
        Runs the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param timeout: The timeout for the process.
        """

        process = None

        if self.running():
            return
        # end if

        if not self.created():
            self.create(
                connection=connection, host=host,
                port=port, daemon=daemon
            )
        # end if

        self.listening_process.start()

        if block:
            self.block = True
        # end if

        if timeout:
            process = self.timeout(timeout)
        # end if

        while self.blocked():
            pass
        # end while

        return process
    # end run

    def rerun(
            self,
            connection: Socket,
            host: Host,
            port: Port,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            timeout: Optional[Union[int, float, dt.timedelta, dt.datetime]] = None
    ) -> Optional[threading.Thread]:
        """
        Runs the api service.

        :param connection: The connection socket.
        :param host: The host of the server.
        :param port: The port of the server.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param timeout: The timeout for the process.
        """

        if self.running():
            self.terminate()
        # end if

        return self.run(
            connection=connection, host=host, port=port,
            daemon=daemon, block=block, timeout=timeout
        )
    # end run

    def timeout(
            self,
            timeout: Union[int, float, dt.timedelta, dt.datetime],
            block: Optional[bool] = False
    ) -> Optional[threading.Thread]:
        """
        Waits to terminate the process.

        :param timeout: The amount of seconds to wait before termination.
        :param block: The value to block the process.
        """

        if isinstance(timeout, dt.datetime):
            timeout = timeout - dt.datetime.now()
        # end if

        if isinstance(timeout, dt.timedelta):
            timeout = timeout.total_seconds()
        # end if

        if block:
            time.sleep(timeout)

            self.terminate()

        else:
            self.timeout_process = threading.Thread(
                target=lambda: (time.sleep(timeout), self.terminate())
            )

            self.timeout_process.start()

            return self.timeout_process
        # end if
    # end timeout

    def terminate(self) -> None:
        """Pauses the process of service."""

        if not self.running():
            return
        # end if

        terminate_thread(self.listening_process)
    # end terminate

    def send_message_to_client(self, message: bytes, connection: Socket) -> None:
        """
        Sends a message to the client by its connection.

        :param message: The message to send to the client.
        :param connection: The sockets' connection object.
        """

        return self.send(connection=connection, message=message)
    # end send_message_to_client

    # defines a method to receive a message form hte server
    def receive_message_from_client(self, connection: Socket) -> bytes:
        """
        Receive a message from the client by its connection.

        :param connection: The sockets' connection object.

        :return: The returned data.
        """

        return self.receive(connection=connection)
    # end receive_message_from_client

    def disconnect_client(self, connection: Socket) -> None:
        """
        Disconnects the client from the server through the connection.

        :param connection: The sockets' connection object.
        """

        return self.brute_disconnect_client(connection)
    # end disconnect_client

    # defines a method to receive a message form hte server
    @staticmethod
    def brute_disconnect_client(connection: Socket) -> None:
        """
        Disconnects the client from the server through the connection.

        :param connection: The sockets' connection object.
        """

        return connection.close()
    # end brute_disconnect_client

    def get_client(self, address: Address) -> dict:
        """
        Returns the client object inside the data class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.get_client(address)
    # end get_client

    def pop_client(self, address: Address) -> dict:
        """
        Pops out and returns the client object from the data  class.

        :param address: The tuple of the ip address and the port of the connection

        :return: The object that represents the client in the dataset.
        """

        return self.clients.pop_client(address)
    # end pop_client

    def remove_client(self, address: Address) -> None:
        """
        Removes the client object from the data class.

        :param address: The tuple of the ip address and the port of the connection
        """

        self.clients.remove_client(address)
    # end remove_client
# end SocketServer

def bluetooth_socket_request(
        host: Host,
        port: Port,
        endpoint: str,
        parameters: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Sends a request through the bluetooth sockets.

    :param host: The request host.
    :param endpoint: The path to the endpoint.
    :param port: The sending port.
    :param parameters: The request parameters.

    :return: The returned value.
    """

    # noinspection PyUnresolvedReferences
    connection = socket.socket(
        socket.AF_BLUETOOTH, socket.SOCK_STREAM,
        socket.BTPROTO_RFCOMM
    )

    client = SocketClient(connection=connection)
    client.connect(host=host, port=port)

    # noinspection HttpUrlsUsage
    url = f"http://127.0.0.1:5555/{endpoint}"

    req = PreparedRequest()
    req.prepare_url(url, parameters or {})

    client.send(message=req.url.encode())
    content = client.receive()

    connection.close()

    return decode(content.decode())
# end bluetooth_socket_request