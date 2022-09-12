from card import Card

class Player:
    connection = None
    name = "Dummy0"
    money = 3
    cards = []
    
    def __init__(self, id, money, connection):
        self.name = "Dummy" + str(id)
        self.money = money
        self.connection = connection
    
    def receive_card(self, card, amount = 1):
        for i in range(amount):
            self.cards.append(card.get_copy())
    
    def gen_strings(self):
        strings = []
        strings.append("Name:               " + self.name)
        strings.append("Money:              " + str(self.money))
        strings.append("Cards:")
        for c in self.cards:
            strings.append(c.gen_string())
        return strings
