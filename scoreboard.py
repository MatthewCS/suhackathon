from contextlib import closing
import socket
import random
import threading


class Scoreboard(object):

    ip_list = []
    ports = {"FTP": 21,
             "SSH": 22,
             "SMTP": 25,
             "HTTP": 80,
             "Remote Desktop": 445}
    update_interval = -1


    def __init__(self, update_interval):

        self.get_ips("./ips.txt")
        self.update_interval = update_interval


    def get_ips(self, filepath):

        with open(filepath, "r") as f:

            self.ip_list = f.readlines()

        for i in range(0, len(self.ip_list)):

            self.ip_list[i] = self.ip_list[i].strip()


    def port_is_open(self, ip, port):

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:

            s.settimeout(3)

            if s.connect_ex((ip, port)) == 0:

                return True

            return False


    def check_ports(self):

        port_check = {}

        for ip in self.ip_list:

            port_check[ip] = {}

            for port in self.ports:

                port_check[ip][port] = self.port_is_open(ip, self.ports[port])


        return port_check


    def update(self, *args, **kwargs):

        offset = args[0]

        def update_wrapper(func):

            def run_func():

                delay = self.update_interval + random.randint(-1 * offset, offset)
                threading.Timer(delay, run_func).start()

                func()

            run_func()

            return func

        return update_wrapper
