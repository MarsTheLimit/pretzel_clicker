import random
import json
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Stock:
    def __init__(self, name: str):
        self.name = name
        self.active = False

        with open(f'data/stocks/{name}.json', 'r') as f:
            self.value_history = deque(json.load(f))
        self.value = self.value_history[0][-1]
        self.y = self.value_history[1][-1]

        self.chance_rise = 50
        self.chance_stay = 10
        self.chance_fall = 100 - (self.chance_rise + self.chance_stay)

        self.cleaned_videos = {}
        with open('data/videos.json', 'r') as f:
            videos = json.load(f)
        i = 0
        for key, value in videos.items():
            del value[0:4]
            del value[1]
            self.cleaned_videos[f'{i}'] = value
            i += 1

        self.options = ['rise', 'fall', 'neutral']
        self.fate = random.choices(self.options, weights=(self.chance_rise, self.chance_fall, self.chance_stay))

        self.calc_video_influence()

    def update_vid_list(self):
        self.cleaned_videos = {}
        with open('data/videos.json', 'r') as f:
            videos = json.load(f)
        i = 0
        for key, value in videos.items():
            del value[0:4]
            del value[1]
            self.cleaned_videos[f'{i}'] = value
            i += 1

    def calc_chance(self):
        self.fate = random.choices(self.options, weights=(self.chance_rise, self.chance_fall, self.chance_stay))
        return self.fate

    def calc_video_influence(self):
        for video, data in self.cleaned_videos.items():
            if data[2] == self.name:
                if data[0] >= 10000:
                    self.influence_stock(data[0] / 5000)
                else:
                    self.influence_stock(data[0] / 1000)

    def influence_stock(self, increase):
        self.chance_rise += increase
        if self.chance_rise > 100:
            self.chance_rise = 100
        self.chance_fall = 100 - (self.chance_rise + self.chance_stay)
        if self.chance_fall < 0:
            self.chance_fall = 0

    def simulate(self, i):
        fate = self.calc_chance()

        if fate == ['rise']:
            self.value += random.choices([1, 2, 3], weights=(75, 20, 5))[0]
        elif fate == ['fall']:
            self.value -= random.choices([1, 2, 3], weights=(50, 30, 20))[0]
        else:
            pass
        self.y += 1

        self.value_history[0].append(self.value)
        self.value_history[1].append(self.y)

        if self.y >= 100000:
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
        ani = animation.FuncAnimation(self.fig, self.simulate, interval=10, save_count=100000000)
        plt.show()
        self.active = False

    def reset(self):
        self.value_history = [[0], [0]]
        self.y = 0
        self.value = 0
