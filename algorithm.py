from PIL import Image, ImageDraw, ImageFont
from random import randint


class Video:
    def __init__(self, brand: str, text: str):
        self.brand = brand[2:]
        self.brand = self.brand.lower()
        self.views = 0
        brands = ['poopsi', 'adidos', 'pingles', 'schmapple']
        self.brand_id = 0
        for i in brands:
            if self.brand == i:
                self.brand_id = brands.index(i)
                break
        self.raw_text = text
        self.text = text.lower().split()
        self.random_post_id = ""

    def make_img(self):
        image = Image.open(f"images/{self.brand}.png").resize((500, 500))
        transrect = Image.open('images/trans_rect.png').resize((500, 500))
        image = Image.blend(image, transrect, .25)
        font = ImageFont.FreeTypeFont('fonts/porky_font.ttf', 30)
        draw = ImageDraw.Draw(image)
        _, _, _, h = draw.textbbox((0, 0), self.raw_text, font=font, stroke_width=2)
        draw.text(((250-h)//2, 260), self.raw_text, (randint(0, 255), randint(0, 255), randint(0, 255)), font=font,
                  stroke_width=2, stroke_fill=(255, 255, 255))
        for i in range(6):
            self.random_post_id += str(randint(0, 9))
        self.save_dir = f'images/posts/{self.random_post_id}.png'
        image.save(self.save_dir)


class Algorithm:
    def __init__(self, m):
        self.settings = m.stgs

    def analyze_vid(self, video, keywords):
        self.video = video
        self.video_points = 0
        self.keyword_list = keywords

        for word in self.video.text:
            if word in self.keyword_list:
                self.video_points += 1

        self.video_points += self.settings.level * 2
        if self.video_points > 25:
            self.video_points = 12
        self.sub_like_range = (0, self.video_points, self.video_points, self.video_points*2)

    def algorithm(self, value):
        sub_like_range = value[5]

        user = randint(0, 25)
        if sub_like_range[0] <= user <= sub_like_range[1]:
            value[2] += 1
            self.settings.get_like_view(1)
        elif sub_like_range[2] <= user <= sub_like_range[3]:
            self.settings.get_like_view(2)
            value[1] += 1

        elif user > sub_like_range[3]:
            # User did nothing
            pass

        value[4] += 1
        
        self.settings.views += 1
        self.settings.get_like_view(0)
        self.settings.update_like_sub()
