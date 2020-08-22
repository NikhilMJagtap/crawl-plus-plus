from xmlrpc.server import SimpleXMLRPCServer
from config import CrawlerConfig, DownloadBalancerConfig as DBC, ParserConfig
from downloader.downloadBalancer import DownloadBalancer

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = SimpleXMLRPCServer((host, port), logRequests=True, allow_none=True)
        self.crawlers = [

        ]
        self.download_balancers = [
            DownloadBalancer(DBC["BALANCERS"][0]["HOST"], DBC["BALANCERS"][0]["PORT"]),
        ]
        
        # register your functions here
        self.server.register_function(self.echo)
        self.server.register_function(self.schedule_url)
        self.server.register_function(self.add_download_balancer)

    def start_server(self):
        try:
            print(f"Serving on {self.host}:{self.port}...")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Exiting...")

    def add_download_balancer(self, db):
        assert isinstance(db, DownloadBalancer), f"db should be of type DownloadBalancer, found {type(db)}"
        self.download_balancers.append(db)

    def echo(self, text):
        if text.lower() == "ping": return "pong"
        return text

    def schedule_url(self, endpoint):
        print(self.download_balancers[0].download(endpoint))

    