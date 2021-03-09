"""
Changes:
    - Add help structures like tasks, r_r ,r_w , r_t_r , r_t_w.
    - Rewrite event_loop to manage sockets and generators.
Result:
    - Async app with generators (see write notes).
"""

import socket
from select import select

tasks = []  # Right generators here

to_read = {}  # key:socket, val:generator
to_write = {}  # key:socket, val:generator


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()  # .accept() -> blocking function!  READ

        print('Connection from: ', addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield 'read', client_socket
        request = client_socket.recv(
            4096)  # Connection completed, receive request from client. .recv() -> blocking function!  READ

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()

            yield 'write', client_socket
            client_socket.send(response)  # .send() -> blocking function!  WRITE

    client_socket.close()  # if we kill client -> close connection


def event_loop():
    """Function which manage calls."""
    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))  # Only generators here (tuple('read/write',gen))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))  # Only generators here

        try:
            task = tasks.pop(0)  # generator

            reason, sock = next(task)  # tuple  MAIN PART where all is executed

            if reason == 'read':
                to_read[sock] = task

            if reason == 'write':
                to_write[sock] = task

        except StopIteration:
            print('All done!')


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
