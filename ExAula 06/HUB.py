import sys
from socket import socket, gethostname, gethostbyname
from threading import Thread
from time import sleep


def name_resolver(hub_server_obj, target, message):
    for i in range(0, len(hub_server_obj[1])):
        if hub_server_obj[1][i] == target:
            hub_server_obj[2][i].sendall(bytes(str(message), "UTF-8"))

def mapper(hub_addrss):
    print("Starting Server...")
    sock = socket()
    sock.bind(hub_addrss)
    sock.listen()
    print(f"HUB ready @{hub_addrss[0]}:{hub_addrss[1]}\n\tMapping available servers...")
    server_info = [[], [], []]  # (IP:port, 'name', socket connection)

    while True:
        try:
            connection, source = sock.accept()
            print(f"Connection stabilised with {source[0]}:{source[1]}")
            in_data = connection.recv(128).decode("UTF-8").split(" ")
            if in_data[0] == "1":  # Worker server
                server_info[0].append(source[0])
                server_info[0].append(in_data[1])
                print(f"Worker {server_info[0][0]}:{server_info[0][1]} connected to the HUB, assigning UID")
                server_info[1].append(f"Server{len(server_info[1])}")
                server_info[2].append(connection)
                wrk_uid = len(server_info[1]) - 1
                print(f"Worker {server_info[0][0]}:{server_info[0][1]} => {wrk_uid}")
                connection.sendall(bytes(str(wrk_uid), "UTF-8"))
            elif in_data[0] == "2":  # Client
                print("Client connected to the HUB.\n\tSending available servers:")
                connection.sendall(bytes(str(len(server_info[1])), "UTF-8"))
                for i in range(0, len(server_info[1])):
                    idex = 2 * i
                    out_data = str(server_info[1][i]) + " "
                    out_data += str(server_info[0][idex]) + " "
                    out_data += str(server_info[0][idex + 1])
                    connection.sendall(bytes(out_data, "UTF-8"))
                    sleep(0.5)
                print("Done")
                #in_data = connection.recv(128).decode("UTF-8").split(" ")
                #if in_data[0] == "connect":  # <connect> <server name> <message>
                #    print(f"Incoming connection request to {in_data[1]}")
                #    msg = ""
                #    for s in in_data[2:]:
                #        msg += s + " "
                #    name_resolver(server_info, in_data[1], msg)

            else:
                print(f"Invalid identifier! Got {in_data}")

        except (KeyboardInterrupt, SystemExit):
            sock.close()
            pass


if __name__ == '__main__':
    lclhst = "127.0.0.1"
    hub_addrss = (lclhst, 3000)
    mapper(hub_addrss)
