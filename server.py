#!/usr/bin/python3

import sys
import os

from tinytcp import TcpClient
from tinytcp import TcpServer

def main():
    global server
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], " <port>")
        return
    ip = "0.0.0.0"
    try:
        port = int(sys.argv[1].strip())
    except ValueError:
        print("Usage: ", sys.argv[0], " <port>")
        return

    try:
        server = TcpServer(ip, port)
    except Exception as e:
        print("Error: ", e)
        return

    server.on_client_connect = handle_client_connect
    server.on_msg_received = handle_message_received
    server.on_shutdown = handle_shutdown
    server.start_listening()
    while True:
        input("> ")


def handle_client_connect(client: TcpClient):
    client_address = client.socket.getpeername()
    print(f"{client_address} connected.")


def handle_message_received(client: TcpClient, msg: bytes):
    msg_str = msg.decode()
    client_address = client.socket.getpeername()
    print(f"{client_address}: {msg_str}")
    broadcast(server, msg_str)


def handle_shutdown(client: TcpClient):
    client_address = client.socket.getpeername()
    print(f"{client_address} disconnected.")


def broadcast(server: TcpServer, msg: str) -> None:
    msg_bytes = msg.encode()
    for client in server.clients:
        client.send(msg_bytes)


if __name__ == "__main__":
    main()

def str_to_bytes(text: str):
    return text.encode()

def bytes_to_str(msg_bytes: bytes):
    return msg_bytes.decode(encoding="utf8")