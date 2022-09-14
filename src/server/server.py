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

def broadcast(msg):
    util.out(msg)
    for p in players:
        p.print(msg)

def close(player):
    broadcast("Connection with " + player.name + " will be closed")
    try:
        player.close()
    except:
        util.out(player.name + " has closed connection on its own.")
    players.remove(player)

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
    info.append(("player_amount", "Player amount:      {}", len(players), ))
    info.append(("Landmark amount:    ", landmark_amount, ))
    info.append(("Cards:", ))
    for c in self.cards:
        info.append(c.gen_string())
    return info

def transactions(activation_no):
    broadcast(players[0].name + " rolled a " + str(activation_no))
    active_player = players[0]
    for p in players:
        for c in p.cards:
            if c.type == "Restaurants":
                pass # check activation & execute
    for p in players:
        for c in p.cards:
            if c.type != "Restaurants" and c.type != "Major Establishment":
                pass # check activation & execute
    for p in players:
        for c in p.cards:
            if c.type == "Major Establishment":
                pass # check activation & execute

def communicate(package, player):
    match package["type"]:
        case "PING":
            player.pong()
        case "PONG":
            util.out("Connection with player " + player.name + " confirmed")
        case "NAME":
            pattern = re.compile(regex)
            if "name" not in package:
                player.error("The name is not present.")
            new_name = str(package["name"])
            if new_name == "BANK":
                player.error("The name is equal to BANK.")
                return 0
                return 0
            for p in players:
                if new_name == p.name:
                    player.error("The name " + new_name + " is already taken.")
                    return 0
            if not re.compile("^.*$").match(new_name):
                player.error("The name " + new_name + " contains illegal charcters")
                return 0
            player.name = str(package["name"])
        case "ERROR":
            if "msg" in package:
                util.out("ERROR from " + player.name + ": " + str(package["msg"]))
            else:
                util.out("An unspecified ERROR occured with " + player.name)
        case "CLOSE":
            close(player)
        case _:
            util.out("Received package from " + player.name + " that couldn't be processed: " + package)
    return 0

def start():
    load_config()
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
    while True:
        for p in players[:]:
            status_code = 0
            try:
                if p.connection.poll():
                    status_code = communicate(p.connection.recv(), p)
            except:
                broadcast(p.name + " has disconnected.")
                close(p)
                status_code = 0
            match status_code:
                case 0:
                    pass
                case 1:
                    break
        if len(players) == 0:
            break
        #                                   dice mode?
        dice_roll = dice.roll_1()
        #                                   add 2?
        transactions(dice_roll)
        #                                   buy
        #                                   invest
        if landmark_amount == len(players[0].landmarks):
            broadcast(players[0].name + " has won the game")
            close(players[0])
        else:
            players.append(players.pop(0))

def finish():
    for p in players:
        p.connection.close()

if __name__ == '__main__':
    util.out("Server start")
    start()
    run()
    finish()
    util.out("Server shutdown")
