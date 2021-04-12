from socket import socket
from threading import Thread


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


def request():
    lclhst = "127.0.0.1"
    svr_def_port = 3000
    int_target = 9
    arr_subdivisions = 2
    arr_input = [1, 2, 0, 9, 3, 7, 8, 5]
    arr_index_step = int(len(arr_input) / arr_subdivisions)
    arr_stepper = 0
    servers = [(), []]
    addrss = []

    for i in range(0, arr_subdivisions):
        addrss.append((lclhst, svr_def_port + i))
        servers[1].append(arr_input[arr_stepper:(arr_stepper + arr_index_step)])
        arr_stepper += arr_index_step

    servers[0] = tuple(addrss)

    threads = []
    for i in range(0, arr_subdivisions):
        # Data format: <ArrSize> <TargetValue> <Arr>
        threads.append(Thread(target=process, args=(servers[0][i], (len(servers[1][i]), int_target, servers[1][i]), i,)))
        print(f"[{i}]: Trying to send to {servers[0][i][0]}:{servers[0][i][1]} > {servers[1][i]}")
        threads[i].start()



if __name__ == '__main__':
    request()
