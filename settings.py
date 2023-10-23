import json
import datetime


class Settings:
    def __init__(self, m):
        self.m = m
        # Aspect ratio must be 2:1
        self.screen_width = 1200
        self.screen_height = 600
        self.post_cost = 10

        # Temp variables
        # Bools
        self.game_running = True

        # Variables to save
        try:
            with open('data/users/user.json', 'r') as f:
                self.stats = json.load(f)
            self.load_stats()

        except IndexError:
            self.stats = [0, 0, 0, 0, 0, 0, 1, 25, 0, 10, 500, '', 0, False, datetime.datetime.now().day, 0, 1, 5, 10]
            self.load_stats()

        with open('data/users/purchased_apps.json', 'r') as f:
            self.purchased_apps = json.load(f)

    def update_pps_value(self):
        self.pps = self.subscribers / 100

    def reset_stats(self):
        self.m.screen.fill((0, 0, 0))
        self.purchased_apps = []
        with open('data/users/user.json', 'w') as f:
            json.dump([0, 0, 0, 0, 0, 0, 1, 25, 0, 10, 1000, '', 0, False, datetime.datetime.now().day, self.golden_pretzels, 1, 5, 10], f)
        with open('data/users/user.json', 'r') as f:
            self.stats = json.load(f)
        with open('data/users/purchased_apps.json', 'w') as f:
            json.dump([], f)
        with open('data/videos.json', 'w') as f:
            json.dump({}, f)
        for stock in ['abibos', 'crapple', 'pingles', 'poopsi']:
            with open(f'data/stocks/{stock}.json', 'w') as f:
                json.dump([[0], [0]], f)
        self.load_stats()

    def get_like_view(self, option: int):
        if option == 0:
            self.pretzels += self.like_give
        elif option == 2:
            self.pretzels += 100
        else:
            self.pretzels += 10

    def update_like_sub(self):
        videos = self.m.game.apps.me_toob.video_dict
        for key, value in videos.items():
            self.subscribers += value[1]
            self.likes += value[2]
            value[1] = 0
            value[2] = 0

    def load_stats(self):
        self.pretzels = self.stats[0]
        self.t_bear_fed = self.stats[1]
        self.pps = self.stats[2]
        self.likes = self.stats[3]
        self.subscribers = self.stats[4]
        self.views = self.stats[5]
        self.pretzels_per_click = self.stats[6]
        self.bear_feed_cost = self.stats[7]
        self.level = self.stats[8]
        self.level_up = self.stats[9]
        self.sub_cost = self.stats[10]
        self.stock = self.stats[11]
        self.stock_buy_price = self.stats[12]
        self.daily_keywords = self.stats[13]
        self.last_date = self.stats[14]
        self.golden_pretzels = self.stats[15]
        self.ppc_cost = self.stats[16]
        self.like_give = self.stats[17]
        self.like_cost = self.stats[18]

    def save_stats(self):
        self.stats = [
            self.pretzels, self.t_bear_fed, self.pps, self.likes, self.subscribers, self.views, self.pretzels_per_click,
            self.bear_feed_cost, self.level, self.level_up, self.sub_cost, self.stock, self.stock_buy_price,
            self.daily_keywords, datetime.datetime.now().day, self.golden_pretzels, self.ppc_cost, self.like_give, self.like_cost]
        with open('data/users/user.json', 'w') as f:
            json.dump(self.stats, f)
        with open('data/users/purchased_apps.json', 'w') as f:
            json.dump(self.purchased_apps, f)
        with open('data/videos.json', 'w') as f:
            json.dump(self.m.game.apps.me_toob.video_dict, f)
