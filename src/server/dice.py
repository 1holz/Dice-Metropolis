import random
import util

simulation = False

def set_simulation(bl):
    simulation = bl

def roll_sim():
    return int(util.ask("Please enter the rolled number", "^[-+]?\d+$"))

def roll_1():
    return random.randint(1, 6)
