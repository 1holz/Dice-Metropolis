#!/usr/bin/env python3

import random
import util

simulation = False

def set_simulation(bl):
    simulation = bl

def roll(mode, player):
    if simulation:
        return int(util.ask("Please enter the rolled number", "^[-+]?\d+$"))
    match mode:
        case "1":
            return [random.randint(1, 6)]
        case "2":
            return [random.randint(1, 6), random.randint(1, 6)]
        case _:
            return [0]
