import socket 

HEADER=64 

PORT = 5000
FORMAT='utf-8'
DISCONNECT_MESSAGE="!Disconnected"
SERVER= socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, PORT)

client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send():
    msg= input("Enter your message: ")
    message = msg.encode(FORMAT)
    msg_length=len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))
    client.close()

def file_send():

    filename=input("filename? -> ")
    fname=filename.encode('utf-8')
    if filename:
        client.send(fname)
        data=client.recv(1024)
        data_decode=data.decode('utf-8')
        if data_decode[:6]=='EXISTS':
            
            filesize=float(data[6:])
            print(data_decode)
            message = input("File exists.  " + str(filesize)+ "Bytes, Download? (Y/N) -> ")
            if message=="Y":
                client.send('OK'.encode('utf-8'))
                f=open('new_'+filename, 'wb')
                data=client.recv(1024)
                total_recv= len(data)
                f.write(data)
                while total_recv<filesize:
                    data=client.recv(1024)
                    total_recv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((total_recv/float(filesize))*100))
                print("Download complete")
        else:
            print("file does not exist")
    client.close()

def Main():
    flag=1
    while flag==1:
        print("\nPress 1 to send message")
        print("\nPress 2 to request a file")
        print("\npress 3 to exit")
        choice = int(input("\nEnter your choice: "))
        print(choice)
        if choice==1:
            client.send("1".encode('utf-8'))
            send()

        elif choice==2:
            client.send("2".encode('utf-8'))
            file_send()
        elif choice==3:
            flag=0
        else:
            print("Wrong choice")

if __name__ == '__main__':
    Main()


    


