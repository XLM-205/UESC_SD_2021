from socket import socket
from threading import Thread
from time import sleep

def get_socket_to_svr(svr_list, target):
    for i in range(len(svr_list[0])):
        svr_name = svr_list[0][i]
        svr_addrss = svr_list[1][i]
        if svr_name == target:
            sock = socket()
            sock.connect(svr_addrss)
            print(f"Connected to {svr_name} @{svr_addrss[0]}:{svr_addrss[1]}")
            return sock
    print(f"Server {target} was not found in the availability list!")


def process(svr_info, data, self_id):
    def_buf = 1024

    # Connection Phase
    try:
        sock = socket()
        sock.connect(svr_info)
        print(f"[{self_id}]: Connection to {svr_info[0]}:{svr_info[1]} was successful")

        # Converting data for the server to process
        out_data = str(data[0]) + " " + str(data[1])
        for v in data[2]:
            out_data += " " + str(v)

        # Sending and waiting response
        sock.sendall(bytes(out_data, "UTF-8"))
        in_data = sock.recv(def_buf)
        if in_data != b"-1":
            print(f"[{self_id} @{svr_info[0]}:{svr_info[1]}]: Target found at index {data[0] * self_id + int(in_data)} !")
        else:
            print(f"[{self_id} @{svr_info[0]}:{svr_info[1]}]: Target not found")
        sock.close()
    except ConnectionRefusedError:
        print(f"[{self_id} @{svr_info[0]}:{svr_info[1]}]: Is unavailable")


def con_hub():
    av_svr = [[], []]
    hub_addrss = ("127.0.0.1", 3000)
    try:
        sock = socket()
        sock.connect(hub_addrss)
        print(f"Main HUB connected. Pooling worker servers")
        sock.sendall(b"2")
        in_data = sock.recv(8).decode("UTF-8")
        print(f"There are {in_data} servers available:")
        for i in range(0, int(in_data)):
            in_data = sock.recv(1024).decode("UTF-8").split(" ")
            sleep(0.5)
            print(f"\t* [{in_data[0]}] @{in_data[1]}:{in_data[2]}")
            temp = (in_data[1], int(in_data[2]))
            av_svr[0].append(in_data[0])
            av_svr[1].append(temp)
        sock.close()
        sock = None
        svr = ""
        while sock is None:
            print("Connect to which server? ")
            svr = str(input())
            sock = get_socket_to_svr(av_svr, svr)
        while True:
            print(f"> Message to send to {svr}:")
            msg = str(input())
            sock.sendall(bytes(msg, "UTF-8"))

    except ConnectionRefusedError:
        print("HUB is unavailable")

if __name__ == '__main__':
    con_hub()
