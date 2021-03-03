"""
Simple client-server application
Current problem:
1) Server can`t serve more than one client (We should give control to the other clients while current client 'thinking')
Solution: - We should give control to the other clients;
          - Code-manager. Event loop.
          1) Callbacks;
          2) Generators and Coroutines;
          3) async/await.

"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

while True:
    client_socket, addr = server_socket.accept()  # .accept() -> blocking function!
    print('Connection from: ', addr)

    while True:
        # stay here, before client message!
        request = client_socket.recv(4096)  # .recv() -> blocking function!

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()
            client_socket.send(response)

    print('Outside inner while loop')  # See this message if kill first client
    client_socket.close()
