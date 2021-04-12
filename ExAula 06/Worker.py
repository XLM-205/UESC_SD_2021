import sys
import random
from socket import socket
from threading import Thread
from time import sleep


def process_request(con):
    def_buf = 1024

    # Receiving and converting data
    in_data = con.recv(def_buf)
    print(f"Received {in_data}!")
    s_in = in_data.decode("UTF-8").split(" ")
    rng = int(s_in[0])
    tgt = int(s_in[1])
    arrdt = []
    for vals in s_in[2:]:
        arrdt.append(int(vals))
    print(f"Stream have length of {rng} and target is {tgt}\nArray Data: {arrdt}")

    # Searching index
    index = 0
    try:
        index = arrdt.index(tgt)
        print(f"Index is {index}")
    except ValueError:
        index = -1
        print("Index not found on given array")

    con.sendall(bytes(str(index), "UTF-8"))

    con.close()
    print("Processing ended")
    


def beacon(port):
    print("Starting Server...")
    worker_addrss = ("127.0.0.1", port)
    hub_addrss = ("127.0.0.1", 3000)
    error_wait = 5
    waiting_hub = True
    hub_id = -1
    sock = socket()
    print(f"Worker started at: {worker_addrss[0]}:{worker_addrss[1]}\n\t> Trying to connect to the HUB")

    while waiting_hub:
        try:
            connection = sock.connect(hub_addrss)
            print("HUB found. Signalling this is a worker server and not a client..")
            sock.sendall(bytes(f"1 {worker_addrss[1]}", "UTF-8"))    # Code '0' is the HUB, '1' is a worker and '2' is the client

            # Wait for HUB confirmation..
            conf = sock.recv(8)
            if conf >= b"0":
                waiting_hub = False
                hub_id = int(conf)
                print(f"[{hub_id} @{worker_addrss[0]}:{worker_addrss[1]}] Successfully mapped!")
            else:
                print("Failed. Retrying..")

        except (KeyboardInterrupt, SystemExit, ConnectionRefusedError):
            print(f"Connection failed or denied. Retying in {error_wait}s")
            sleep(error_wait)
            #sock.close()
            print("\t> Trying to connect to the HUB")
            pass
    print(f"[{hub_id} @{worker_addrss[0]}:{worker_addrss[1]}] Waiting data from HUB...")
    while True:
        in_data = sock.recv(1024).decode("UTF-8")
        print(in_data)


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("!! Warning !! No port address supplied as argument! Using fallback port 3000")
    #    listen(3000)
    #else :
    #    listen(int(sys.argv[1]))
    beacon(3001 + random.randint(0, 998))
