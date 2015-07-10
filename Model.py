__author__ = 'rex8312'

from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
from Consts import *


class RandomModel:
    def query(self, q):
        return random.choice(ACTION_LIST)


class Model:
    indexer = None
    conditions = None
    actions = None
    rewards = None

    def __init__(self, conditions, actions, rewards):
        self.conditions = conditions
        self.actions = actions
        self.rewards = rewards
        self.indexer = NearestNeighbors(n_neighbors=25, algorithm='ball_tree').fit(conditions[:50])

    def query(self, q):
        try:
            distances, indices = self.indexer.kneighbors(q)
            nns = list()
            for idx, distance in zip(indices[0], distances[0]):
                nns.append([self.actions[idx], self.rewards[idx], distance])

            summary = dict()
            R = 0
            D = 1
            for action, reward, distance in nns:
                summary.setdefault(action, [list(), list()])
                summary[action][R].append(reward)
                summary[action][D].append(distance)

            for action in summary:
                summary[action][R] = np.mean(summary[action][R])
                summary[action][D] = np.mean(summary[action][D])

            unexp_actions = set(ACTION_LIST) - set(summary.keys())
            print unexp_actions
            if len(unexp_actions) > 0:
                decision = random.choice(ACTION_LIST)
                print decision, '?', '?'
            else:
                decision = summary.keys()[0]
                max_reward = -10e10
                max_distance = -10e10
                for action in summary:
                    if summary[action][R] + summary[action][D] > max_reward + max_distance:
                        decision = action
                        max_reward, max_distance = summary[action][R], summary[action][D]
                print decision, max_reward, max_distance

            return decision
        except ValueError:
            return random.choice(ACTION_LIST)




