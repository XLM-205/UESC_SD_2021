import sys
from socket import socket
from threading import Thread


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


def listen(port):
    print("Starting Server...")
    socket_bind_info = ('127.0.0.1', port)
    sock = socket()
    sock.bind(socket_bind_info)
    sock.listen()
    print(f"Server started at: {socket_bind_info[0]}:{socket_bind_info[1]}")

    while True:
        try:
            connection, source = sock.accept()
            print("Connection stabilised")
            thread = Thread(target=process_request, args=(connection,))
            thread.start()
            print("Thread deployed\n")

        except KeyboardInterrupt:
            sock.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("!! Warning !! No port address supplied as argument! Using fallback port 3000")
        listen(3000)
    else :
        listen(int(sys.argv[1]))
