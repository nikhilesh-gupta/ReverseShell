# # import argparse

# # parser = argparse.ArgumentParser()

# # parser.add_argument("-l", "--list", dest="LFiles", default=76524, help="List the file name")
# # parser.add_argument("-p", "--par", dest="Parxict", default="67582", help="Par the file name")
# # #parser.add_argument("-d", "--duin", dest="Idk", help="IDK the file name")

# # args = parser.parse_args()
# # args.LFiles = int(args.LFiles)

# # print(
# #         args.LFiles,
# #         args.Parxict
# #         #args.Idk
# #         )
# # print(
# #     type(args.LFiles), 
# #     type(args.Parxict) 
# # )

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

# print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.FAIL + "Fail: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.BOLD + "Bold: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.HEADER + "Header: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.UNDERLINE + "Underline: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.OKGREEN + "OkGreen: No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.OKBLUE + ": No active frommets remain. Continue?" + bcolors.ENDC)
# print(bcolors.OKCYAN + "OkCyan: No active frommets remain. Continue?" + bcolors.ENDC)


import socket
import tqdm
import os
import argparse

def client():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    host = args.Addr
    # the port, let's use 5001
    port = 5001
    # the name of file we want to send, make sure it exists
    filename = input("Enter the file name: ")
    # get the file size
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()

def server():
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()

parser = argparse.ArgumentParser()
parser.add_argument("-c", dest="Client", action='store_true', help="Client Code")
parser.add_argument("-s", dest="Server", action='store_true', help="Server Code")
parser.add_argument("-l", dest="Addr", help="Ip Addr")
args = parser.parse_args()

# if args.Client:
#     print("True")
# if not args.Client:
#     print("False")

if args.Client and args.Addr:
    client()
elif args.Server:
    server()
else:
    print("[!] Something went wrong...")



# while True:
#     cmd = input(f"command $> ")
#     if not cmd.strip():
#         pass
#     if cmd.lower() == "exit":
#         break