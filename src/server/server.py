import card
import dice
import json
import os
import re
import util
from player import Player
from multiprocessing.connection import Listener

config = {}
players = []
landmark_amount = 0
cards = []
phase = 0

def broadcast(msg):
    util.out(msg)
    for p in players:
        p.print(msg)

def close(player):
    try:
        player.close()
    except:
        util.out(player.name + " has closed connection on its own.")
    broadcast("Connection with " + player.name + " will be closed")

def load_config():
    global config
    with open("config.json", "r") as file:
        config = json.loads(file.read())

def reload_cards():
    global cards
    global landmark_amount
    cards = []
    names = []
    for (root, dirs, files) in os.walk('./cards/'):
        for f in files:
            if f[-5:].casefold() == ".json".casefold():
                path = os.path.join(root, f)
                new_card = card.from_file(path)
                if new_card.name == "":
                    util.out("The file " + path + " didn't contain a valid name and will be skiped")
                    continue
                if new_card.name in names:
                    util.out("The card " + new_card.name + " was attempted to be loaded twice. The second attempt will be skiped")
                    continue
                cards.append(new_card)
                if new_card.type == "Landmark":
                    landmark_amount += 1
                names.append(new_card.name)

def gen_info():
    info = []
    info.append(("players", util.align("Players"), len(players), ))
    for i in range(len(players)):
        p = players[i]
        info.append(("player" + str(i), "{:<30} Landmarks: {:>3} Money: {:>3}", p.name,
            p.landmarks, p.money, ))
    info.append(("landmark_amount", util.align("Landmark amount"), landmark_amount, ))
    info.append(("cards", util.align("Cards"), len(cards)))
    for i in range(len(cards)):
        c = cards[i]
        info.append(("card" + str(i), "{:<30} Index: {:>3} Availabel: {:>3}", c.name, i, c.availabel, ))
    return info

def transactions(activation_no):
    broadcast(players[0].name + " rolled a " + str(activation_no))
    activate(activation_no, lambda type : type != "Restaurants")
    activate(activation_no, lambda type : type == "Restaurants" or type == "Major Establishment")
    activate(activation_no, lambda type : type != "Major Establishment")

def activate(activation_no, type_l):
    active_player = players[0]
    for i in range(len(players)):
        owner = players[i]
        for c in players[i].cards:
            if (type_l(c.type) or activation_no not in c.activation_no or
                c.activation == "passiv" or c.activation == "self" and i > 0 or
                c.activation == "others" and i == 0):
                continue
            if c.renovating:
                c.renovating = False
                broadcast(owner.name + " finished renovating " + c.name)
                continue
            for action in c.actions:
                act = action.split()
                match act[0].upper():
                    case "BANK":
                        if len(act) > 0:
                            if act[1] == "inv".lower():
                                owner.money += c.investment
                                broadcast(owner.name + " recieved " + str(c.investment) + " coin(s) with the " + c.name)
                            else:
                                owner.money += int(act[1])
                                broadcast(owner.name + " recieved " + act[1] + " coin(s) with the " + c.name)
                        else:
                            invalid_action(c.name, action)
                    case "STEAL":
                        if len(act) > 0:
                            taken = 0
                            if act[1] == "inv".lower():
                                taken = min(c.investment, active_player.money)
                            elif act[1] == "all".lower():
                                taken = active_player.money
                            else:
                                taken = min(int(act[1]), active_player.money)
                            active_player.money -= taken
                            owner.money += taken
                            broadcast(owner.name + " took " + str(taken) + " coin(s) with the " + c.name)
                        else:
                            invalid_action(c.name, action)
                    case "COMBO":
                        if len(act) > 1:
                            amount = 0
                            for card in owner.cards:
                                if card.icon == act[1]:
                                    amount += 1
                            owner.money += amount * int(act[2])
                            broadcast(owner.name + " recieved " + str(amount * int(act[2])) + " coin(s) with the " + c.name)
                    case "RENOVATE:":
                        c.renovating = True
                        broadcast(owner.name + " started renovating " + c.name)
                    case "GRANT":
                        owner.flags = owner.flags + act[1:]
                        broadcast(owner.name + " got flag(s): " + ", ".join(act[1:]) + " with the " + c.name)
                    case "REVOKE":
                        f = []
                        for flag in act[1:]:
                            if flag in owner.flags:
                                owner.flags.remove(flag)
                                f.append(flag)
                        broadcast(owner.name + " lost flag(s): " + ", ".join(f) + " with the " + c.name)
                    case _:
                        invalid_action(c.name, action)

def invalid_action(name, action):
    util.out(name + " contains invalid action " + action)

def communicate():
    while True:
        for p in players[:]:
            if p.closed:
                continue
            try:
                if p.connection.poll() and handle_package(p.connection.recv(), p):
                    break
            except:
                close(p)
                broadcast(p.name + " has disconnected")
        if players[0].closed:
            break
    return players[0].closed

def handle_package(package, player):
    match package["type"].upper():
        case "PING":
            player.pong()
        case "PONG":
            util.out("Connection with player " + player.name + " confirmed")
        case "ERROR":
            if "msg" in package:
                util.out("ERROR from " + player.name + ": " + str(package["msg"]))
            else:
                util.out("An unspecified ERROR occured with " + player.name)
        case "CLOSE":
            close(player)
        case "NAME":
            if "name" not in package:
                player.error("The name is not present")
                return False
            new_name = str(package["name"])
            if new_name == "BANK":
                player.error("The name is equal to BANK")
                return False
            for p in players:
                if new_name == p.name:
                    player.error("The name " + new_name + " is already taken")
                    return False
            if not re.compile("^\S*[^\d\s]+\S*$").match(new_name):
                player.error("The name " + new_name + " contains illegal charcters")
                return False
            broadcast(player.name + " has changed the name to " + str(package["name"]))
            player.name = str(package["name"])
        case "INFO":
            player.prints(gen_info())
        case "INFO_DETAIL":
            if "src" not in package:
                player.error("Source is missing for detailed info")
                return False
            src = package["src"]
            info = []
            if src == "BANK":
                info = gen_info()
            else:
                e = from_list(players, src)
                if e is not None:
                    info = e.gen_info()
            if info:
                player.prints(info)
            else:
                player.error("The source " + src + " is unavailabel")
        case "BUY":
            pass
        case _:
            util.out("Received package from " + player.name + " that couldn't be processed: " + package)
    return False

def start():
    load_config()
    dice.set_simulation(bool(config["simulation"]))
    addr = ("127.0.0.1", int(config["port"]))
    listener = Listener(addr, authkey=config["key"].encode("utf-8"))
    init_money = int(config["init_money"])
    for i in range(int(config["player_amount"])):
        players.insert(0, Player(i + 1, init_money, listener.accept()))
    listener.close()
    card.player_amount = len(players)
    reload_cards()
    for c in cards:
        for p in players:
            for i in range(c.start):
                p.receive_card(c)

def run():
    global landmark_amount
    global phase
    while True:
        if players[0].closed:
            players.remove(players[0])
        if len(players) == 0:
            break
        #                                   dice mode?
        #if communicate():
        #    continue
        dice_roll = dice.roll_1()
        #                                   add 2?
        #                                   reroll?
        #if communicate():
        #    continue
        transactions(dice_roll)
        #                                   buy
        if communicate():
            continue
        #                                   invest
        if communicate():
            continue
        if landmark_amount <= players[0].landmarks:
            broadcast(players[0].name + " has won the game")
            close(players[0])
        else:
            if False: #                     check double
                pass
            else:
                players.append(players.pop(0))

def from_list(list, element):
    if isinstance(element, int):
        return list[element % len(list)]
    else:
        element = str(element)
        if element.isdigit():
            return list[int(element) % len(list)]
        else:
            for e in list:
                if e.name == element:
                    return e
                return None

def finish():
    for p in players:
        p.connection.close()

if __name__ == '__main__':
    util.out("Server start")
    start()
    run()
    finish()
    util.out("Server shutdown")
