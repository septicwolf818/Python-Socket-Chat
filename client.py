import socket
import threading
HEADER_SIZE = 10


def handle_messages(_s):
    while True:
        new_message = True
        while True:
            if new_message:
                new_message = False
                header = str(_s.recv(HEADER_SIZE).decode("utf-8"))
                if len(header) != 0:
                    message_length = int(header)
                    message = _s.recv(message_length).decode("utf-8")
                    print("\r" + f'{message:>9}', end="")
                    break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Enter IP: ")
port = int(input("Enter PORT: "))
try:
    s.connect((host, port))
except Exception as e:
    print(str(e))
    exit(0)
nick = input("\rEnter your name: ")
if nick == "":
    nick = "Guest"
print("Type 'exit' to close connection")
threading.Thread(target=handle_messages, args=(s,), daemon=True).start()
while True:

    msg = input("Message: ")
    msg_cp = msg
    msg = nick + ": " + msg
    msg = f'{len(msg.encode("utf-8")):<10}' + msg
    s.send(bytes(msg.encode("utf-8")))
    if msg_cp == "exit":
        print("Connection closed")
        break
exit(0)
