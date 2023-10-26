import random
import json
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time


class Stock:
    def __init__(self, name: str):
        self.name = name
        self.active = False
        self.start = time()

        with open(f'data/stocks/{name}.json', 'r') as f:
            self.value_history = deque(json.load(f))
        self.value = self.value_history[0][-1]
        self.y = self.value_history[1][-1]
        try:
            self.chance_rise += 0
        except AttributeError:
            print("init")
            self.chance_rise = 50
            self.chance_stay = 10
            self.chance_fall = 100 - (self.chance_rise + self.chance_stay)

        self.options = ['rise', 'fall', 'neutral']
        self.fate = random.choices(self.options, weights=(self.chance_rise, self.chance_fall, self.chance_stay))

    def calc_chance(self):
        self.fate = random.choices(self.options, weights=(self.chance_rise, self.chance_fall, self.chance_stay))
        return self.fate
    
    def get_percs(self):
        return [self.chance_rise, self.chance_fall]
        

    def influence_stock(self, increase):
        print("bbb", self.chance_rise, self.chance_fall)
        self.chance_rise += increase
        if self.chance_rise > 90:
            self.chance_rise = 90
        self.chance_fall = 100 - (self.chance_rise + self.chance_stay)
        if self.chance_fall < 0:
            self.chance_fall = 0

    def simulate(self, i):
        if time() - self.start >= 2:
            fate = self.calc_chance()

            if fate == ['rise']:
                self.value += random.choices([100, 200, 300], weights=(75, 20, 5))[0]
            elif fate == ['fall']:
                self.value -= random.choices([100, 200, 300], weights=(50, 30, 20))[0]
            else:
                pass
            self.y += 1

            self.value_history[0].append(self.value)
            self.value_history[1].append(self.y)

            if self.y >= 10000:
                self.reset()

            if self.active:
                self.ax1.clear()
                self.ax1.plot(self.value_history[1], self.value_history[0])

            with open(f'data/stocks/{self.name}.json', 'w') as f:
                json.dump(list(self.value_history), f)

    def show_graph(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        plt.ylabel('Value (pretzels)')
        plt.title(self.name)
        ani = animation.FuncAnimation(self.fig, self.simulate, interval=1000, save_count=10000)
        plt.show()
        self.active = False

    def reset(self):
        self.value_history = [[0], [0]]
        self.y = 0
        self.value = 0
