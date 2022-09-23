import util
from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 0
    cards = []
    landmarks = 0
    closed = False
    dice_mode = "1"
    # flags:
    dice_modes = [dice_mode]
    roll_mods = []
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
            if card.activation == "passive":
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
                    if len(f) > 1 and f[1].lower() not in self.dice_modes:
                        self.dice_modes.append(f[1].lower())
                case "roll":
                    util.out("WIP")
                case "buff":
                    util.out("WIP")
                case "repeats":
                    if len(f) > 1 and f[1].isdigit():
                        self.double_repeats += int(f[1])
                    else:
                        util.out("Cannot grant invalid repeats flag " + flag)
                case "min":
                    if len(f) > 1 and f[1].isdigit():
                        self.min_money += int(f[1])
                    else:
                        util.out("Cannot grant invalid min money flag " + flag)
                case "skip":
                    if len(f) > 1 and f[1].isdigit():
                        self.skip_compensation += int(f[1])
                    else:
                        util.out("Cannot grant invalid skip compensation flag " + flag)
                case _:
                    util.out("Flag " + flag + " is unavailable and cannot be granted")

    def revoke(self, flags):
        for flag in flags:
            f = flag.split("-")
            match f[0].lower():
                case "dice":
                    if len(f) > 1 and f[1].lower() in self.dice_modes:
                        self.dice_modes.remove(f[1].lower())
                case "roll":
                    util.out("WIP")
                case "buff":
                    util.out("WIP")
                case "repeats":
                    if len(f) > 1 and f[1].isdigit():
                        self.double_repeats -= int(f[1])
                    else:
                        util.out("Cannot revoke invalid repeats flag " + flag)
                case "min":
                    if len(f) > 1 and f[1].isdigit():
                        self.min_money -= int(f[1])
                    else:
                        util.out("Cannot revoke invalid min money flag " + flag)
                case "skip":
                    if len(f) > 1 and f[1].isdigit():
                        self.skip_compensation -= int(f[1])
                    else:
                        util.out("Cannot revoke invalid skip compensation flag " + flag)
                case _:
                    util.out("Flag " + flag + " is unavailable and cannot be revoked")

    def gen_info(self):
        info = []
        info.append(("name", util.align("Name"), self.name, ))
        info.append(("money", util.align("Money"), self.money, ))
        info.append(("landmark_amount", util.align("Landmarks"), self.landmarks, ))
        info.append(("dice_mode", util.align("Last dice mode"), self.dice_mode, ))
        info.append(("dice_modes", util.align("Owned dice modes"), self.dice_modes, ))
        info.append(("roll_mods", util.align("Owned roll mods"), self.roll_mods, ))
        info.append(("buffs", util.align("Owned buffs"), self.buffs, ))
        info.append(("double_repeats", util.align("Double Repeats"), self.double_repeats, ))
        info.append(("min_money", util.align("Minimum money"), self.min_money, ))
        info.append(("skip_compensation", util.align("Skip Compensation"), self.skip_compensation, ))
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
