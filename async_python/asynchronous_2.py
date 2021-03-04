"""
Changes:
    - Add event_loop(): Function with while True loop, which manage 2 other funcs.
        + select.select(to_monitor, [], []) look for files(sockets) in to_monitor list, and return files
            which are in a read_available state.
        + when select returns socket -> check: server(call accept_connection()) or client(call send_message()).
    - Add to_monitor list to store in it sockets(First of all put server_socket in it,
        then after .accept() - put client_socket).
    - Make all functions independent(now we can execute each func when we want).
Result:
    Now we have simple async application.
"""

import socket
from select import select

to_monitor = []  # -> list of files(sockets) which we need to check reading (in select())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # .accept() -> blocking function!
    print('Connection from: ', addr)
    to_monitor.append(client_socket)  # after creating connection we need to put client_socket to the to_monitor


def send_message(client_socket):
    """We don`t need while loop anymore, because event_loop manage execution by itself."""
    request = client_socket.recv(
        4096)  # Connection completed, receive request from client. .recv() -> blocking function!
    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()  # if we kill client -> close connection


def event_loop():
    """Function which manage calls."""
    while True:
        # Check if file(socket) in to_monitor in read state, than returns this file(socket)
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:  # if client_socket
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)  # Add first server_socket
    event_loop()
