import re

def ask(question, regex):
    pattern = re.compile(regex)
    answer = None
    while True:
        out(question)
        answer = inp()
        if pattern.match(answer):
            return answer
        else:
            out("Your answer was invalid. Please try again.")

def multi_out(list):
    out("=========================")
    for e in list:
        out(e)

def out(s):
    print(s.strip())

def inp(s = ""):
    return input(s).strip()
