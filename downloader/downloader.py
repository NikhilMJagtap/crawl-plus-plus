import requests
from downloader.endpoint import Endpoint
import time

class DownloaderBusyException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class Downloader:
    def __init__(self , is_cordinator):
        self.busy = False
        self.is_healthy = True
        self.attempt_count = 0
        self.data = None
        self.endpoint = None
        self.is_cordinator = is_cordinator
        print(f"Downloader {id(self)} up and running!")

    def download(self, endpoint):
        assert isinstance(endpoint, Endpoint), f"endpoint should be Endpoint object, found {type(endpoint)}"
        self.endpoint = endpoint
        if self.busy:
            raise DownloaderBusyException(f"Downloader {id(self)} busy.")
        self.busy = True
        url = endpoint.get_full_url()
        # print("GET " , url)
        try:
            response = requests.get(url, data=endpoint.get_data(), headers=endpoint.get_headers(), cookies=endpoint.get_cookies())
            print("GET " , url , "    " , response.status_code)
            # print(response.text)
        except:
            # failed download
            if self.attempt_count > 4:
                self.busy = False
                raise DownloadFailedException(f"Download failed on {str(endpoint)}")
            self.attempt_count += 1
            self.handle_failed_download()

        self.attempt = 0
        self.data = response
        self.busy = False
        self.endpoint = None
        return response

    def handle_failed_download(self):
        # TODO:
        raise NotImplementedError()

    def is_busy(self):
        return self.busy

    def is_alive(self):
        return is_healthy

