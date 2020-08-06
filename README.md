## tinytcp
Event based package for tcp server/client on top of python sockets package

### TcpClient
TcpClient one class for two cases: from the client side, it would be used to initiate the connection, and from the server side, it would be used on the accepted socket.
For client, TcpClient constructor would take ip and port of the server, and for the server, TcpClient constructor would have the accepted socket.
TcpClient have a method to start receiving asynchronously, once there is a message it triggers the message received handler function.

### TcpServer
It has a method to start listening to incoming connections asynchronously, once there is a new connection, it initiates a new TcpClient object with the accepted sockets, it links the events, and makes it start receiving messages.
