from xmlrpc.client import ServerProxy
from downloader.endpoint import Endpoint

def main():
    proxy = ServerProxy("http://localhost:3000")
    print(proxy.echo("Hello"))
    print(proxy.schedule_url(Endpoint("https://www.vgmusic.com/music/console/nintendo/nes/")))

if __name__ == "__main__":
    main()