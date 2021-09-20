# from the socket module import all
import socket

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set values for host 'localhost' - meaning this machine and port number 10000
# the machine address and port number have to be the same as the server is using.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
server_address = (host_ip, 10000)
# output to terminal some info on the address details
print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port
sock.connect(server_address)

try:
    
    # Send data
    print("Please enter a message: ")
    message = input()
    print('sending "%s"' % message)
    # Data is transmitted to the server with sendall()
    # encode() function returns bytes object
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
    	# Data is read from the connection with recv()
        # decode() function returns string object
        data = sock.recv(16).decode()
        amount_received += len(data)
        print('received "%s"' % data)
    storage = ''
    flag = "END FLAG"
    sock.sendall(flag.encode())
    while True:
        # decode() function returns string object
        data = sock.recv(16).decode()
        if data:
            # encode() function returns bytes object
            storage += data
        else:
            print('no more data from server')
            break
    print(storage)

finally:
    print('closing socket')
    sock.close()