import socket
import sys

port = 0

if len(sys.argv) != 2:
    print("Usage: python3 TCPServer [port]")
else:
    port = int(sys.argv[1])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 사용
sock.bind(("127.0.0.1", port))

sock.listen()
