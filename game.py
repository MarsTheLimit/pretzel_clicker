import pygame
import time
import random
from time import time
import webbrowser
import os

from apps import Apps
from box_gui import TextBox, ImageBox
from algorithm import Algorithm


class Game:
    def __init__(self, m):
        self.m = m
        self.apps = Apps(self.m)
        self.settings = m.stgs
        self.app_area = m.app_area
        self.error = 0
        self.error_msg_active = False
        self.active = True
        self.start_t = time()

        self.help_btn = TextBox(self.m, 'Help', 0, 0, (0, 0, 0), (0, 0, 0), self.app_area[2] - 120, 20, 40, True, 'left')
        self.algo = Algorithm(m)
        self.bg_img = ImageBox(self.m, 'images/paper_texture.png', 800, 600, self.m.app_area[0], 0)
        self.title_img = TextBox(self.m, 'Apps', 0, 0, (0, 0, 0), (0, 0, 0), (self.app_area[2] - self.app_area[0]),
                                 40, 40, True)

        self.pretzel_button = ImageBox(m, 'images/pretzel.png', self.m.pretzel_area[2],
                                       self.settings.screen_height // 2, 0, 0)
        self.bear_button = ImageBox(m, f'images/bear{self.settings.level}.png', self.m.pretzel_area[2],
                                    self.settings.screen_height // 2, 0, self.settings.screen_height // 2)
        self.pretzel_counter = TextBox(m, f'{self.settings.pretzels} pretzels', 0, 0, (0, 0, 0),
                                       (255, 255, 255), 0, 0, 40, False, 'left')
        self.pps_counter = TextBox(m, f'{self.settings.pps} pps', 0, 0, (0, 0, 0), (0, 0, 0), 0,
                                   self.m.stgs.screen_height // 2 - 30,
                                   30, True, 'left')
        self.bear_fed_counter = TextBox(m, f'Bear has been fed {m.stgs.t_bear_fed} times', 0, 0, (0, 0, 0),
                                        (255, 255, 255), 0, self.settings.screen_height // 2, 40, False, 'left')
        self.bear_lvl_counter = TextBox(m, f'Level {self.settings.level} Bear', 0, 0, (0, 0, 0),
                                        (255, 255, 255), 5, self.settings.screen_height - 30, 30, True, 'left')
        self.bear_feed_cost_count = TextBox(m, f'Bear needs {self.settings.bear_feed_cost} pretzels', 0, 0, (0, 0, 0),
                                        (255, 255, 255), self.app_area[0], self.settings.screen_height - 30, 30, True, 'right')
        self.pretzels_stock = TextBox(m, f'{self.apps.stocks.get_stock_val() - self.settings.stock_buy_price}', 0, 0,
                                      (0, 0, 0), (0, 0, 0), self.app_area[0], self.m.stgs.screen_height // 2 - 30, 30,
                                      True, 'right')
        self.pretzels_stock.prep_msg(f'{self.apps.stocks.get_stock_val() - self.settings.stock_buy_price} from stocks')
        scale, size, offset = 2, self.settings.screen_height // 5, self.settings.screen_width // 15
        spacing = (self.settings.screen_width // 80) * scale + size // 2
        self.metoob_button = ImageBox(self.m, "images/me_toob.png", size, size, self.app_area[0] + spacing, spacing,
                                      self.apps.me_toob)
        self.hack_button = ImageBox(self.m, "images/hack.png", size, size, self.app_area[0] + spacing * 2 + offset,
                                    spacing, self.apps.hack)
        self.stock_button = ImageBox(self.m, "images/stock.png", size, size, self.app_area[0] + spacing * 4 + offset,
                                     spacing, self.apps.stocks)
        self.app_buttons = [self.metoob_button, self.hack_button, self.stock_button]
        self.locks = []
        self.level_locks = []
        for btn in self.app_buttons:
            lock = ImageBox(self.m, 'images/lock.png', btn.width, btn.width, btn.x, btn.y)
            lvl_lock = TextBox(self.m, f'lvl {btn.app.level_needed}', 0, 0, (0, 0, 0), (255, 255, 255),
                               btn.x + btn.width // 2,
                               btn.y + btn.width // 2, 30, True)
            self.locks.append(lock)
            self.level_locks.append(lvl_lock)

    def check_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.m.exit()

            for app in self.apps.apps:
                if app.active:
                    app.check_events(event)
                    self.active = False
                    break
                else:
                    self.active = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_mouse(event, mouse_pos)

            if self.active:
                if event.type == pygame.KEYDOWN:
                    self.check_keydown(event)

    def check_keydown(self, event):
        if event.key == pygame.K_F11:
            self.m.exit()

    def check_keyup(self, event):
        pass

    def algorithm(self):
        user = random.randint(0, 10)
        if user == 1:
            try:
                video = list(self.apps.me_toob.video_dict.values())[
                    random.randint(0, len(self.apps.me_toob.video_dict) - 1)]
                self.algo.algorithm(video)
                
            except ValueError:
                pass

    def check_mouse(self, event, mouse_pos):
        if event.button == 1:
            if self.active:
                clicked = self.help_btn.msg_image_rect.collidepoint(mouse_pos)
                if clicked:
                    webbrowser.open_new_tab(f'file://{os.getcwd()}/images/help.html')
                for i in range(len(self.app_buttons)):
                    clicked = self.app_buttons[i].rect.collidepoint(mouse_pos)
                    if clicked and self.app_buttons[i].app.purchased:
                        self.app_buttons[i].app.active = True
                        self.active = False
                        break
                    elif clicked and not self.app_buttons[i].app.purchased:
                        if self.app_buttons[i].app.cost <= self.settings.pretzels:
                            if self.settings.level >= self.app_buttons[i].app.level_needed:
                                self.app_buttons[i].app.purchased = True
                                self.settings.pretzels -= self.app_buttons[i].app.cost
                                self.settings.purchased_apps.append(self.app_buttons[i].app.app_name)
                                self.app_buttons[i].app.active = True
                                self.active = False
                                break
                            else:
                                self.display_error(
                                    f"You need to be at level {self.app_buttons[i].app.level_needed} to buy {self.app_buttons[i].app.app_name}.")
                        else:
                            self.display_error(
                                f"You need {self.app_buttons[i].app.cost - round(self.settings.pretzels)} pretzels to buy {self.app_buttons[i].app.app_name}.")

            clicked = self.pretzel_button.rect.collidepoint(mouse_pos)
            if clicked:
                self.reward_pretzels(self.settings.pretzels_per_click)
            clicked = self.bear_button.rect.collidepoint(mouse_pos)
            if clicked:
                self.feed_bear()
                self.check_level_up()

    def update_screen(self):
        self.bear_button.image_str = f'images/bear{self.settings.level}.png'
        self.bear_button.reload_img()
        end_t = time()
        if end_t - self.start_t >= 1:
            self.algorithm()
            self.start_t = time()

        self.settings.update_pps_value()

        # Pretzel/Info area: 0-500,0-800
        self.m.screen.fill((255, 248, 247), self.m.pretzel_area)
        self.pretzel_button.draw_image()
        self.bear_button.draw_image()
        if len(str(round(float(self.settings.pretzels / 1000000), 6))) >= 7 and self.settings.pretzels >= 1000000:
            pretzel_msg = f'{round(float(self.settings.pretzels / 1000000), 3)}mil. pretzels'
        else:
            pretzel_msg = f'{round(self.settings.pretzels)} pretzels'
        self.pretzel_counter.prep_msg(pretzel_msg)
        self.pretzel_counter.draw_box()
        self.pps_counter.prep_msg(f'{self.settings.pps} pps')
        self.pps_counter.draw_box()
        self.bear_fed_counter.prep_msg(f'Bear has been fed {self.settings.t_bear_fed} times')
        self.bear_fed_counter.draw_box()
        self.bear_lvl_counter.prep_msg(f'Level {self.settings.level} Bear')
        self.bear_lvl_counter.draw_box()
        self.bear_feed_cost_count.prep_msg(f'Bear needs {self.settings.bear_feed_cost} pretzels')
        self.bear_feed_cost_count.draw_box()
        if self.apps.stocks.active:
            self.pretzels_stock.prep_msg(
                f'{self.apps.stocks.get_stock_val() - self.settings.stock_buy_price} from stocks')
        self.pretzels_stock.draw_box()

        # App corner: 500-1600,0-800
        if self.apps.me_toob.active:
            self.apps.me_toob.update_screen()
            if self.apps.me_toob.posting and len(self.apps.me_toob.video_dict) >= 10:
                self.apps.me_toob.posting = False
                self.display_error('You can\'t have more than 10 videos at once!')

        elif self.apps.hack.active:
            self.apps.me_toob.check_vid_oldness()
            self.apps.hack.update_screen()
        elif self.apps.stocks.active:
            self.apps.stocks.update_screen()
        elif self.active:
            self.bg_img.draw_image()
            self.help_btn.draw_box()
            self.title_img.draw_box()
            for app in self.app_buttons:
                app.draw_image()
                if not app.app.purchased:
                    self.locks[self.app_buttons.index(app)].draw_image()
                    self.level_locks[self.app_buttons.index(app)].draw_box()

        if self.error_msg_active and self.error <= 8:
            self.error += 1
            self.error_msg.draw_box()
        elif self.error > 8:
            self.error = 0
            self.error_msg_active = False

        pygame.display.flip()

    def display_error(self, error):
        self.error_msg = TextBox(self.m, error, 0, 0, (0, 0, 0), (209, 32, 19), self.settings.screen_width // 2,
                                 self.settings.screen_height // 2, 40, True)
        self.error_msg.draw_box()
        self.error_msg_active = True

    def reward_pretzels(self, amount):
        self.settings.pretzels += amount

    def feed_bear(self):
        if self.settings.pretzels - self.settings.bear_feed_cost >= 0:
            self.settings.pretzels -= self.settings.bear_feed_cost
            self.settings.t_bear_fed += 1
            self.settings.bear_feed_cost += self.settings.bear_feed_cost // 15
            if self.settings.t_bear_fed >= 110:
                self.apps.me_toob.active = False
                self.apps.hack.active = False
                self.apps.stocks.active = False
                self.settings.game_running = False
        else:
            self.display_error(
                f'You need {self.settings.bear_feed_cost - round(self.settings.pretzels)} more pretzels to do that.')

    def check_level_up(self):
        if self.settings.t_bear_fed >= self.settings.level_up and self.settings.level < 10:
            self.settings.level += 1
            self.settings.level_up += 10
            self.settings.pretzels_per_click += self.settings.level
            self.bear_button.image_str = f'images/bear{self.settings.level}.png'
            self.bear_button.reload_img()

    def pretzels_ps(self):
        pygame.time.wait(100)
        self.settings.pretzels += self.settings.pps // 10
