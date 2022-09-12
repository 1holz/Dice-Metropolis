import re

def multi_out(list):
    for e in list:
        out(e)

def ask(question, regex):
    pattern = re.compile(regex)
    answer = None
    while True:
        answer = inp(question)
        if pattern.match(answer):
            return answer
        else:
            out("Your answer was invalid. Please try again.")

def out(s):
    print(s)

def inp(s):
    return input(s)
