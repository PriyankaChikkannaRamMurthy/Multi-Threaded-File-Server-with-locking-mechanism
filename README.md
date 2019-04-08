# Multi-Threaded-File-Server-with-locking-mechanism

Program Implementation:

Language: Python 3.6

Outcomes:

In Multithreaded server, there are multiple threads/multiple processes, which works on same data and resources at same time. So, distributed locking is necessary where it prevents the interruption between threads.

Learnings:

In this project, got a chance to learn a bit more about socket programming and a whole lot about multithreaded servers and we applied those learnings to implement the entire project.

Issues:

1.	Encoding and Decoding of data over the communication between the client and server was hard to implement.
2.	Testing all the scenarios for file operations for client-server communication like, file exist condition, connection error, file does not exist etc.,

Challenges in converting single threaded to multi-threaded server:

1.	Implementing Thread locking was difficult as locking of resources was not happening. 
2.	Keeping the download operation irrespective of upload and rename file operation was difficult.
3.	The challenge in creating a single threaded server is that it can handle only one client at a time as object for Socket handles client making it to block until the connection gets terminated so that any other client will not be connected on the same port. We should ensure that socket is freed and handled by each thread.
4.	In order, to increase the efficiency of the server for file handling operations, we ensure that multiple clients to be connected to the same server at same time and request from each client is handled concurrently. 


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Instructions to compile:

To compile in cmd:

1.	Open the directory/folder where the project resided.

2.	Run the server and client files in separate cmd terminal.

3.	First run the server file and then run the client file.

4.	Run the program as: python filename.py. Eg: python fileClient.py

5.	Choose the menu options in the client side for file operations.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
