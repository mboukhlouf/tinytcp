# Notes

## Tcp package
I've made this package as a first step, to make it easier to work with Tcp. TcpServer makes a socket that listens to a port asynchronously.

### TcpClient
TcpClient one class for two cases: from the client side, it would be used to initiate the connection, and from the server side, it would be used on the accepted socket.
For client, TcpClient constructor would take ip and port of the server, and for the server, TcpClient constructor would have the accepted socket.
TcpClient have a method to start receiving asynchronously, once there is a message it triggers the message received handler function.

### TcpServer
It has a method to start listening to incoming connections asynchronously, once there is a new connection, it initiates a new TcpClient object with the accepted sockets, it links the events, and makes it start receiving messages.

### Message header
To be able to send and receive messages however big they are and however the size of the buffer is, every message transmitted will start with a header that contains how many bytes are there. So the socket receiving the message would know where a message stops.

The buffer size can be 1 and still works fine.
