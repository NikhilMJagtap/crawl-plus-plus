from xmlrpc.client import ServerProxy
from downloader.endpoint import Endpoint
from threading import Thread


url_list = ["https://www.geeksforgeeks.org/basic-understanding-of-cure-algorithm/" ,
             "https://www.geeksforgeeks.org/" , "https://www.geeksforgeeks.org/python-programming-language/",
             "https://www.geeksforgeeks.org/python-programming-examples/" , 
             "https://www.geeksforgeeks.org/machine-learning/" , "https://www.geeksforgeeks.org/c-plus-plus/"]

def main():
    proxy = ServerProxy("http://localhost:3001")
    # print(proxy.echo("Hello"))

    for url in url_list:
        print(url)
        # Thread(target=send_request , args=(proxy,url)).start()
        print(proxy.schedule_url(Endpoint(url , headers={"User-Agent":"Custom"})))

if __name__ == "__main__":
    main()