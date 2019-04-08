import os
import sys
import socket
import time


def Upload(s):
    print("Upload File Operation")
    s.send("1")
    dir_arr = []
    message = raw_input("Do you want to upload files (Y/N)?")
    if message == "Y" or message == 'y':
        for path_dir, name_dir, files in os.walk('./client/'):
            dir_arr.extend(files)
        print (dir_arr)
        inputfile=raw_input("Enter the file to be uploaded or type 'quit' to exit :")
        print(inputfile)
        if inputfile != 'quit':
            inputfile = inputfile.split('\n')
            print(inputfile)
            if inputfile[0] in dir_arr:
                s.send(inputfile[0].encode('utf-8'))
                print("File is present and getting uploaded...")
                data = s.recv(1024)
                if data[:6] == 'EXISTS':
                    filesize = long(data[6:])
                    print("File Exists," + str(filesize) + "Bytes")
                    print("File already exists in Server!!")
                    s.send("DONE")
                else:
                    read_file=open('client/' + inputfile[0], 'rb')
                    with read_file as uploadfile:
                        for file_content in uploadfile:
                            s.sendall(file_content)
                    print("File Upload done!!!")
            else:
                print("File doesn't exist...")
        else:
            print("Quit - Upload process")
    else:
        print("Exiting the connection")
    time.sleep(5)

def Download(s):
    print("Download File Operation:")
    s.send("2")
    # Getting file name from the user
    filename = raw_input("Filename?: ")
    if filename != 'q':
        # Send server the file name
        s.send(filename)
        # If file exists
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            # Ask the user if they want to download the file
            message = raw_input("File Exists, " +str(filesize)+ "Bytes, Do you want to Download? (Y/N)?")
            if message == 'Y' or message == 'y':
                s.send('OK')
                # Open the file to write the incoming data
                f = open('client/' + filename, 'wb')
                # Start receiving the data
                data = s.recv(1024)
                # Since we are not sure of the no of bytes we are going to receive, we use the variable totalRecv that is  equal to the length of the data that we get
                totalRecv = len(data)
                # Write the data we got
                f.write(data)
                # If data is more than 1024 then we continue receiving the data
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    # Print the percentage of the file currently downloaded
                    print("{0:2f}" .format((totalRecv/float(filesize))*100)+"% Done")
                print("Download Finished")
        else:
            print("File does not Exist!")
        time.sleep(5)

def Delete(s):
    print("Delete File Operation")
    s.send("3")
    ack = s.recv(1024)
    if(ack.decode('utf-8') == 'OK'):
        message = raw_input("Enter file to delete?: ")
        if message != 'q':
            message = message.split('\n')
            s.sendall(message[0].encode('utf-8'))
            data = s.recv(1024)
            if data[:6] == 'EXISTS':
                filesize = long(data[6:])
                print("File Exists," + str(filesize)+ "Bytes")
                print("Deleting file in the system")
                if(s.recv(1024) == "ERROR"):
                    print("File doesn't exists in server")
                else:
                    print("Delete Completed")
            else:
                print("File doesn't exist in server")
    else:
        print("Exiting the connection")
    time.sleep(5)

def Rename(s):
    print("Rename File Operation")
    s.send("4")
    # Getting file name from the user
    filename = raw_input("Filename?: ")
    if filename != 'q':
        # Send server the file name
        s.send(filename)
        # If file exists
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File Exists, " + str(filesize) + "Bytes, Enter the new name for the file ->")
            s.send(message)
            data = s.recv(1024)
            if data == "SUCCESS":
                print("File is Renamed!")
                newFile = s.recv(4096)
                print("Renamed File:", newFile)
        else:
            print("File does not Exist!")
    else:
        return
    time.sleep(5)



def Main():
    host = '127.0.0.1'
    port = 5051

    # Creating a socket
    s = socket.socket()
    s.connect((host,port))
    print("Client-Server System\n")
    option = raw_input("Select an option to perform one of the following:\n 1.Upload\n 2.Download\n 3.Delete\n 4.Rename\n")
    if option == '1':
        Upload(s)
    elif option == '2':
        Download(s)
    elif option == '3':
        Delete(s)
    elif option == '4':
        Rename(s)
    else:
        s.close()
        sys.exit(0)

if __name__ == '__main__':
    Main()