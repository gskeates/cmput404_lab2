#!/usr/bin/env python3
import socket, sys, time
from multiprocessing import Process

# create a tcp socket
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()

    return s

# get web_host information
def get_remote_ip(web_host):
    try:
        remote_ip = socket.gethostbyname( web_host )
    except socket.gaierror:
        print ('web_hostname could not be resolved. Exiting')
        sys.exit()

    return remote_ip

# send data to server
def send_data(serversocket, payload):
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()

def client_connection(conn, addr):

    # Step 2 - connect to google
    try:
        # define address info, payload, buffer size
        host = 'www.google.com'
        port = 80
        buffer_size = 4096

        # make the socket, get the ip, and connect
        web_socket = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        web_socket.connect((remote_ip , port))
        print (f'Proxy server connected to {host} on ip {remote_ip}')


        # Step 3 - receive data from proxy client, send to google
        print('Connected to ', addr)

        payload = conn.recv(buffer_size)

        web_socket.sendall(payload)
        web_socket.shutdown(socket.SHUT_WR)

        # continue accepting data until no more left
        full_data = b""
        while True:
            data = web_socket.recv(buffer_size)
            if not data:
                 break
            full_data += data
        # Step 4 - send received data back to proxy client
        conn.sendall(full_data)

    except Exception as e:
        print(e)

    finally:
        # always close at the end!
        web_socket.close()

def main():
    # Step 1 - listen for incoming connections from proxy_client
    num_connections = 10
    # create server socket
    server_socket = create_tcp_socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind socket to address
    server_socket.bind(("", 8001))
    # set to listening mode
    server_socket.listen(num_connections)

    # continuously listen for connections
    while True:
        conn, addr = server_socket.accept()

        # Spawn new process to deal with connection
        process = Process(target=client_connection, args=(conn, addr))
        process.start()

        conn.close()



if __name__ == "__main__":
    main()
