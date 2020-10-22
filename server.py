import socket 
import threading
import os

HEADER=64 
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT='utf-8'
DISCONNECT_MESSAGE="!Disconnected"

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def ret_file(name,sock):
    filename= (sock.recv(1024))
    fname=filename.decode('utf-8')
    if os.path.isfile(fname):
        data="EXISTS " + str(os.path.getsize(filename))
        send_data = data.encode('utf-8')
        sock.send(send_data)
        response = sock.recv(1024)
        user_response=response.decode()
        if user_response[:2]=='OK':
            with open(filename,'rb') as f:
                bytes_send=f.read(1024)
                sock.send(bytes_send)
                while bytes_send != "":
                    bytes_send=f.read(1024)
                    sock.send(bytes_send)
    else:
        sock.send("error")
    sock.close()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected=True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MESSAGE:
               connected=False

            print(f"[{addr}] {msg} ")
            conn.send("msg recived".encode(FORMAT))
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER} ")
    while True:

        conn, addr = server.accept()
        thread_msg = threading.Thread(target=handle_client, args=(conn,addr))
        thread_file =threading.Thread(target=ret_file, args=("retrThread",conn))

        choice_recv = conn.recv(1024)
        choice = choice_recv.decode('utf-8')
        if choice=='1':
            
            thread_msg.start()
        if choice=='2':
            print("you are in")
            thread_file.start()     
        print(f"[ACTIVE CONNTECTIONS] {threading.activeCount()-1}")



print("[STARTING] Server is starting....")
start()



