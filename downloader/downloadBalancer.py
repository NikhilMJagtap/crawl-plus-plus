from xmlrpc.server import SimpleXMLRPCServer
from downloader.downloader import Downloader, DownloaderBusyException
from downloader.endpoint import Endpoint
from collections import deque
from config import DownloadBalancerConfig as DBC
import threading
import time
import os

class DownloadBalancer():
    def __init__(self, host, port):
        self.is_ready = False
        self.host = host
        self.port = port
        self.rpc_server = SimpleXMLRPCServer((host, port), logRequests=True)
        self.queue = deque()
        self.queue_lock = threading.Lock()
        self.util = dict()
        for _ in range(DBC["DOWNLOADER_INIT_COUNT"]):
            d = Downloader()
            self.queue.append(d)
            self.util[id(d)] = deque(maxlen=DBC["DOWNLOADER_UTIL_COUNT"])
        self.d_count = DBC["DOWNLOADER_INIT_COUNT"]
        self.scalar_thread = threading.Thread(target=self.scalar).start()
        self.rpc_thread = threading.Thread(target=self.start_rpc_server).start()
        self.is_ready = True
        # register RPC functions here
        self.rpc_server.register_function(self.download)


    def download(self, endpoint):
        return self.balancer(endpoint)

    def balancer(self, endpoint):
        self.queue_lock.acquire()
        try:
            d = self.queue.popleft()
            print(f"Try downloading {id(d)}")
            if type(endpoint) == dict:
                endpoint = self.dict_to_endpoint(endpoint)
            threading.Thread(target=self.download_util, args=(d, endpoint)).start()
            self.queue.append(d)
        except:
            print("To be handled")
        self.queue_lock.release()


    def download_util(self, d, endpoint, wait=1):
        try:
            resposne = d.download(endpoint)
            # TODO: assert for response
            self.save_response(resposne)
        except DownloaderBusyException:
            # exponential backoff
            if wait > 32:
                print("Download timed out!")
                return
            time.sleep(wait*2)
            self.download_util(d, endpoint, wait=wait*2)


    def save_response(self, response):
        # print("TODO: save response")

        directories = response.url.split("/")[2:]

        if not os.path.exists(os.path.join("./Data" , *directories)):
            os.makedirs(os.path.join("./Data" , *directories))

        with open(os.path.join("./Data" , *directories , "main.html") , "wb") as f:
            f.write(response.text.encode())
        


    def start_rpc_server(self):
        try:
            print(f"Serving Download Balanacer on {self.host}:{self.port}...")
            self.rpc_server.serve_forever()
        except KeyboardInterrupt:
            print("\nExiting...")

    def scalar(self):
        while True:
            time.sleep(1)
            self.queue_lock.acquire()
            for d in self.queue:
                if d.is_busy():
                    self.util[id(d)].append(1)
                else:
                    self.util[id(d)].append(0)
                if sum(self.util[id(d)]) > DBC["DOWNLOADER_UTIL_THRESH"]:
                    print("Too many requests yo! Need help!")
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
            self.queue_lock.release()

    def dict_to_endpoint(self, endpoint):
        return Endpoint(
            endpoint["url"],
            params=endpoint["query_params"], 
            data=endpoint["data"], 
            headers=endpoint["headers"], 
            cookies=endpoint["cookies"]

        )
        
    def __del__(self):
        self.scalar_thread.stop()
        self.rpc_thread._stop()
