import json
import time
import pygame
import random
import datetime
import os

from stocks import Stock
from box_gui import TextBox, ImageBox
from algorithm import Algorithm, Video


class Apps:
    def __init__(self, m):
        self.m = m
        self.me_toob = MeToobApp(m)
        self.hack = LikeSubHackApp(m)
        self.stocks = StockApp(m)
        self.apps = [self.me_toob, self.hack, self.stocks]


class App:
    def __init__(self, m, app_name: str, cost: int, level_needed=0, purchased=False, active=False):
        self.m = m
        self.settings = m.stgs

        self.app_name = app_name
        self.cost = cost
        self.purchased = purchased
        self.active = active
        self.level_needed = level_needed

        self.app_area = m.app_area

        if self.app_name in self.settings.purchased_apps:
            self.purchased = True

        self.bg_img = ImageBox(m, 'images/paper_texture.png', 800, 600, self.app_area[0], 0)
        self.title = TextBox(m, self.app_name, 0, 0, (0, 0, 0), (200, 6, 16), (self.app_area[2] - self.app_area[0]),
                             40, 40, True)
        self.back_button = ImageBox(m, 'images/back_arrow.png', 40, 40, self.app_area[0] + 5, 20)

    def unpurchase(self):
        if self.app_name in self.settings.purchased_apps:
            self.purchased = True
        else:
            self.purchased = False

    def purchase_app(self):
        if not self.purchased:
            self.purchased = True
            self.settings.purchased_apps.append(self.app_name)


class MeToobApp(App):
    def __init__(self, m):
        super().__init__(m, 'MeToob', 20, 0, False, False)
        self.m = m
        self.stock_app = StockApp(m)

        self.post_button = ImageBox(m, 'images/create_btn.png', 100, 45, self.app_area[2] - 120, 20)

        self.active_vid = 0
        with open('data/videos.json', 'r') as f:
            self.video_dict = json.load(f)
        self.update_vid_list()

        # For posting
        self.posting = False
        self.brands = ['* Pingles', '* Poopsi', '* Abibos', '* Crapple']
        offset = 50
        self.brands_textbox = []
        self.typing = False
        self.hack = LikeSubHackApp(m)
        i = 2
        for brand in self.brands:
            brand = TextBox(m, brand, 0, 0, (0, 0, 0), (0, 0, 0), (self.app_area[0] + 40) + offset * i, 150, 25, True)
            i += 2
            self.brands_textbox.append(brand)

        self.choice_1 = self.brands_textbox[0]
        self.choice_2 = ''

        self.brand_choice = TextBox(self.m, 'What brand are you gonna promote?', 0, 0, (0, 0, 0), (0, 0, 0),
                                    self.app_area[0] + 30, 100, 30, True, 'left')
        self.video_text_choice = TextBox(self.m, 'What would you like your video to say? (keywords matter!)', 0, 0,
                                         (0, 0, 0), (0, 0, 0),
                                         self.app_area[0] + 30, 250, 30, True, 'left')
        self.video_text_input = TextBox(self.m, self.choice_2, 200, 25, (200, 6, 16), (0, 0, 0),
                                        self.app_area[0] + 140, 300, 25, False, 'left')
        self.submit_button = ImageBox(m, 'images/submit.png', 100, 45, self.app_area[0] + 30, 350)
        self.stat_counter = TextBox(self.m,
                                    f'Subscribers: {self.settings.subscribers}\tLikes: {self.settings.likes}\t Views: {self.settings.views}',
                                    0, 0, (255, 255, 255), (0, 0, 0), self.app_area[0] + 10, 550, 40, False, 'left')
        self.error_msg = TextBox(self.m, f'You need {self.settings.post_cost - self.settings.pretzels} more pretzels!',
                                 0, 0, (0, 0, 0), (200, 6, 16), self.app_area[0] + 30, 390, 30, True, 'left')

    def update_vid_list(self):
        self.video_imgs = []
        for key in self.video_dict:
            video = ImageBox(self.m, f'images/posts/{key}.png', 500, 500,
                             (self.app_area[2] - self.app_area[0] + 125) // 2,
                             90)
            self.video_imgs.append(video)
        self.active_vid = len(self.video_imgs) - 1

    def post_video(self):
        if self.settings.pretzels - self.settings.post_cost >= 0:
            self.settings.pretzels -= self.settings.post_cost
            video = Video(self.choice_1.msg, self.choice_2)
            video.make_img()

            algo = Algorithm(self.m, self.stock_app)
            algo.analyze_vid(video, self.hack.keywords)

            self.video_dict[video.random_post_id] = [video.save_dir, 0, 0, algo.video_points, 0, algo.sub_like_range,
                                                     time.time(), self.choice_1.msg[2:].lower()]
            self.update_vid_list()
            self.m.stgs.save_stats()
            self.choice_2 = ''
            for stock in self.stock_app.stocks:
                stock.update_vid_list()
                stock.calc_video_influence()
            self.posting = False

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_typing(event)
            if event.key == pygame.K_ESCAPE:
                self.active = False
                self.posting = False
            if event.key == pygame.K_LEFT:
                if self.active_vid == len(self.video_imgs) - 1:
                    self.active_vid = 0
                else:
                    self.active_vid += 1
            elif event.key == pygame.K_RIGHT:
                if self.active_vid == 0:
                    self.active_vid = len(self.video_imgs) - 1
                else:
                    self.active_vid -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                clicked = self.back_button.rect.collidepoint(mouse_pos)
                if clicked:
                    self.active = False
                    self.posting = False
                clicked = self.post_button.rect.collidepoint(mouse_pos)
                if clicked:
                    self.posting = True

                if self.posting:
                    for brand in self.brands_textbox:
                        clicked = brand.msg_image_rect.collidepoint(mouse_pos)
                        if clicked:
                            self.choice_1 = brand
                            break
                    clicked = self.video_text_input.rect.collidepoint(mouse_pos)
                    if clicked:
                        self.typing = True
                    else:
                        self.typing = False
                    clicked = self.submit_button.rect.collidepoint(mouse_pos)
                    if clicked:
                        self.post_video()

    def check_typing(self, event):
        if self.typing:
            if event.key == pygame.K_BACKSPACE:
                self.choice_2 = self.choice_2[:-1]
            else:
                self.choice_2 += event.unicode

    def update_screen(self):
        self.bg_img.draw_image()

        if self.typing:
            self.video_text_input.button_color = (255, 0, 0)
        else:
            self.video_text_input.button_color = (200, 6, 16)

        self.settings.update_like_sub()

        if not self.posting:
            self.post_button.draw_image()
            try:
                self.video_imgs[self.active_vid].draw_image()
            except IndexError:
                pass
            self.stat_counter.prep_msg(
                f'Subscribers: {self.settings.subscribers}   Likes: {self.settings.likes}   Views: {self.settings.views}'
            )
            self.stat_counter.draw_box()
        else:
            self.brand_choice.draw_box()
            self.video_text_choice.draw_box()
            for brand in self.brands_textbox:
                if brand != self.choice_1:
                    brand.text_color = (0, 0, 0)
                    brand.prep_msg(brand.msg)
                else:
                    brand.text_color = (200, 6, 16)
                    brand.prep_msg(brand.msg)
                brand.draw_box()
            self.video_text_input.prep_msg(self.choice_2)
            self.video_text_input.draw_box()
            self.submit_button.draw_image()

            if self.settings.post_cost - self.settings.pretzels > 0:
                self.error_msg.prep_msg(f'You need {self.settings.post_cost - self.settings.pretzels} more pretzels!')
                self.error_msg.draw_box()

        self.title.draw_box()
        self.back_button.draw_image()
        self.check_vid_oldness()

    def check_vid_oldness(self):
        for key, value in self.video_dict.items():
            oldness = round(time.time() - value[6])
            if oldness >= 7200:
                os.remove(self.video_dict[key][0])
                del self.video_dict[key]
                self.update_vid_list()
                break


class LikeSubHackApp(App):
    def __init__(self, m):
        super().__init__(m, 'Sub and Like Hack', 2000, 2, False, False)
        self.m = m

        with open('data/keywords.json', 'r') as f:
            self.keywords = json.load(f)
        self.possible_keywords = ['poop', 'lol', 'pee', 'bear', 'abibos', 'metoob', 'donald nasplukker', 'stewz',
                                  'tnnl', 'pretzel', 'toilet', 'poopy buttcheeck', 'dum', 'coolio', 'lololol']
        self.start_t = time.time()

        self.sub_button = ImageBox(m, 'images/sub_button.png', 250, 80, self.app_area[0] + 50, 80)
        self.like_button = ImageBox(m, 'images/like_button.png', 250, 80, self.app_area[0] + 50, 180)
        self.ppc_button = ImageBox(m, 'images/ppc_button.png', 250, 80, self.app_area[0] + 50, 280)
        self.sub_btn_cost = TextBox(m, f'cost: {self.settings.sub_cost}', 0, 0, (0, 0, 0), (0, 0, 0),
                                    self.app_area[0] + 310, 90, 40, True, 'left')
        self.like_btn_cost = TextBox(m, 'cost: 5', 0, 0, (0, 0, 0), (0, 0, 0), self.app_area[0] + 310, 190, 40, True,
                                     'left')
        self.ppc_btn_cost = TextBox(m, f'cost: {self.settings.ppc_cost}', 0, 0, (0, 0, 0), (0, 0, 0),
                                    self.app_area[0] + 310, 290, 40, True, 'left')

        self.keyword_show = TextBox(m, f'Show daily keywords for 1000 pretzels', 0, 0, (0, 0, 0), (0, 0, 0),
                                    self.app_area[0] + 50, 390, 30, True, 'left')
        self.keyword_box = TextBox(m, f'The keywords are: {self.keywords[0]}, {self.keywords[1]}', 0, 0, (0, 0, 0),
                                   (0, 0, 0),
                                   self.app_area[0] + 50, 390, 30, True, 'left')

    def pick_keywords(self):
        self.keywords = []
        for i in range(2):
            self.keywords.append(random.choice(self.possible_keywords))
        with open('data/keywords.json', 'w') as f:
            json.dump(self.keywords, f)
        self.settings.daily_keywords = False

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                clicked = self.back_button.rect.collidepoint(mouse_pos)
                if clicked:
                    self.active = False

                clicked = self.keyword_show.msg_image_rect.collidepoint(mouse_pos)
                if clicked and self.settings.pretzels >= 1000:
                    self.settings.daily_keywords = True

                clicked = self.sub_button.rect.collidepoint(mouse_pos)
                if clicked and self.settings.pretzels >= self.settings.sub_cost:
                    self.settings.subscribers += 1
                    self.settings.pretzels -= self.settings.sub_cost
                    self.settings.sub_cost += self.settings.sub_cost // 10
                clicked = self.ppc_button.rect.collidepoint(mouse_pos)
                if clicked and self.settings.pretzels >= self.settings.ppc_cost:
                    self.settings.pretzels_per_click += 1
                    self.settings.pretzels -= self.settings.ppc_cost
                    self.settings.ppc_cost += self.settings.ppc_cost // 5
                clicked = self.like_button.rect.collidepoint(mouse_pos)
                if clicked and self.settings.pretzels >= 5:
                    self.settings.likes += 1
                    self.settings.pretzels -= 5
                    self.settings.pretzels += 5

    def update_screen(self):
        end_t = time.time()
        if end_t - self.start_t >= 10800:
            self.pick_keywords()

        self.bg_img.draw_image()
        self.sub_button.draw_image()
        self.like_button.draw_image()
        self.sub_btn_cost.prep_msg(f'cost: {self.settings.sub_cost}')
        self.sub_btn_cost.draw_box()
        self.ppc_btn_cost.prep_msg(f'cost: {self.settings.ppc_cost}')
        self.ppc_btn_cost.draw_box()
        self.ppc_button.draw_image()
        self.like_btn_cost.draw_box()
        self.title.draw_box()
        self.back_button.draw_image()

        if self.settings.daily_keywords:
            self.keyword_box.prep_msg(f'The most popular searches today are: {self.keywords[0]}, {self.keywords[1]}')
            self.keyword_box.draw_box()
        else:
            if self.settings.pretzels >= 1000:
                self.keyword_show.text_color = (0, 0, 0)
                self.keyword_show.prep_msg('Show todays\'s popular searches for 1000 pretzels')
            else:
                self.keyword_show.text_color = (255, 0, 0)
                self.keyword_show.prep_msg(
                    f'You need {1000 - self.settings.pretzels} more pretzels to show todays\'s popular searches')
            self.keyword_show.draw_box()

        current_time = datetime.datetime.now().day
        if current_time != self.settings.last_date:
            self.settings.last_date = current_time
            self.pick_keywords()


class StockApp(App):
    def __init__(self, m):
        super().__init__(m, 'Stock Market', 10000, 5, False, False)
        self.stocks = [Stock('pingles'), Stock('poopsi'), Stock('abibos'), Stock('crapple')]
        y = 80
        self.stock_btns = []
        self.buy_stock_btns = []
        self.rise_percents, self.fall_percents = [], []
        self.reset_btn = TextBox(m, 'Reset (1000 pretzels)', 0, 0, (0, 0, 0), (0, 0, 0), self.app_area[2] - 220, 25, 30,
                                 True, 'left')
        self.selected_stock = self.settings.stock
        for stock in self.stocks:
            stock_btn = TextBox(m, f'{stock.name.title()}: {stock.value}', 120, 27, (0, 0, 0), (255, 255, 255),
                                self.app_area[0] + 50, y, 30, False, 'left', stock)
            fall_per = TextBox(m, f'{round(stock.chance_fall, 2)}%', 0, 0, (0, 0, 0), (255, 0, 0),
                               self.app_area[0] + 50, y + 30, 30, True, 'left')
            rise_per = TextBox(m, f'{round(stock.chance_rise, 2)}%', 0, 0, (0, 0, 0), (38, 171, 42),
                               self.app_area[0] + 140, y + 30, 30, True, 'left')
            buy_btn = TextBox(m, f'Select', 0, 0, (0, 0, 0), (0, 0, 0), self.app_area[0] + 230, y + 30, 30, True,
                              'left', stock)
            y += 85
            self.rise_percents.append(rise_per)
            self.fall_percents.append(fall_per)
            self.stock_btns.append(stock_btn)
            self.buy_stock_btns.append(buy_btn)

            if stock.name == self.selected_stock:
                self.stock_price = stock.value

    def get_stock_val(self):
        for stock in self.stocks:
            if stock.name == self.selected_stock:
                self.stock_price = stock.value
                return self.stock_price
        return 0

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                clicked = self.back_button.rect.collidepoint(mouse_pos)
                if clicked:
                    self.active = False

                for stock in self.stocks:
                    stock_btn = self.stock_btns[self.stocks.index(stock)]
                    clicked = stock_btn.rect.collidepoint(mouse_pos)
                    if clicked:
                        stock_btn.app.active = True

                    buy_btn = self.buy_stock_btns[self.stocks.index(stock)]
                    clicked = buy_btn.msg_image_rect.collidepoint(mouse_pos)
                    if clicked and self.selected_stock != buy_btn.app.name:
                        self.buy_stock(self.stocks[self.buy_stock_btns.index(buy_btn)])
                    elif clicked and self.selected_stock == buy_btn.app.name:
                        self.sell_stock(self.stocks[self.buy_stock_btns.index(buy_btn)])

                clicked = self.reset_btn.msg_image_rect.collidepoint(mouse_pos)
                if self.settings.pretzels >= 1000 and clicked:
                    self.settings.pretzels -= 1000
                    for stock in self.stocks:
                        stock.reset()

    def update_screen(self):
        self.bg_img.draw_image()
        if self.settings.pretzels >= 1000:
            self.reset_btn.draw_box()

        for stock in self.stocks:
            if not stock.active:
                stock.simulate(0)
            else:
                stock.show_graph()

        for stock in self.stocks:
            stock_btn = self.stock_btns[self.stocks.index(stock)]
            stock_btn.prep_msg(f'{stock.name.title()}: {stock.value}')
            stock_btn.draw_box()

            buy_btn = self.buy_stock_btns[self.stocks.index(stock)]
            if stock.value <= self.settings.pretzels:
                buy_btn.text_color = (0, 0, 0)
            else:
                buy_btn.text_color = (255, 0, 0)
            if self.stocks[self.buy_stock_btns.index(buy_btn)].name == self.selected_stock:
                buy_btn.prep_msg('Sell')
            else:
                buy_btn.prep_msg('Buy')
            buy_btn.draw_box()

            self.rise_percents[self.stocks.index(stock)].prep_msg(f'{round(stock.chance_rise, 2)}%')
            self.rise_percents[self.stocks.index(stock)].draw_box()
            self.fall_percents[self.stocks.index(stock)].prep_msg(f'{round(stock.chance_fall, 2)}%')
            self.fall_percents[self.stocks.index(stock)].draw_box()

        self.title.draw_box()
        self.back_button.draw_image()

    def buy_stock(self, stock):
        if self.settings.pretzels >= stock.value:
            self.settings.pretzels -= stock.value
            self.settings.stock_buy_price = stock.value
            self.selected_stock = stock.name
            for stock in self.stocks:
                if stock.name == self.selected_stock:
                    self.stock_price = stock.value
                    break
            self.settings.stock = self.selected_stock

    def sell_stock(self, stock):
        self.settings.pretzels += stock.value
        self.settings.stock_buy_price = 0
        self.selected_stock = ""
        self.settings.stock = self.selected_stock
