import re
from queue import Queue
from threading import Thread

in_queue = Queue()

def setup_io():
    thread = Thread(target = console, daemon = True)

def console():
    while True:
        in_queue.put(inp())

def ask(question, regex):
    pattern = re.compile(regex)
    answer = None
    while True:
        out(question)
        answer = inp()
        if pattern.match(answer):
            return (question, answer
        else:
            out("Your answer was invalid. Please try again.")

def inp():
    return input()

def multi_out(list):
    for e in list:
        out(e)

def out(s):
    print(s)
