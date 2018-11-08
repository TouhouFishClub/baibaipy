import socket
import threading
import random
import time
import gc
from urllib.parse import urlparse
from urllib import parse
import xiaobing as xb
# import asyncore

# import time

HOST, PORT = "0.0.0.0", 10088


class Singleton(object):
    __instance = None
    __LinkedNum = 0
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get():
        Singleton.__lock.acquire()
        num = Singleton.__LinkedNum
        Singleton.__lock.release()
        return num

    @staticmethod
    def increase():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum += 1
        Singleton.__lock.release()

    @staticmethod
    def decrease():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum -= 1
        Singleton.__lock.release()

    def __new__(cls, *args, **kwd):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls, *args, **kwd)
            # Singleton.__lock = threading.Lock
        return Singleton.__instance


def rand_str(length):
    string = "abcdefghijklmnopqrstuvwxyz123456789"
    t = int(round(time.time() * 1000))
    ret = ""
    for i in range(0, length):
        num = random.randrange(0, len(string) - 1)
        ret += string[num]
    return ret + str(t)


def customer(client_connection):
    Singleton().increase()
    rate = 0

    http_response = '{"a":1}'
    try:
        request = client_connection.recv(1024).decode()
        method = request.split(' ')[0]
        fullpath = str(request.split(' ')[1])

        query = parse.parse_qs(urlparse(fullpath).query)
        path = urlparse(fullpath).path
        print(query)
        type = query['type'][0]
        print(type)
        imgurl = query['url'][0]
        print(imgurl)
        print(path)
        print(5555555)
        param = ""
        imgUrl = 'https://gchat.qpic.cn/gchatpic_new/771210053/549823679-2860105086-7161E023087FC6BBAE3484BE4189D69B/0'
        poemResult = xb.poem(imgurl)
        http_response = poemResult
        print(poemResult)

        print(1111111)
        print(param)
        http_head = 'HTTP/1.x 200 OK\r\nContent-Type: application/json\r\n\r\n'

        http_res_all = http_head + http_response + ''
        print(http_res_all)
        print(2222222)
        client_connection.sendall(http_res_all.encode())
    except:
        pass
    finally:
        client_connection.close()
        Singleton().decrease()
        gc.collect()


def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(5)
    while True:
        client_connection, client_address = listen_socket.accept()
        # print(Singleton().get())
        if Singleton().get() > 30:
            client_connection.close()
        else:
            threading.Thread(target=customer, args=(client_connection,)).start()


if __name__ == '__main__':
    print("start")
    main()
