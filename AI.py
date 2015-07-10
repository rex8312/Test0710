__author__ = 'rex8312'

import random
from Objects import *
from Consts import *
from sqlitedict import SqliteDict


class PlayerAI:
    next_action = ACTION.NONE
    money = 15
    team = None
    hq = None

    def random_act(self, state):
        if self.next_action is ACTION.NONE:
            self.next_action = random.choice(ACTION_LIST)
        return self.do_action(state)

    def do_action(self, state):
        if self.next_action is not ACTION.NONE:
            if self.next_action // 100 == 9:
                if self.money >= self.next_action % 100 * 10:
                    self.next_action = ACTION.NONE

            elif self.next_action // 100 == 1:
                y = self.next_action % 100 // 10
                x = self.next_action % 10
                unit = Rock(self.team, x, y)
                self.money -= unit.cost
                state[y][x][self.team].append(unit)
                self.next_action = ACTION.NONE

            elif self.next_action // 100 == 2:
                y = self.next_action % 100 // 10
                x = self.next_action % 10
                unit = Scissors(self.team, x, y)
                self.money -= unit.cost
                state[y][x][self.team].append(unit)
                self.next_action = ACTION.NONE

            elif self.next_action // 100 == 3:
                y = self.next_action % 100 // 10
                x = self.next_action % 10
                unit = Paper(self.team, x, y)
                self.money -= unit.cost
                state[y][x][self.team].append(unit)
                self.next_action = ACTION.NONE

        return state


class RedPlayerAI(PlayerAI):
    def __init__(self, hq):
        self.team = TEAM.RED
        self.hq = hq
        self.act = self.random_act


class BluePlayerAI(PlayerAI):
    def __init__(self, hq):
        self.team = TEAM.BLUE
        self.hq = hq
        self.model = None

    def act(self, state, q=None):
        if self.next_action is ACTION.NONE:
            self.next_action = self.model.query(q)
        self.do_action(state)
        return state


def group_ai(state):
    for y in range(3):
        for x in range(3):
            for entity in state[y][x][TEAM.RED]:
                if len(state[y][x][TEAM.BLUE]) > 0:
                    target = random.choice(state[y][x][TEAM.BLUE])
                    entity.attack_to(target)
                elif not isinstance(entity, HQ):
                    x = random.choice(range(3))
                    y = random.choice(range(3))
                    entity.move_to(x, y)
            for entity in state[y][x][TEAM.BLUE]:
                if len(state[y][x][TEAM.RED]) > 0:
                    target = random.choice(state[y][x][TEAM.RED])
                    entity.attack_to(target)
                elif not isinstance(entity, HQ):
                    x = random.choice(range(3))
                    y = random.choice(range(3))
                    entity.move_to(x, y)
    return state