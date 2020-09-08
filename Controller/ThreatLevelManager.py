import sys
import threading
import socket


class TUCommunicator(threading.Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 58678))

    def run(self):
        self.sock.listen()

        (client, addr) = self.sock.accept()
        print(addr, " has connected.")

        while True:
            response = ""

            rdat = client.recv(1024).decode()

            print("Received: ", rdat)

            if rdat.startswith("tupdate"):
                res = setTimeout(rdat.split('.')[1:3])
                if res == 0:
                    response = "ACK"
                else:
                    response = "ERR"
            elif rdat == "init":
                response = "ACK"
            else:
                exit(2)

            client.send(response.encode())


# Global variables
min_timeout = 0
max_timeout = 0


def setTimeout(vals):
    try:
        global min_timeout, max_timeout
        min_timeout = vals[0]
        max_timeout = vals[1]
        print("New timeout: ", min_timeout, "/", max_timeout)
        return 0
    except IndexError:
        print("Error: invalid timeout value")
        return 1


if len(sys.argv) != 3:
    print("Usage: ThreatLevelManager [MIN_TIMEOUT] [HOUR_TIMEOUT]")
    exit(1)
else:
    min_timeout = sys.argv[1]
    max_timeout = sys.argv[2]

tuCommunicator = TUCommunicator()
tuCommunicator.start()
