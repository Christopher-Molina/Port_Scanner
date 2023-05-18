import socket
import threading
from queue import Queue

target = "127.0.0.1"
queue = Queue()
open_ports = []


def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except Exception as E:
        return False


def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print("Port {} is Open".format(port))
            open_ports.append(port)


def main():
    port_list = range(1, 1024)
    fill_queue(port_list)
    thread_list = []

    for t in range(500):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open Ports Are: ", open_ports)


# Call the main function
if __name__ == '__main__':
    main()
