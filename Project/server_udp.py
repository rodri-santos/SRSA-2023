import configparser
import sys
import socket

ThreadCount = 0
Client_number = 0

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.9.0.2"
port = 5001
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    sys.exit(1)

print(f'UDP server is listening in address {host} and port {port} ...')

try:
    while True:
        data, addr = ServerSocket.recvfrom(1024)
        Client_number += 1
        decoded_data = data.decode('utf-8')

        print(f'{decoded_data}')


except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
finally:
    ServerSocket.close()