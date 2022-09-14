import util
from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 0
    cards = []
    landmarks = []
    flags = []

    def __init__(self, id, money, connection):
        self.name = "Dummy" + str(id)
        self.money = money
        self.connection = connection
    
    def receive_card(self, card, amount = 1):
        if card.type == "Landmark":
            for i in range(amount):
                self.landmarks.append(card.get_copy())
        else:
            for i in range(amount):
                self.cards.append(card.get_copy())
    
    def gen_strings(self):
        strings = []
        strings.append("Name:               " + self.name)
        strings.append("Money:              " + str(self.money))
        strings.append("Landmarks:")
        for c in self.landmarks:
            strings.append(c.gen_string())
        strings.append("Cards:")
        for c in self.cards:
            strings.append(c.gen_string())
        return strings
    
    def send(self, package):
        try:
            self.connection.send(package)
        except:
            util.out("Could not send " + str(package) + " to " + self.name)

    def pong(self):
        self.send({"type": "PONG"})

    def error(self, msg):
        self.send({"type": "ERROR", "msg": str(msg)})

    def close(self):
        self.send({"type": "CLOSE"})
        self.connection.close()

    def print(self, msg):
        self.send({"type": "PRINT", "msg": str(msg)})

    #def ask(self, question, regex):
    #    self.send({"type": "ASK", "question": question, "regex": regex})
