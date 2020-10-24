from engine.server import Server
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p" , "--port")

args = parser.parse_args()

server = Server("0.0.0.0", int(args.port))
server.start_server()