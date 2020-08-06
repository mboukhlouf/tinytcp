#!/usr/bin/python3

import sys
import os

from tinytcp import TcpClient

def main():
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], " <server-hostname> <server-port>")
        return
    ip = sys.argv[1]
    try:
        port = int(sys.argv[2].strip())
    except ValueError:
        print("Usage: ", sys.argv[0], " <server-hostname> <server-port>")
        return

    print("Connecting...")
    try:
        smtp_client = TcpClient(ip, port)
    except ConnectionRefusedError:
        print("Connection refused.")
        return
    print("Connected.")
    smtp_client.on_msg_received = handle_message
    smtp_client.on_shutdown = server_shutdown
    smtp_client.start_receiving()

    while True:
        s = input('> ')
        msg = s.encode("utf-8")
        if s == "quit":
            smtp_client.close()
        else:
            smtp_client.send(msg)


def handle_message(msg : bytes):
    with open("received_image.jpg", "wb") as f:
        f.write(msg)
    print("file received and written")


def server_shutdown():
    print("Server shutdown.")
    os._exit(0)


if __name__ == "__main__":
    main()