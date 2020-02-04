import socket
import threading
HEADER_SIZE = 10
conn_id = 0
header = None
connections = []


def dispatch_message(message, id):
    print("Dispatching message: '" + message + "' from ID '" + str(id) + "'")
    message = message + "\nMessage: "
    message = f'{len(message.encode("utf-8")):<10}' + message
    message = message.encode("utf-8")
    for connection in connections:
        if connection[0] != id:
            print("Sending to ID: " + str(connection[0]))

            connection[1].send(bytes(message))


def handle_client(s, a, id):
    global header
    print(f"Connection from {a} has been established")
    while True:
        new_message = True
        while True:
            if new_message:
                new_message = False
                try:
                    header = str(s.recv(HEADER_SIZE).decode("utf-8"))
                except ConnectionResetError:
                    for index, connection in enumerate(connections):
                        if connection[0] == id:
                            conn = connections.pop(index)
                            conn[1].close()
                            print(f"Connection from {a} has been closed")
                            return
                if len(header) != 0:
                    message_length = int(header)
                    print(f'New message from {a}! Length: {message_length}')
                    message = s.recv(message_length).decode("utf-8")
                    if message.split()[-1] == "exit":
                        for index, connection in enumerate(connections):
                            if connection[0] == id:
                                conn = connections.pop(index)
                                conn[1].close()
                                print(
                                    f"Connection from {a} has been closed by user")
                                return
                    print(message)
                    dispatch_message(message, id)
                    break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1234))
print("Server started at {}:{}".format(
    socket.gethostbyname(socket.gethostname()), 1234))
s.listen(5)


while True:
    print("Waiting for connection...")
    clientsocket, address = s.accept()
    connections.append((conn_id, clientsocket))
    threading.Thread(target=handle_client, args=(
        clientsocket, address, conn_id), daemon=True).start()
    conn_id += 1
