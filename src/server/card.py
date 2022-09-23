import copy
import json
import os
import util

player_amount = 0

def from_file(path):
    with open(path) as f:
        return json.load(f, object_hook=from_dct)

def from_dct(dct):
    return Card(dct.get("name", ""), dct.get("desc", ""),
        dct.get("type", "Secondary Industry"),
        dct.get("icon", ""), dct.get("activation_no", []),
        dct.get("activation", "self"), dct.get("cost", 1),
        dct.get("start", 0), dct.get("available", 2),
        dct.get("actions", []), dct.get("investable", 0))

def error(name, param):
    util.out("There was an error with the parameter " + param + " for the card " + name + ". A correction will be attepted or a fallback will be used")

class Card:
    name = ""
    desc = ""
    type = "Secondary Industry"
    icon = ""
    activation_no = []
    activation = ""
    cost = 1
    start = 0
    available = 2
    actions = []
    investable = 0
    renovating = False
    investment = 0

    def __init__(self, name, desc, type, icon, activation_no, activation, cost,
        start, available, actions, investable):
        self.name = name
        self.desc = desc
        self.type = type
        self.icon = "".join(icon.split())
        if self.icon != icon or self.icon == "":
            error(self.name, "icon")
        if self.icon == "":
            self.icon = "bread"
        self.activation_no = activation_no
        self.activation = activation.lower()
        if self.activation not in ["passive", "self", "others", "all"] or self.activation != activation:
            error(self.name, "activation")
        if self.activation not in ["passive", "self", "others", "all"]:
            if type == "Landmark":
                self.activation = "passive"
            if type == "Primary Industry":
                self.activation = "all"
            if type == "Restaurants":
                self.activation = "others"
            else:
                self.activation = "self"
        self.cost = cost
        self.start = start
        if self.start > 1 and self.icon == "tower":
            error(self.name, "start")
            self.start = 1
        if available + self.start != 1 and self.icon == "tower":
            error(self.name, "available")
            available = 1 - self.start
        self.available = available * player_amount
        self.actions = actions
        self.investable = investable

    def get_copy(self):
        new = copy.deepcopy(self)
        new.available = 0
        return new

    def gen_info(self):
        info = []
        info.append(("name", util.align("Name"), self.name, ))
        info.append(("desc", util.align("Description"), self.desc, ))
        info.append(("type", util.align("Type"), self.type, ))
        info.append(("icon", util.align("Icon"), self.icon, ))
        info.append(("activation_no", util.align("Activation numbers"), ''.join(str(x) for x in self.activation_no), ))
        info.append(("activation", util.align("Activation mode"), self.activation, ))
        info.append(("cost", util.align("Cost"), self.cost, ))
        info.append(("start", util.align("Start"), self.start, ))
        info.append(("available", util.align("Available"), self.available, ))
        info.append(("investable", util.align("Investable"), self.investable, ))
        info.append(("actions", "", self.actions, ))
        return info
