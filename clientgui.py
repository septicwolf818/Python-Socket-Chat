import socket
import threading
from tkinter import *
from tkinter import messagebox
import time


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
                    _label = Label(messages_container, text="\n".join(message.split(
                        "\n")[:-1]), anchor=W, wraplength=240, justify="left", fg="white", bg="black").grid(column=0, sticky=W)
                    break


def start_chat():

    grid_list = root.grid_slaves()
    for widget in grid_list:
        widget.destroy()
    root.geometry("500x500")
    root.title(base_title + connected_title +
               str(connection_host)+":"+str(connection_port))
    global messages_container
    global message_label
    global message_entry
    messages_main_container.grid(
        column=0, row=0, columnspan=2, sticky="we")
    message_label.grid(column=0, row=1)
    message_entry.grid(column=1, row=1, sticky="wes")


def connect(host, port):
    _host = host
    _port = int(port)
    try:
        s.connect((_host, _port))
        threading.Thread(target=handle_messages,
                         args=(s,), daemon=True).start()
        global connection_host
        global connection_port
        global nick
        connection_host = host
        connection_port = port
        nick = nick_entry.get()
        start_chat()

    except Exception as e:
        print(str(e))
        messagebox.showerror("Connection error", str(e))
        exit(0)


def send_message(_):
    msg = message_entry.get()
    message_entry.delete(0, END)
    message_entry.insert(0, "")
    _label = Label(messages_container, text=msg,
                   anchor=E, wraplength=240, justify="right").grid(column=1, sticky=E)

    msg_cp = msg
    msg = nick + ": " + msg
    msg = f'{len(msg.encode("utf-8")):<10}' + msg
    s.send(bytes(msg.encode("utf-8")))
    if msg_cp == "exit":
        exit(0)


HEADER_SIZE = 10
nick = None
connection_host = None
connection_port = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# GUI init
# application base title and options
base_title = "Python Socket Chat Client"
connect_title = " | Connect"
connected_title = " | Connected to "


# main window
root = Tk()
root.title(base_title + connect_title)
root.geometry("400x90")
root.resizable(False, False)
root.grid_columnconfigure(1, weight=1)

# connection
host_label = Label(root, text="IP")
host_entry = Entry(root)
port_label = Label(root, text="PORT")
port_entry = Entry(root)
nick_label = Label(root, text="NICK")
nick_entry = Entry(root)
connect_button = Button(root, text="Connect", width=400, command=lambda: connect(
    host_entry.get(), port_entry.get()))
connect_button.bind('<Return>', lambda e: connect(
    host_entry.get(), port_entry.get()))

# chat
messages_main_container = Frame(root, height=475)
messages_main_container.pack_propagate(0)
messages_canvas = Canvas(messages_main_container)
messages_container = Frame(messages_canvas)
messages_container.grid_columnconfigure(0, minsize=240)
messages_container.grid_columnconfigure(1, minsize=240)
messages_scrollbar = Scrollbar(
    messages_main_container, command=messages_canvas.yview)
messages_scrollbar.pack(side="right", fill="y")
messages_canvas.pack(side="left", fill="both", expand=True)
messages_canvas.config(yscrollcommand=messages_scrollbar.set)
messages_canvas.create_window((0, 0), window=messages_container, anchor="nw")
messages_container.bind("<Configure>", lambda e: [messages_canvas.configure(
    scrollregion=messages_canvas.bbox("all"), width=e.width),
    messages_canvas.yview_moveto(1)])
message_label = Label(root, text="Message")
message_entry = Entry(root)
message_entry.bind('<Return>', send_message)


# GUI connection - show

host_label.grid(column=0, row=0)
host_entry.grid(column=1, row=0, sticky='we')
port_label.grid(column=0, row=1)
port_entry.grid(column=1, row=1, sticky='we')
nick_label.grid(column=0, row=2)
nick_entry.grid(column=1, row=2, sticky='we')
connect_button.grid(column=0, row=3, columnspan=2)

root.mainloop()
