import sys
import threading
import socket
import time
import datetime
import subprocess


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

    def updateTimer(self, min, hr):
        sdat = "tupdate." + str(min) + "." + str(hr)
        self.sock.send(sdat.encode())

        rdat = self.sock.recv(1024).decode()
        print("Receive: ", rdat)

        if rdat == "ACK":
            return 0
        else:
            return 1


# Global variables
controller_ip = ""
interface = "eth0"
c = 0

if len(sys.argv) != 4:
    print("Usage: TimerUpdater [CONTROLLER_IP] [INTERFACE] [C]")
    exit(1)
else:
    controller_ip = sys.argv[1]
    interface = sys.argv[2]
    c = int(sys.argv[3])

tlmCommunicator = TLMCommunicator(controller_ip)
tlmCommunicator.start()

time.sleep(0.1)

packetdata =[]

capture = subprocess.Popen([
    'tshark', '-l', '-i', interface, '-Tfields',
    '-e', 'frame.time_relative','-e', 'ip.src', '-e', 'ip.dst',
    '-e', 'tcp.srcport', '-e', 'tcp.flags'
], stdout=subprocess.PIPE)

linenum = 0

while True:
    line = capture.stdout.readline().decode().split("\t")
    linenum += 1
    #print("Line: ", line)

    if len(line) > 3:
        packetdata.append({
            "timestamp": float(line[0]), "src": line[1], "dst": line[2], "sport": line[3],
            "flags": line[4]
        })
        
    if linenum % 50000 == 0:
        timestamps = [packet["timestamp"] for packet in packetdata]
        timediffs = [(timestamps[i + 1] - timestamps[i]) for i in range(len(timestamps) - 1)]

        max_diff = max(timediffs)
        min_diff = min(timediffs)
        range_diff = max_diff - min_diff
        print(linenum, ',', max_diff)

        th = max_diff - (range_diff / 10)

        candidates = [timediff if timediff > th else 0 for timediff in timediffs]

        new_timeout = int(max(candidates)) + c
        print("New timeout: ", new_timeout)

        tlmCommunicator.updateTimer(new_timeout, 60)
