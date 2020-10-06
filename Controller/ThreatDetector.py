import threading
import time
import requests


class DetectorThread(threading.Thread):
    def __init__(self, thsrc, thtime):
        super().__init__()
        self.thsrc = thsrc
        self.thtime = thtime

    def run(self):
        while True:
            packetdata = [
                {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.1", "dst": "10.0.0.2"},
                {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.2", "dst": "10.0.0.1"},
                {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.3", "dst": "10.0.0.1"},
                {"timestamp": "2020-9-8 15:45", "protocol": "tcp", "src": "10.0.0.6", "dst": "10.0.0.1"},
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

            atts = detectIpEntropyOutlier(packetdata, self.thsrc)

            for att in atts:
                generateFlowRule(att, "192.168.0.2")

            time.sleep(self.thtime)

def detectIpEntropyOutlier(packets, thsrc): #패킷데이터, 임계치, 단위시간 입력
    dstIps = [] #목적지 주소를 저장하는 배열
    dstSrcMap = {} #목적지 - 목적지로 패킷을 보낸 출발지를 저장하는 딕셔너리
    attackers = []

    [dstIps.append(packet["dst"]) if packet["dst"] not in dstIps else 0 for packet in packets] #dspIps(목적지 주소 리스트) 생성 루프
    for dstIp in dstIps:
        dstSrcMap[dstIp] = [] #dstSrcMap 딕셔너리 초기화

    #dstSrcMap 생성 루프
    [dstSrcMap[packet["dst"]].append(packet["src"]) if packet["src"] not in dstSrcMap[packet["dst"]] else 0 for packet in packets]

    print(dstSrcMap)
    for key, val in dstSrcMap.items():
        if len(val) > thsrc:
            attackers.append(key)

    return attackers


def generateFlowRule(att, honeypot_url):
    rule = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": True,
        "deviceId": "of:0000000000000001",
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": "CONTROLLER"
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x88cc"
                }
            ]
        }
    }
    resp = requests.post("http://localhost:8181/onos/v1/flows/", data=rule)


dtThread = DetectorThread(2, 3)
dtThread.start()
