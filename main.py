import pygame
import sys

from settings import Settings
from game import Game
from box_gui import TextBox, ImageBox


class Main:
    def __init__(self):
        pygame.init()
        self.stgs = Settings(self)
        self.screen = pygame.display.set_mode((self.stgs.screen_width, self.stgs.screen_height))
        self.app_area = (self.stgs.screen_width // 3, 0, self.stgs.screen_width, self.stgs.screen_height)
        self.pretzel_area = (0, 0, self.app_area[0], self.stgs.screen_width)

        self.game = Game(self)
        self.end_screen_running = False
        self.golden_run = False

        pygame.display.set_caption('Pretzel Clicker')
        pygame_icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(pygame_icon)

        self.next_btn = ImageBox(self, 'images/next_arrow.png', 86, 80, self.stgs.screen_width // 2 - 43,
                                 self.stgs.screen_height - 100)
        self.skip_btn = TextBox(self, 'Skip', 0, 0, (0, 0, 0), (250, 250, 250), self.stgs.screen_width - 43,
                                self.stgs.screen_height - 110, 40, True, 'right')

        self.i = 0
        self.txts = ["Well,", 'Here we are.', 'You won [part of] the game.',
                     'You\'re probably wondering what will happen next...', 'Unless you done this before.',
                     'You get a GOLDEN PRETZEL!', 'Golden pretzels are the real prize.',
                     f'Get to 5 golden pretzels to REALLY win the game! (you have {self.stgs.golden_pretzels})',
                     f'For all your efforts, we\'ll award you {(self.stgs.golden_pretzels + 1) * 5000} pretzels.',
                     'Good luck!']
        self.txt_boxes = []
        for txt in self.txts:
            txts = TextBox(self, txt, 0, 0, (0, 0, 0), (255, 255, 255), self.stgs.screen_width // 2,
                           self.stgs.screen_height // 2, 40)
            self.txt_boxes.append(txts)

    def run(self):
        while self.stgs.game_running:
            self.game.check_inputs()

            self.game.pretzels_ps()

            self.game.update_screen()

        self.end_screen()

    def check_end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked = self.next_btn.rect.collidepoint(mouse_pos)
                    if clicked:
                        self.i += 1
                    clicked = self.skip_btn.msg_image_rect.collidepoint(mouse_pos)
                    if clicked:
                        self.i = 100

    def end_screen(self):
        self.stgs.game_running = False
        self.stgs.reset_stats()
        if self.stgs.golden_pretzels + 1 >= 5:
            self.golden_end()
        self.end_screen_running = True
        while self.end_screen_running:
            self.check_end_events()
            self.screen.fill((0, 0, 0))
            try:
                self.txt_boxes[self.i].draw_box()
            except IndexError:
                self.end_screen_running = False
                self.stgs.game_running = True
                self.stgs.pretzels += (self.stgs.golden_pretzels + 1) * 5000
                self.stgs.golden_pretzels += 1
                self.stgs.save_stats()
                self.i = 0
                self.run()
            self.next_btn.draw_image()
            self.skip_btn.draw_box()
            pygame.display.flip()

    def golden_end(self):
        txt = TextBox(self, 'YOU WON!! (click pretzel to restart)', 0, 0, (0, 0, 0), (255, 255, 255), self.stgs.screen_width//2, self.stgs.screen_height//2-200, 40)
        gold_pretzel = ImageBox(self, 'images/golden_pretzel.png', 225*2, 225*2, self.stgs.screen_width//2 - 225, self.stgs.screen_height//2 - 225)
        self.stgs.reset_stats()
        self.stgs.golden_pretzels = 0
        self.stgs.save_stats()
        self.stgs.load_stats()
        self.golden_run = True
        while self.golden_run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.golden_run = False
                    pygame.display.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        clicked = gold_pretzel.rect.collidepoint(mouse_pos)
                        if clicked:
                            self.golden_run = False
                            self.stgs.game_running = True
                            self.run()

            gold_pretzel.draw_image()
            txt.draw_box()
            pygame.display.flip()

    def exit(self):
        self.stgs.save_stats()
        self.stgs.game_running = False
        self.end_screen_running = False
        self.golden_run = False
        pygame.display.quit()
        sys.exit()


if __name__ == "__main__":
    Main().run()
