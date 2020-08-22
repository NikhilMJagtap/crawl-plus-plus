from xmlrpc.client import ServerProxy

def main():
    proxy = ServerProxy("http://localhost:3000")
    print(proxy.echo("Hello"))
    

if __name__ == "__main__":
    main()