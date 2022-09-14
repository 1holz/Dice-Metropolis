import re

def infos_out(list):
    new_list = []
    out("=========================")
    for t in list:
        out(t[1].format(t[2:]))

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
