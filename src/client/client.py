import json
import util
from multiprocessing import Process
from multiprocessing.connection import Client

def get_connection():
    config = {}
    with open("config.json", "r") as file:
        config = json.loads(file.read())
    addr = (config["ip"], int(config["port"]))
    return Client(addr, authkey=config["key"].encode("utf-8"))

def communicate(connection, package):
    match package["type"]:
        case "PING":
            connection.send({"type": "PONG"})
        case "PONG":
            util.out("Connection with server confirmed")
        case "ERROR":
            if "msg" in package:
                util.out("ERROR: " + package["msg"])
            else:
                util.out("An unspecified ERROR occured")
        case "CLOSE":
            util.out("Connection will be closed")
            return 1
        case _:
            util.out("Received package from " + player.name + " that couldn't be processed: " + package)
    return 0

def start(conection):
    connection.send({"type": "NAME", "name": util.ask("Please enter your name: ", "^.*$")})

def run(connection):
    while True:
        status_code = communicate(connection, connection.recv())
        match status_code:
            case 0:
                pass
            case 1:
                break

def finish(connection):
    connection.close()

if __name__ == '__main__':
    connection = get_connection()
    util.out("Client start")
    start(connection)
    run(connection)
    finish(connection)
    util.out("Client shutdown")
