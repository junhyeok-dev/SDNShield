import sys
import threading
import socket
import time
import datetime


class TLMCommunicator(threading.Thread):
    controller_ip = ""

    def __init__(self, c_ip):
        super().__init__()
        self.controller_ip = c_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 사용

    def run(self):
        self.sock.connect((self.controller_ip, 58678)) # 연결 요청

        self.sock.send("init".encode()) # 값 전송

        dat = self.sock.recv(1024).decode() # 값 읽기
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
c = 0

if len(sys.argv) != 3:
    print("Usage: TimerUpdater [CONTROLLER_IP] [C]")
    exit(1)
else:
    controller_ip = sys.argv[1]
    c = int(sys.argv[2])

tlmCommunicator = TLMCommunicator(controller_ip)
tlmCommunicator.start()

time.sleep(0.1)

while True:
    packetdata = [
        {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
        {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
        {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
        {"timestamp": "2020-9-8 15:46", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
        {"timestamp": "2020-9-8 15:46", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
        {"timestamp": "2020-9-8 15:57", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
        {"timestamp": "2020-9-8 15:57", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
        {"timestamp": "2020-9-8 15:57", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
        {"timestamp": "2020-9-8 15:58", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
        {"timestamp": "2020-9-8 15:58", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
        {"timestamp": "2020-9-8 15:58", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"}
    ]

    #시간 데이터를 UNIXTIME으로 변환하는 코드
    timestamps = [time.mktime(datetime.datetime.strptime(packet["timestamp"], "%Y-%m-%d %H:%M").timetuple()) for packet in packetdata]
    #모든 패킷 사이의 시간 간격을 리스트화
    timediffs = [(timestamps[i + 1] - timestamps[i]) / 60 for i in range(len(timestamps) - 1)]
    print(timediffs)
    #시간 간격의 평균 계산
    avg_diff = sum(timediffs) / len(timediffs)

    candidates = [timediff if timediff > avg_diff else 0 for timediff in timediffs]
    print(candidates)
    num_candidate = 0
    for candidate in candidates:
        if candidate != 0:
            num_candidate += 1 # candidates의 개수 세기
    candidates = sum(candidates)

    new_timeout = candidates / num_candidate + c # 새로운 타임아웃값 생성
    print(new_timeout)

    tlmCommunicator.updateTimer(new_timeout, 60) # 허니팟으로 새로운 타임아웃값 전송

    time.sleep(10)

