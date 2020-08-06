import socket
import threading


DEFAULT_BUFFER_SIZE = 1024


class TcpClient:
    # Constructor

    def __init__(self, ip: str =None, port: int =None, accepted_socket=None):
        if accepted_socket is not None:
            self._socket = accepted_socket
        elif ip is not None and port is not None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((ip, port))
        else:
            raise ValueError("Either the socket should be passed in the parameters or the ip/port of the server.")
        self.on_msg_received = None
        self.on_shutdown = None
        self._receive_msg_thread = None
        
        self._buffer_size = DEFAULT_BUFFER_SIZE
    
    # Properties
    @property
    def socket(self):
        return self._socket

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self._buffer_size = buffer_size
    # /Properties

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
    # /Events

    # Event triggers
    def _trigger_msg_received(self, msg : bytes):
        if self._on_msg_received is not None:
            self._on_msg_received(msg)

    def _trigger_shutdown(self):
        if self._on_shutdown is not None:
            self._on_shutdown()
    # /Event triggers

    # Private methods
    def _handle_receive_msg(self):
        while True:
            try:
                buffer = self._socket.recv(self._buffer_size)
            except OSError:
                self._trigger_shutdown()
                break
            # Server shutdown
            if len(buffer) == 0:
                self._trigger_shutdown()
                break
            
            self._trigger_msg_received(buffer)

    @staticmethod
    def _parse_header(header_bytes : bytes):
        header_str = header_bytes.decode("utf-8")
        length = int(header_str)
        return {
            "length": length
        }
    # /Private methods

    # Public methods
    def start_receiving(self):
        self._receive_msg_thread = threading.Thread(target=self._handle_receive_msg)
        self._receive_msg_thread.start()

    def send(self, msg : bytes):
        self._socket.send(msg)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    # /Public methods
