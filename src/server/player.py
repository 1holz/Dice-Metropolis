import util
from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 0
    cards = []
    landmarks = 0
    flags = []

    def __init__(self, id, money, connection):
        self.name = "Dummy" + str(id)
        self.money = money
        self.connection = connection
    
    def receive_card(self, card, amount = 1):
        if card.type == "Landmark":
            self.landmarks += 1
        for i in range(amount):
            self.cards.append(card.get_copy())
    
    def gen_infos(self):
        info = []
        info.append(("name", util.align("Name"), self.name, ))
        info.append(("money", util.align("Money"), self.money, ))
        info.append(("landmark_amount", util.align("Landmarks"), self.landmarks, ))
        info.append(("flags", util.align("Flags"), self.flags, ))
        info.append(("cards", util.align("Cards"), len(self.cards)))
        for i in range(len(cards)):
            c = cards[i]
            tupel = ("card" + str(i), )
            string = "{:<30}"
            if c.renovating:
                string = string + " in renovation"
            if c.investable > 0:
                string = string + " with {:>3} invested"
            tupel = tupel + (string, c.investment, c.renovating)
            info.append(tupel)
        return info
    
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
