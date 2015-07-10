__author__ = 'rex8312'

from Consts import *

# Game Objects
class GameObject:
    team = 0
    attack = 1
    hp = 10
    cost = 10
    stronger = None
    ap = 5
    state = STATE.LIVE
    next_move = (None, None)

    def __init__(self, team, x, y):
        self.team = team
        if isinstance(self, Scissors):
            self.stronger = Paper
        elif isinstance(self, Paper):
            self.stronger = Rock
        elif isinstance(self, Rock):
            self.stronger = Scissors
        self.next_move = x, y

    def attack_to(self, target):
        if isinstance(target, self.stronger):
            target.hp -= 2 * self.attack
        else:
            target.hp -= self.attack

    def move_to(self, x, y):
        self.next_move = (x, y)


class Rock(GameObject):
    hp = 20
    cost = 20
    attack = 3


class Scissors(GameObject):
    hp = 10
    cost = 10
    attack = 2


class Paper(GameObject):
    hp = 5
    cost = 5
    attack = 1


class HQ(GameObject):
    hp = 100

    def attack_to(self, target):
        pass

    def move_to(self, x, y):
        pass