#!/usr/bin/env python3
import socket, sys

# create a tcp socket
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    return s

# get host information
def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    return remote_ip

# send data to server
def send_data(serversocket, payload):
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()

def main():
    try:
        # define address info, payload, and buffer size
        proxy_host = '127.0.0.1'
        host = 'www.google.com'
        port = 8001
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 4096

        # make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(proxy_host)

        s.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')

        # send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)
        # continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        print("Response from host ", full_data)

    except Exception as e:
        print(e)

    finally:
        # always close at the end!
        s.close()
        
if __name__ == "__main__":
    main()
