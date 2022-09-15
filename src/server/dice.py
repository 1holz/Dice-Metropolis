import random

simulation = False

def set_simulation(bl):
    simulation = bl

def roll_1():
    return random.randint(1, 6)
