def detectIpEntropyOutlier(packets, thsrc, thtime): #패킷데이터, 임계치, 단위시간 입력
    dstIps = [] #목적지 주소를 저장하는 배열
    dstSrcMap = {} #목적지 - 목적지로 패킷을 보낸 출발지를 저장하는 딕셔너리
    [dstIps.append(packet["dst"]) if packet["dst"] not in dstIps else 0 for packet in packets] #dspIps(목적지 주소 리스트) 생성 루프
    for dstIp in dstIps:
        dstSrcMap[dstIp] = [] #dstSrcMap 딕셔너리 초기화

    #dstSrcMap 생성 루프
    [dstSrcMap[packet["dst"]].append(packet["src"]) if packet["src"] not in dstSrcMap[packet["dst"]] else 0 for packet in packets]

    result = False #결과를 False로 초기화

    print(dstSrcMap)
    for key, val in dstSrcMap.items():
        if len(val) > thsrc:
            result = True

    return result


# 샘플 데이터
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

print(detectIpEntropyOutlier(packetdata, 10000, 1))
