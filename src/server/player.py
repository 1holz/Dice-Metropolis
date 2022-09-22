import util
from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 0
    cards = []
    landmarks = 0
    closed = False
    # flags:
    dice_modes = ["1"]
    roll_manipulation = []
    buffs = []
    double_repeats = 0
    min_money = 0
    skip_compensation = 0

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
                            self.grant(act[1:])
                        case "REVOKE":
                            self.revoke(act[1:])

    def grant(self, flags):
        for flag in flags:
            f = flag.split("-")
            match f[0].lower():
                case "dice":
                    if f[1].lower() not in self.dice_modes:
                        self.dice_modes.append(f[1].lower())
                case "roll":
                    util.out("WIP")
                case "buff":
                    util.out("WIP")
                case "double_repeats":
                    util.out("WIP")
                case "min":
                    util.out("WIP")
                case "skip":
                    util.out("WIP")
                case _:
                    util.out("Flag " + flag + " is unavailabel and cannot be granted")

    def revoke(self, flags):
        for flag in flags:
            f = flag.split("-")
            match f[0].lower():
                case "dice":
                    if f[1].lower() in self.dice_modes:
                        self.dice_modes.remove(f[1].lower())
                case "roll":
                    util.out("WIP")
                case "buff":
                    util.out("WIP")
                case "double_repeats":
                    util.out("WIP")
                case "min":
                    util.out("WIP")
                case "skip":
                    util.out("WIP")
                case _:
                    util.out("Flag " + flag + " is unavailabel and cannot be revoked")

    def gen_info(self):
        info = []
        info.append(("name", util.align("Name"), self.name, ))
        info.append(("money", util.align("Money"), self.money, ))
        info.append(("landmark_amount", util.align("Landmarks"), self.landmarks, ))
        #info.append(("flags", util.align("Flags"), self.flags, ))
        info.append(("cards", util.align("Cards"), len(self.cards)))
        for i in range(len(self.cards)):
            c = self.cards[i]
            tupel = ("card" + str(i), )
            string = "{:<30}"
            if c.renovating:
                string = string + " in renovation"
            if c.investable > 0:
                string = string + " with {:>3} invested"
            tupel = tupel + (string, c.name, c.investment, c.renovating)
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
