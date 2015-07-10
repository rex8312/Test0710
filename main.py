__author__ = 'rex8312'

import time
import numpy as np
import pylab as pl
from AI import *
from DataManager import *

VISUAL = False

def update(state):
    _state = [[(list(), list()) for x in range(3)] for y in range(3)]

    for y in range(3):
        for x in range(3):
            for team in (TEAM.RED, TEAM.BLUE):
                for entity in state[y][x][team]:
                    if entity.hp > 0:
                        _x, _y = entity.next_move
                        _state[_y][_x][team].append(entity)
    return _state


def draw(state_view, assets_view, progress_view, state, data_manager):
    state_view.cla()
    values = np.zeros((3, 4))
    for y in range(3):
        for x in range(3):
            for entity in state[y][x][TEAM.RED]:
                values[y][x] += entity.hp
            for entity in state[y][x][TEAM.BLUE]:
                values[y][x] -= entity.hp
            values[y][x] = min(values[y][x], 100)
            values[y][x] = max(values[y][x], -100)

    values[0][3] = 100
    values[1][3] = 0
    values[2][3] = -100

    #print values
    state_view.imshow(values, interpolation='nearest', cmap='bwr')

    assets_view.cla()
    assets_view.axis([0, max(50, len(data_manager.red_assets)), 0, 200])
    assets_view.plot(data_manager.red_assets, 'r')
    assets_view.plot(data_manager.blue_assets, 'b')

    progress_view.cla()
    wins = data_manager.get_wins()
    progress_view.axis([0, len(wins), 0, 1])
    progress_view.plot(wins)

    pl.pause(1./FPS)


def game():
    tick = 0
    state = [[(list(), list()) for x in range(3)] for y in range(3)]

    red_hq = HQ(TEAM.RED, 1, 0)
    blue_hq = HQ(TEAM.BLUE, 1, 2)

    state[0][1][TEAM.RED].append(red_hq)
    state[2][1][TEAM.BLUE].append(blue_hq)

    red_player_ai = RedPlayerAI(red_hq)
    blue_player_ai = BluePlayerAI(blue_hq)

    if VISUAL:
        gs = pl.GridSpec(5, 1)
        state_view = pl.subplot(gs[:3, :])
        assets_view = pl.subplot(gs[3, :])
        progress_view = pl.subplot(gs[4, :])

    data_manager = DataManager()
    data_manager.reset()
    model = data_manager.get_model()
    blue_player_ai.model = model

    result = RESULT.DRAW
    while True:
        if red_player_ai.hq.hp <= 0 and blue_player_ai.hq.hp <= 0:
            print 'DRAW'
            data_manager.add_win(RESULT.DRAW)
            break
        elif red_player_ai.hq.hp <= 0:
            print 'BLUE WIN'
            result = RESULT.BLUE_WIN
            data_manager.add_win(RESULT.BLUE_WIN)
            break
        elif blue_player_ai.hq.hp <= 0:
            print 'RED_WIN'
            result = RESULT.RED_WIN
            data_manager.add_win(RESULT.RED_WIN)
            break

        #print 'R', red_player_ai.money, red_hq.hp
        #print 'B', blue_player_ai.money, blue_hq.hp
        state = blue_player_ai.act(state, q=data_manager.transform(state, red_player_ai, blue_player_ai))
        state = red_player_ai.act(state)

        state = group_ai(state)
        state = update(state)
        red_player_ai.money += 1
        blue_player_ai.money += 1
        red_asstes, blue_assets = data_manager.evaluate_state(state, red_player_ai, blue_player_ai)
        data_manager.add_sa(tick, red_player_ai, blue_player_ai, state, red_asstes, blue_assets)
        state = update(state)
        if VISUAL:
            draw(state_view, assets_view, progress_view, state, data_manager)
        tick += 1
        #print

    if VISUAL:
        pl.pause(3)
    data_manager.save()
    return result


if __name__ == '__main__':
    while True:
        if VISUAL:
            pl.ion()
        print game()
