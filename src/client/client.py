import json
import re
import util
from multiprocessing import Process, Queue
from multiprocessing.connection import Client as Connection
from threading import Thread

def get_connection():
    config = {}
    with open("config.json", "r") as file:
        config = json.loads(file.read())
    addr = (config["ip"], int(config["port"]))
    return Connection(addr, authkey=config["key"].encode("utf-8"))

def console(queue):
    while True:
        queue.put(util.inp())

class Client:
    connection = None
    queue = Queue()
    thread = Thread(target = console, args = (queue, ), daemon = True)

    def __init__(self):
        util.out("Client start")
        self.connection = get_connection()
        self.thread.start()

    def start(self):
        pass
        #util.out("Please enter your name: ")
        #pattern = re.compile("^.*$")
        #answer = None
        #while True:
        #    if queue.qsize() <= 0:
        #        continue
        #    answer = queue.get()
        #    if pattern.match(answer):
        #        self.send(send. connection, "NAME:" + answer)
        #        break
        #    else:
        #        util.out("Your name is invalid. Please try again.")

    def run(self):
        while True:
            status_code = recieve(self.connection, self.connection.recv())
            match status_code:
                case 0:
                    pass
                case 1:
                    break
            if self.queue.qsize() > 0:
                send(self.queue.get())

    def finish(self):
        self.connection.close()
        util.out("Client shutdown")

def recieve(connection, package):
    match package["type"]:
        case "PING":
            connection.send({"type": "PONG"})
        case "PONG":
            util.out("Connection with server confirmed")
        case "ERROR":
            if "msg" in package:
                util.out("ERROR: " + str(package["msg"]))
            else:
                util.out("An unspecified ERROR occured")
        case "CLOSE":
            util.out("Connection will be closed")
            return 1
        case "PRINT":
            if "msg" in package:
                util.out(str(package["msg"]))
            else:
                util.out("ERROR: An empty message was recieved")
        case "ASK":
            pass # WIP
        case _:
            util.out("Received package from " + player.name + " that couldn't be processed: " + package)
    return 0

def send(connection, in_str):
    pass

def ask(question, regex):
    pattern = re.compile(regex)
    answer = None
    while True:
        util.out(question)
        answer = util.inp()
        if pattern.match(answer):
            return answer
        else:
            out("Your answer was invalid. Please try again.")

if __name__ == '__main__':
    client = Client()
    client.start()
    client.run()
    client.finish()
