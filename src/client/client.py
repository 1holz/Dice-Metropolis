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

    def run(self):
        while True:
            if self.connection.poll() and recieve(self.connection, self.connection.recv()):
                break
            if self.queue.qsize() > 0:
                send(self.connection, self.queue.get())

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
                error(str(package["msg"]))
            else:
                util.out("An unspecified ERROR occured")
        case "CLOSE":
            util.out("Connection will be closed")
            return True
        case "PHASE":
            if "phase" not in package or not isinstance(package["phase"], int):
                error("Exact phase is missing or invalid")
                return False
            match package["phase"]:
                case 0:
                    pass
                case 1:
                    pass
                case _:
                    error("Phase " + package["phase"] + " is invalid")
        case "PRINT":
            if "msg" in package:
                util.out(str(package["msg"]))
            else:
                error("An empty message was recieved")
        case "PRINTS":
            if "lines" not in package:
                error("A message without lines was recieved")
                return False
            lines = []
            for line in package["lines"]:
                print(line)
                lines.append(line[1].format(*line[2:]))
            util.multi_out(lines)
        case _:
            error("Received package from " + player.name + " that couldn't be processed: " + package)
    return False

def send(connection, in_str):
    com = in_str.split(" ", 1)
    match com[0].upper():
        case "NAME":
            if len(com) > 1 and re.compile("^\S*[^\d\s]+\S*$").match(com[1]):
                connection.send({"type": "NAME", "name": com[1]})
            else:
                error("Some characters in the name are invalid")
        case "INFO":
            connection.send({"type": "INFO"})
        case "INFO_DETAILED":
            if len(com) > 1:
                connection.send({"type": "INFO_DETAIL", "src": com[1]})
            else:
                error("Source argument is missing for detailed info")
        case "BUY":
            if len(com) > 1:
                connection.send({"type": "BUY", "card": com[1]})
            else:
                error("Source argument is missing for buy")
        case _:
            error("Command " + in_str + " is not availabel")

def error(msg):
    util.out("ERROR: " + msg)

#def ask(question, regex):
#    pattern = re.compile(regex)
#    answer = None
#    while True:
#        util.out(question)
#        answer = util.inp()
#        if pattern.match(answer):
#            return answer
#        else:
#            out("Your answer was invalid. Please try again.")

if __name__ == '__main__':
    client = Client()
    client.start()
    client.run()
    client.finish()
