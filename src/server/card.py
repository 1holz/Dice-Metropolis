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
        dct.get("start", 0), dct.get("availabel", 2),
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
    availabel = 2
    actions = []
    investable = 0
    renovating = False
    investment = 0

    def __init__(self, name, desc, type, icon, activation_no, activation, cost,
        start, availabel, actions, investable):
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
        if self.activation not in ["passiv", "self", "others", "all"] or self.activation != activation:
            error(self.name, "activation")
        if self.activation not in ["passiv", "self", "others", "all"]:
            if type == "Landmark":
                self.activation = "passiv"
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
        if availabel + self.start != 1 and self.icon == "tower":
            error(self.name, "availabel")
            self.availabel = 1 - self.start
        self.availabel = self.availabel * player_amount
        self.actions = actions
        self.investable = investable

    def get_copy(self):
        new = copy.deepcopy(self)
        new.availabel = 0
        return new

    def gen_string(self):
        string = self.name
        if self.renovating:
            string.append(" in renovation")
        if self.investable and self.investment != 0:
            string.append(" with " + str(self.investment) + " invested")
        return string

    def gen_strings(self):
        strings = []
        strings.append("Name:               " + self.name)
        strings.append("Description:        " + self.desc)
        strings.append("Type:               " + self.type)
        strings.append("Icon:               " + self.icon)
        strings.append("Activation numbers: " + ''.join(str(x) for x in self.activation_no))
        strings.append("Activation mode:    " + self.activation)
        strings.append("Cost:               " + str(self.cost))
        strings.append("Start:              " + str(self.start))
        strings.append("Availabel:          " + str(self.availabel))
        strings.append("Investable:         " + str(self.investable))
        return strings
