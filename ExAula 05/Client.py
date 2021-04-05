from socket import socket
from threading import Thread


def process(svr_info, data, self_id):
    def_buf = 1024

    # Connection Phase
    sock = socket()
    sock.connect(svr_info)
    print(f"[{self_id}]: Connection to {svr_info[0]}:{svr_info[1]} was successful")

    # Converting data for the server to process
    out_data = str(data[0]) + " " + str(data[1])
    for v in data[2]:
        out_data += " " + str(v)
    print(f"[{self_id}]: out_data= {out_data}")

    # Sending and waiting response
    sock.sendall(bytes(out_data, "UTF-8"))
    in_data = sock.recv(def_buf)
    if in_data != b"-1":
        print(f"[{self_id}]: Target found at index {data[0] * self_id + int(in_data)} !")
    sock.close()


def request():
    lclhst = "127.0.0.1"
    svr1 = (lclhst, 3000)
    svr2 = (lclhst, 3001)
    svr1_arr = [1, 2, 0, 9]
    svr2_arr = [3, 7, 8, 5]
    int_target = 9

    # Data format: <ArrSize> <TargetValue> <Arr>
    thread1 = Thread(target=process, args=(svr1, (len(svr1_arr), int_target, svr1_arr), 0, ))
    thread2 = Thread(target=process, args=(svr2, (len(svr2_arr), int_target, svr2_arr), 1, ))

    thread1.start()
    thread2.start()


if __name__ == '__main__':
    request()
