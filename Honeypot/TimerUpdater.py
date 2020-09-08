import sys
import threading
import socket
import time


class TLMCommunicator(threading.Thread):
    controller_ip = ""

    def __init__(self, c_ip):
        super().__init__()
        self.controller_ip = c_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.connect((self.controller_ip, 58678))

        self.sock.send("init".encode())

        dat = self.sock.recv(1024).decode()
        print("Received: ", dat)

    def updateTimer(self, min, max):
        sdat = "tupdate." + str(min) + "." + str(max)
        self.sock.send(sdat.encode())

        rdat = self.sock.recv(1024).decode()
        print("Receive: ", rdat)

        if rdat == "ACK":
            return 0
        else:
            return 1


# Global variables
controller_ip = ""

if len(sys.argv) != 2:
    print("Usage: TimerUpdater [CONTROLLER_IP]")
    exit(1)
else:
    controller_ip = sys.argv[1]

tlmCommunicator = TLMCommunicator(controller_ip)
tlmCommunicator.start()

time.sleep(0.1)

tlmCommunicator.updateTimer(2, 60)
tlmCommunicator.updateTimer(3, 60)
