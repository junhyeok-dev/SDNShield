# -*- coding: utf-8 -*-

import sys
import threading
import socket
import time


class TUCommunicator(threading.Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 사용
        self.sock.bind(("172.17.0.2", 58678)) # 포트 오픈

    def run(self):
        self.sock.listen() # 포트 연결 대기

        (client, addr) = self.sock.accept() #연결 성립
        print(addr, " has connected.")

        while True:
            response = ""

            rdat = client.recv(1024).decode() # 클라이언트로부터 값을 읽어오기

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

            client.send(response.encode()) # 값 전송

            time.sleep(1)


# Global variables
min_timeout = 0
hr_timeout = 0


def setTimeout(vals):
    try:
        global min_timeout, hr_timeout
        min_timeout = int(vals[0])
        hr_timeout = int(vals[1])
        print("New timeout: ", min_timeout, "/", hr_timeout)
        return 0
    except IndexError:
        print("Error: invalid timeout value")
        return 1


if len(sys.argv) != 3:
    print("Usage: ThreatLevelManager [MIN_TIMEOUT] [HOUR_TIMEOUT]")
    exit(1)
else:
    min_timeout = int(sys.argv[1])
    hr_timeout = int(sys.argv[2])

tuCommunicator = TUCommunicator()
tuCommunicator.start()

NO_THREAT = 0
LOW_THREAT = 1
AFTER_LOW_THREAT = 2
HIGH_THREAT = 3

state = NO_THREAT

signal = False
timer_start = 0

while True:
    if signal:
        if state == NO_THREAT:
            state = LOW_THREAT
        elif state == LOW_THREAT:
            state = HIGH_THREAT
        else:
            state = HIGH_THREAT
        timer_start = time.time()

    if time.time() - timer_start > min_timeout * 60:
        if state == LOW_THREAT:
            state = AFTER_LOW_THREAT
        elif state == HIGH_THREAT:
            state = LOW_THREAT

    if time.time() - timer_start > hr_timeout * 60:
        state = NO_THREAT


