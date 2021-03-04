"""
Changes:
    - Replace .select() -> selectors.
        + Allow us bound socket with right function (server-accept_connection/client-send_message).
        + Make simpler event_loop.
        = Create selector object.
        = Register (and bound wih function).
    - Refactoring: put server_socket creation into server().
Result:
    - Async app on callbacks.
"""

import socket
import selectors

# The same as .select() (almost)
selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    # Register socket, give parameters
    # (1]File_object(server_socket), 2]Event that we interested in, 3]Bounded data)
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # .accept() -> blocking function!
    print('Connection from: ', addr)
    # Register socket, give parameters
    # (1]File_object(client_socket), 2]Event that we interested in, 3]Bounded data)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    """We don`t need while loop anymore, because event_loop manage execution by itself."""
    request = client_socket.recv(
        4096)  # Connection completed, receive request from client. .recv() -> blocking function!
    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        # Unregister socket before closing
        selector.unregister(client_socket)
        client_socket.close()  # if we kill client -> close connection


def event_loop():
    """Function which manage calls."""
    while True:
        events = selector.select()  # ->(SelectorKey-object,events[read/write])
        # SelectorKey -> named tuple with fields: fileobj,events,data
        for key, _ in events:
            # Getting bounded_data(function) and call it with file(socket) from SelectorsKey
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
