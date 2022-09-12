from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 3
    cards = []
    landmarks = []
    
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

    def pong(self):
        self.connection.send({"type": "PONG"})

    def error(self, msg):
        self.connection.send({"type": "ERROR", "msg": str(msg)})

    def close(self):
        self.connection.send({"type": "CLOSE"})
        self.connection.close()

    def print(self, msg):
        self.connection.send({"type": "PRINT", "msg": str(msg)})

    def ask(self, question, regex):
        self.connection.send({"type": "ASK", "question": question, "regex": regex})
