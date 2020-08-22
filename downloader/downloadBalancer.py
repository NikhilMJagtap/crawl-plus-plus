from xmlrpc.server import SimpleXMLRPCServer
from downloader.downloader import Downloader
from collections import deque
from config import DownloadBalancerConfig as DBC
import threading

class DownloadBalancer():
    def __init__(self, host, port):
        self.is_ready = False
        self.rpc_server = SimpleXMLRPCServer((host, port), logRequests=True)
        self.queue = deque()
        self.util = dict()
        for _ in range(DBC["DOWNLOADER_INIT_COUNT"]):
            d = Downloader()
            self.queue.append(d)
            self.util[id(d)] = deque(maxlen=DBC["DOWNLOADER_UTIL_COUNT"])
        self.d_count = DBC["DOWNLOADER_INIT_COUNT"]
        self.thread = None
        self.is_ready = True

    def balancer(self, endpoint):
        try:
            d = self.queue.popleft()
            threading.Thread(target=self.download, args=(d, endpoint)).start()
            self.queue.append(d)
        except:
            print("To be handled")

    def download(self, d, endpoint):
        resposne = d.download(endpoint)
        # TODO: assert for response
        self.save_response(resposne)


    def save_response(self):
        pass


    def scalar(self):
        for d in self.queue:
            if d.is_busy():
                self.util[id(d)].append(1)
            else:
                self.util[id(d)].append(0)
            if sum(self.util[id(d)]) > DBC["DOWNLOADER_UTIL_THRESH"]:
                # load on downloader d
                if self.d_count < DBC["DOWNLOADER_MAX_COUNT"]:
                    # scale up
                    old_queue = self.util[id(d)]
                    del old_queue
                    self.util[id(d)] = deque(maxlen=DBC["DOWNLOADER_UTIL_COUNT"])
                    new_d = Downloader()
                    self.util[id(new_d)] = deque(maxlen=DBC["DOWNLOADER_UTIL_COUNT"])
                    self.queue.append(new_d)
                    self.d_count += 1
            else:
                pass

        

