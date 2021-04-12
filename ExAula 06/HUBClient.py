from socket import socket
from threading import Thread
from time import sleep


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
        print("Connect to which server? ")
        svr = "connect " + str(input())
        print(svr)
        sock.sendall(bytes(svr, "UTF-8"))
    except ConnectionRefusedError:
        print("HUB is unavailable")

if __name__ == '__main__':
    con_hub()
