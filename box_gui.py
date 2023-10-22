import pygame.font


class Box:
    def __init__(self, m, width, height, x, y):
        self.settings = m.stgs
        self.screen = m.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = width, height

        self.rect = pygame.Rect(x, y, self.width, self.height)


class TextBox(Box):
    def __init__(self, m, msg, width, height, bg, text, x, y, ft_size: int, transparent=False, orientation='center',
                 app=None):
        super().__init__(m, width, height, x, y)
        self.app = app
        self.orientation = orientation
        self.transparent = transparent
        self.msg = msg

        self.button_color = bg
        self.text_color = text
        self.font = pygame.font.Font('fonts/porky_font.ttf', ft_size - 10)

        self.prep_msg(msg)

    def prep_msg(self, msg):
        if self.transparent:
            self.msg_image = self.font.render(msg, True, self.text_color)
        else:
            self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        if self.orientation == 'left':
            self.msg_image_rect.left = self.rect.left
            self.msg_image_rect.top = self.rect.top
        elif self.orientation == 'right':
            self.msg_image_rect.right = self.rect.right
            self.msg_image_rect.top = self.rect.top
        else:
            self.msg_image_rect.center = self.rect.center

    def draw_box(self):
        # draw a blank button, then draw the center
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class ImageBox(Box):
    def __init__(self, m, image_str, width, height, x, y, app=None):
        super().__init__(m, width, height, x, y)
        self.x = x
        self.y = y
        self.image_str = image_str
        self.app = app
        self.reload_img()
        
    def reload_img(self):
        self.image = pygame.image.load(self.image_str)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw_image(self):
        self.screen.blit(self.image, (self.x, self.y))
