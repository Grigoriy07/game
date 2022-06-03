import pygame, random, os, sys

WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_window_surface = pygame.Surface((WIDTH, HEIGHT))
game_window = pygame.Surface((WIDTH, HEIGHT))
start_window_surface.fill(WHITE)
game_over_surface = pygame.Surface((360, 240))
game_over_surface.fill(GREY)

pygame.display.set_caption("Пиу-пиу")
clock = pygame.time.Clock()

player_image_1 = pygame.image.load('player_images/Korabl.png')
player_image_2 = pygame.Surface((30, 40))
player_image_3 = pygame.Surface((30, 40))
player_image_2.fill(RED)
player_image_3.fill(WHITE)
start_game_button_image = pygame.image.load('data/start_game_button.png')
start_game_with_recording_button_image = pygame.image.load('data/start_game_with_recording.png')
repeat_button_image = pygame.image.load('data/repeat_button.png')
lazer_image = pygame.image.load('data/Lazer.png')
shield_image = pygame.image.load('data/Shield.png')
shield_on_player_image = pygame.image.load('data/Shield_PL.png')
meteor_20_image = pygame.image.load('data/Meteor20.png')
meteor_40_image = pygame.image.load('data/Meteor40.png')
meteor_70_image = pygame.image.load('data/Meteor40.png')
exit_button = pygame.image.load('data/exit.png')
right_click = pygame.image.load('data/right_image.png')
left_click = pygame.image.load('data/left_image.png')
playrs_images = [player_image_1, player_image_2, player_image_3]
image_index = 0
player_image = player_image_1

mobs_images_and_shield = [meteor_20_image, meteor_40_image, meteor_70_image]

shield_is_active = False
recordings = []

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.image_bullet = pygame.Surface((2, 10))
        self.rect = self.image.get_rect()
        self.rect.y = 560
        self.rect.x = 215
        self.speedx = 8
        self.last_hit = 0
        self.recharge = 200
        self.bullet_y = self.rect.y

    def update(self, left, right, shoot):
        if left:
            self.rect.x -= self.speedx
        elif right:
            self.rect.x += self.speedx
        if shoot:
            now_hit = pygame.time.get_ticks()
            if now_hit - self.last_hit > self.recharge:
                self.last_hit = now_hit
                self.shoot()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.bullet_y, self.image_bullet)
        if recording_go:
            all_sprites_c.add(bullet)
            bullets_c.add(bullet)
        else:
            all_sprites.add(bullet)
            bullets.add(bullet)

    def shoot_rec(self):
        bullet = Bullet(self.rect.centerx, self.bullet_y, self.image_bullet)
        all_sprites_c.add(bullet)
        bullets_c.add(bullet)



def load_image(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def draw_text(x, y, text, surface, size, color):
    f_1 = pygame.font.Font(None, size)
    text_s = f_1.render(str(text), False, color)
    surface.blit(text_s, (x, y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 10

    def update(self):
        if self.rect.y < -0:
            self.kill()
        self.rect.y -= 10

class Improvement(pygame.sprite.Sprite):
    def __init__(self, x=False, y=False):
        super().__init__()
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.kill()

    def recording_set(self):
        return [self.rect.x, self.rect.y, self.type]

class Lazer(Improvement):
        def __init__(self, x=False, y=False):
            super().__init__(x, y)
            self.type = 'lazer'
            self.image = lazer_image
            self.rect = self.image.get_rect()
            if x:
                self.rect.x = x
                self.rect.y = y
            else:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-50, -40)

        def baf(self, other):
            other.recharge = 0
            other.image_bullet = pygame.Surface((10, 560))
            other.bullet_y = 0

class Shield(Improvement):
                def __init__(self, x=False, y=False):
                    super().__init__(x, y)
                    self.type = 'shield'
                    self.image = shield_image
                    self.rect = self.image.get_rect()
                    if x:
                        self.rect.x = x
                        self.rect.y = y
                    else:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-50, -40)
class Mob(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-50, -40)
        self.speedy = random.randrange(1, 4)
        self.ticks = []
        self.data = [self.rect.x, self.rect.y, self.speedy, self.image]

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            make_new_mob()

    def recording_set(self):
        return self.data
def make_new_mob():
    image_key = random.randrange(0, 2)
    m = Mob(mobs_images_and_shield[image_key])
    all_sprites.add(m)
    mobs.add(m)
    if recording_start:
        recording_data['mobs'].append(m.recording_set())
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        size = self.image.get_rect().size
        self.height = size[1]
        self.width = size[0]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def pressed(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False

    def change_image(self, image):
        self.image = image
class Mob_recording(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.list_speedy = speedy
        self.rect.x = x
        self.rect.y = y
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()