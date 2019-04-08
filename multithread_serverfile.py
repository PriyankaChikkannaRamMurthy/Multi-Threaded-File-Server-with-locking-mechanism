import os
import socket
import threading
userResponse = 0
multi_lock = threading.Lock()
def fileOperation(name, sock):
    userResponse = sock.recv(1024)
    print (userResponse[:2])
    if userResponse[:2] == '2':
        while 1:
            if not multi_lock.acquire():
                # Get filename from the user
                filename = sock.recv(1024)
                # If the file exists and is a file
                if os.path.isfile('server/' +filename):
                    sock.send("EXISTS" + str(os.path.getsize('server/'+ filename)))
                    userResponse = sock.recv(1024)
                    if userResponse[:2] == 'OK':
                        # Assuming the user wants to read the file
                        with open('server/'+ filename, 'rb') as f:
                        # Bytes to be sent
                            bytesToSend = f.read(1024)
                            sock.send(bytesToSend)
                             # If file size is greater than 1024 then we get more bytes to send
                            while bytesToSend != "":
                                bytesToSend = f.read(1024)
                                sock.send(bytesToSend)
                else:
                    print("File not found!!")
                    sock.send("ERROR")

    elif userResponse[:2] == '1':
        multi_lock.acquire()
        fname=sock.recv(1024).decode('utf-8')
        if os.path.isfile('server/' +fname):
            print("File is present in server already!!!")
            sock.send("EXISTS" + str(os.path.getsize('server/'+ fname)))
            sock.recv(1024)
            multi_lock.release()
        else:
            sock.send("SUCCESS")
            file_upload = open('server/' + fname, 'wb')
            with file_upload as write_file:
                while 1:
                    content_file = sock.recv(1024)
                    #print(file_content)
                    if not content_file:
                        break
                    write_file.write(content_file)
            file_upload.close()
            multi_lock.release()
        print("File Upload Successful!!!")




    elif userResponse[:2] == '3':
        while 1:
            if not multi_lock.acquire():
                sock.sendall('OK'.encode('utf-8'))
                # Get filename from the user
                filename = sock.recv(1024)
                # If the file exists and is a file
                if os.path.isfile('server/' + filename):
                    sock.send("EXISTS" +str(os.path.getsize('server/' + filename)))
                    os.remove('server/' +filename)
                    print("File removed successfully!")
                else:
                    sock.send("ERROR")



    elif userResponse[:2] == '4':
        multi_lock.acquire()
        # Get filename from the user
        filename = sock.recv(1024)
        # If the file exists and is a file
        if os.path.isfile('server/' + filename):
            sock.send("EXISTS" + str(os.path.getsize('server/' + filename)))
            new_filename = sock.recv(1024)
            print(new_filename)
            os.rename('server/' +filename, 'server/' +new_filename)
            sock.send("SUCCESS")
            save_path = 'C:\\Shwetha\\MS\\Sem4\\Distributed Systems\\Projects\\Project1\\Client-Server\\server'
            new_filetxt = new_filename
            print(new_filetxt)
            reName = os.path.join(save_path, new_filetxt)
            print(reName)
            print("Success in Renaming the file!!!")
        else:
            print("file does not exist!!!")
            sock.send("ERROR")
            multi_lock.release()

    else:
        sock.send("ERROR")


    sock.close()

def Main():
    host = '127.0.0.1'
    port = 5051
    # Creating a socket
    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_sock.bind((host,port))
    # Server listening for connections
    new_sock.listen(10)
    print("Server started, waiting for client to accept request...")
    while True:
        # Get the connection socket
        connection, ip_address = new_sock.accept()
        print("Client connected to ip-address: ")
        print("<", str(ip_address), ">")
        thread = threading.Thread(target=fileOperation, args=("MultiThreading", connection))
        # Starting thread
        thread.start()



if __name__ == '__main__':
    Main()