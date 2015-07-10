__author__ = 'rex8312'

from sqlitedict import SqliteDict
from uuid import uuid4
from time import time
from Consts import *
from Objects import *
import csv
import numpy as np
from sklearn.neighbors import NearestNeighbors
from Model import *


game_sar_file_name = "data/sars.csv"
game_win_file_name = "data/wins.csv"
DISCOUNT_FACTOR = 0.1


class DataManager:
    game_sars_buffer = list()
    game_wins_buffer = list()
    red_assets = list()
    blue_assets = list()

    def reset(self):
        self.game_sars_buffer = list()
        self.game_wins_buffer = list()
        self.red_assets = list()
        self.blue_assets = list()

    def save(self):
        with open(game_sar_file_name, 'ab') as game_sar_file:
            game_sars_buff = self.game_sars_buffer[:]
            game_sars_buff.extend([game_sars_buff[-1] for _ in range(11)])
            game_log_writer = csv.writer(game_sar_file)
            for i, game_log in enumerate(game_sars_buff[:-11]):
                game_log['r'] = 0
                for j in range(1, 11):
                    game_log['r'] += 0.7 ** j * (game_sars_buff[i + j]['e'] - game_log['e'])
                game_log_writer.writerow(game_log['s'] + [game_log['a'], game_log['r']])
            self.game_sars_buffer = list()

        with open(game_win_file_name, 'ab') as game_win_file:
            game_wins_writer = csv.writer(game_win_file)
            for game_win in self.game_wins_buffer:
                game_wins_writer.writerow([game_win['w']])
            self.game_wins_buffer = list()

        self.red_assets = list()
        self.blue_assets = list()

    def transform(self, state, red_player, blue_player):
        vec = [red_player.money, blue_player.money]
        for y in range(3):
            for x in range(3):
                area_vec = [0, 0, 0, 0, 0, 0, 0, 0]
                for entity in state[y][x][TEAM.RED]:
                    if isinstance(entity, HQ):
                        area_vec[0] += 1
                    elif isinstance(entity, Rock):
                        area_vec[1] += 1
                    elif isinstance(entity, Scissors):
                        area_vec[2] += 1
                    elif isinstance(entity, Paper):
                        area_vec[3] += 1
                for entity in state[y][x][TEAM.BLUE]:
                    if isinstance(entity, HQ):
                        area_vec[4] += 1
                    elif isinstance(entity, Rock):
                        area_vec[5] += 1
                    elif isinstance(entity, Scissors):
                        area_vec[6] += 1
                    elif isinstance(entity, Paper):
                        area_vec[7] += 1
                vec.extend(area_vec)
        return vec

    def add_sa(self, tick, red_player, blue_player, state, red_assets, blue_assets):
        vec = self.transform(state, red_player, blue_player)
        self.game_sars_buffer.append({'s': vec, 'a': blue_player.next_action, 'e': blue_assets - red_assets})

    def add_win(self, win):
        self.game_wins_buffer.append({'w': win, 't': time()})

    def get_model(self):
        conditions = list()
        actions = list()
        rewards = list()
        try:
            with open(game_sar_file_name, 'rb') as f:
                reader = csv.reader(f)
                for x in reader:
                    conditions.append(map(float, x[:-2]))
                    actions.append(int(x[-2]))
                    rewards.append(float(x[-1]))

            return Model(conditions, actions, rewards)
        except IOError:
            return RandomModel()

    def get_wins(self):
        wins = list()
        try:
            with open(game_win_file_name, 'rb') as game_win_file:
                reader = csv.reader(game_win_file)
                for win in reader:
                    wins.append(float(win[0]))

            N = 1
            if len(wins) > 50:
                N = 50
                wins = np.convolve(wins, [1./N for _ in range(N)])
            return wins[N:-N]
        except IOError:
            return [0.5]

    def evaluate_state(self, state, red_player, blue_player):
        red_assets = red_player.money
        blue_assets = blue_player.money

        for y in range(3):
            for x in range(3):
                for entity in state[y][x][TEAM.RED]:
                    red_assets += entity.hp
                for entity in state[y][x][TEAM.BLUE]:
                    blue_assets += entity.hp

        self.red_assets.append(red_assets)
        self.blue_assets.append(blue_assets)
        return red_assets, blue_assets



