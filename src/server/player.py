import util
from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 0
    cards = []
    landmarks = 0
    flags = []
    closed = False

    def __init__(self, id, money, connection):
        self.name = "Dummy" + str(id)
        self.money = money
        self.connection = connection
    
    def receive_card(self, card, amount = 1):
        if card.type == "Landmark":
            self.landmarks += 1
        for i in range(amount):
            self.cards.append(card.get_copy())
            if card.activation == "passiv":
                for action in card.actions:
                    act = action.split()
                    match act[0]:
                        case "GRANT":
                            self.flags = self.flags + act[1:]
                        case "REVOKE":
                            for flag in act[1:]:
                                if flag in self.flags:
                                    self.flags.remove(flag)

    def gen_info(self):
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
        if self.closed:
            return
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
        self.closed = True
        self.connection.close()

    def phase(self, phase):
        self.send({"type": "PHASE", "phase": phase})

    def print(self, msg):
        self.send({"type": "PRINT", "msg": str(msg)})

    def prints(self, lines):
        self.send({"type": "PRINTS", "lines": lines})

    #def ask(self, question, regex):
    #    self.send({"type": "ASK", "question": question, "regex": regex})
