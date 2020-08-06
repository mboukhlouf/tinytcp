import socket
import threading

from . import TcpClient


CONNECTION_QUEUE_SIZE = 10
DEFAULT_BUFFER_SIZE = 1024


class TcpServer:
    def __init__(self, ip : str, port : int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._socket.bind((ip, port))

        self._clients = list()
        self.on_client_connect = None
        self.on_msg_received = None
        self.on_shutdown = None
        self._listening_thread = None
        self._buffer_size = DEFAULT_BUFFER_SIZE

    @property
    def socket(self):
        return self._socket

    @property
    def clients(self):
        return self._clients

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self._buffer_size = buffer_size

    # Events
    @property
    def on_msg_received(self):
        return self._on_msg_received

    @on_msg_received.setter
    def on_msg_received(self, on_msg_received):
        self._on_msg_received = on_msg_received

    @property
    def on_shutdown(self):
        return self._on_shutdown

    @on_shutdown.setter
    def on_shutdown(self, on_shutdown):
        self._on_shutdown = on_shutdown

    @property
    def on_client_connect(self):
        return self._on_client_connect

    @on_client_connect.setter
    def on_client_connect(self, on_client_connect):
        self._on_client_connect = on_client_connect

    # /Events
    
    # Event triggers
    def _trigger_msg_received(self, client: TcpClient, msg: bytes):
        if self._on_msg_received is not None:
            self._on_msg_received(client, msg)

    def _trigger_shutdown(self, client: TcpClient):
        self.clients.remove(client)
        if self._on_shutdown is not None:
            self._on_shutdown(client)
    
    def _trigger_client_connect(self, client: TcpClient):
        if self._on_client_connect is not None:
            self._on_client_connect(client)
    # /Event triggers

    def _handle_listening(self):
        self.socket.listen(CONNECTION_QUEUE_SIZE)
        while True:
            accepted_socket, _ = self.socket.accept()
            client = TcpClient(accepted_socket=accepted_socket)
            client.on_msg_received = lambda msg: self._trigger_msg_received(client, msg)
            client.on_shutdown = lambda : self._trigger_shutdown(client)
            client.buffer_size = self.buffer_size
            self.clients.append(client)
            client.start_receiving()
            self._trigger_client_connect(client)
            
        
    def start_listening(self):
        self._listening_thread = threading.Thread(target=self._handle_listening)
        self._listening_thread.start()