# from the socket module import all
import socket
import datetime

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# if we did not import everything from socket, then we would have to write the previous line as:
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set values for host 'localhost' - meaning this machine and port number 10000
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
server_address = (host_ip, 10000)
# output to terminal some info on the address details
print('*** Server is starting up on %s port %s ***' % server_address)
# Bind the socket to the host and port
sock.bind(server_address)

# Listen for one incoming connections to the server
sock.listen(1)
log = ""
recv_size = 16
# we want the server to run all the time, so set up a forever true while loop
while True:

    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    # accept() returns an open connection between the server and client, along with the address of the client
    connection, client_address = sock.accept()
    content = ""
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            # decode() function returns string object
            data = connection.recv(recv_size).decode()
            content += data
            if data and data != "END FLAG":
                print('received "%s"' % data)
                print('sending data back to the client')
                # encode() function returns bytes object
                connection.sendall(data.encode())
            else:
                timestamp = datetime.datetime.now()
                log1 = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
                log1 += " "
                content = content[0:-8]
                print("Content as of now" + content)
                log1 += content
                connection.sendall(log1.encode())
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing connection")
        connection.close()
        f = open("log.txt", "w+")
        f.write(log1)
        f.close()
# now close the socket
sock.close();