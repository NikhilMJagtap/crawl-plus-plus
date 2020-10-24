from xmlrpc.client import ServerProxy
from downloader.endpoint import Endpoint
from threading import Thread


url_list = ["https://en.wikipedia.org/wiki/Lionel_Messi" , "https://en.wikipedia.org/wiki/Indian_Premier_League" , 
            "https://www.w3schools.com/tags/ref_urlencode.ASP" , "https://www.w3schools.com/tags/ref_canvas.asp",
            "https://www.w3schools.com/tags/tag_data.asp" , "https://www.w3schools.com/python/python_casting.asp"]

def main():
    proxy = ServerProxy("http://localhost:3000")
    # print(proxy.echo("Hello"))

    for url in url_list:
        print(url)
        # Thread(target=send_request , args=(proxy,url)).start()
        print(proxy.schedule_url(Endpoint(url , headers={"User-Agent":"Custom"})))

if __name__ == "__main__":
    main()