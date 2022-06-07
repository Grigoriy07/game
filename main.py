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
score = 0
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
improvements = pygame.sprite.Group()
start_window_sprites = pygame.sprite.Group()
game_over_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

lazer_event = pygame.USEREVENT + 1
lazer_time_event = pygame.USEREVENT + 2

shield_event = pygame.USEREVENT + 3
shield_time_event = pygame.USEREVENT + 4

pygame.time.set_timer(lazer_event, random.randrange(1500, 30000))
pygame.time.set_timer(shield_event, random.randrange(1000, 20000))

running = True
start_window = True
game_running = False
recording_go = False
recording_start = False
game_over = False

player = Player()
all_sprites.add(player)

start_button = Button(100, 100, start_game_button_image)
recording_start_button = Button(250, 100, start_game_with_recording_button_image)
restart_button = Button(180, 300, start_game_button_image)
watch_repeat_button = Button(180, 345, repeat_button_image)
exit_button = Button(120, 300, exit_button)
right_click_button = Button(250, 160, right_click)
left_click_button = Button(160, 160, left_click)


start_window_sprites.add(start_button)
start_window_sprites.add(recording_start_button)
start_window_sprites.add(right_click_button)
start_window_sprites.add(left_click_button)
game_over_sprites.add(restart_button)
game_over_sprites.add(exit_button)
player_sprite.add(player)
text = ''

right = False
left = False
shoot = False

while running:
    clock.tick(FPS)
    if start_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.pressed(event.pos):
                    start_window = False
                    game_running = True
                    for i in range(4):
                        make_new_mob()
                elif recording_start_button.pressed(event.pos):
                    start_window = False
                    game_running = True
                    recording_start = True
                    recording_data = {'improvents': [],
                              'mobs': []}
                    recording_events = []
                    for i in range(4):
                        make_new_mob()
                    game_over_sprites.add(watch_repeat_button)
                elif right_click_button.pressed(event.pos):
                    image_index += 1
                    if image_index == 3:
                        image_index = 0
                    player.kill()
                    player_image = playrs_images[image_index]

                    player = Player()
                    all_sprites.add(player)
                    player_sprite.add(player)
                elif left_click_button.pressed(event.pos):
                    image_index -= 1
                    if image_index == -1:
                        image_index = 2
                    player.kill()
                    player_image = playrs_images[image_index]

                    player = Player()
                    all_sprites.add(player)
                    player_sprite.add(player)

        start_window_surface.fill(WHITE)
        start_window_surface.blit(player_image, (200, 160))
        start_window_sprites.update()
        start_window_sprites.draw(start_window_surface)
        screen.blit(start_window_surface, (0, 0))
        pygame.display.flip()
    if game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                    left = False
                if event.key == pygame.K_LEFT:
                    left = True
                    right = False
                if event.key == pygame.K_SPACE:
                    shoot = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_SPACE:
                    shoot = False

            if event.type == lazer_event:
                imp = Lazer()
                improvements.add(imp)
                all_sprites.add(imp)
                pygame.time.set_timer(lazer_event, random.randrange(10000, 30000))
                pygame.time.set_timer(lazer_time_event, 4000)
                if recording_start:
                    recording_data['improvents'].append(imp.recording_set())

            if event.type == shield_event:
                imp = Shield()
                improvements.add(imp)
                all_sprites.add(imp)
                pygame.time.set_timer(shield_event, random.randrange(8000, 23000))
                pygame.time.set_timer(shield_time_event, 6000)
                if recording_start:
                    recording_data['improvents'].append(imp.recording_set())

            if event.type == shield_time_event:
                shield_is_active = False

            if event.type == lazer_time_event:
                player.recharge = 200
                player.image_bullet = pygame.Surface((2, 10))
                player.bullet_y = player.rect.y
    if game_over:
        all_sprites.empty()
        mobs.empty()
        improvements.empty()
        bullets.empty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.pressed(event.pos):
                    for i in range(4):
                        make_new_mob()
                    player = Player()
                    all_sprites.add(player)
                    player_sprite.add(player)
                    game_over = False
                    game_running = True
                    right = False
                    left = False
                    shoot = False
                    score = 0
                    screen.fill(BLACK)
                    pygame.time.set_timer(lazer_event, random.randrange(1500, 30000))
                    pygame.time.set_timer(shield_event, random.randrange(1000, 20000))
                    recording_data = {'improvents': [],
                                      'mobs': []}
                    recording_events = []
                elif exit_button.pressed(event.pos):
                    player = Player()
                    all_sprites.add(player)
                    player_sprite.add(player)
                    game_over = False
                    start_window = True
                    right = False
                    left = False
                    shoot = False
                    score = 0
                    screen.fill(BLACK)
                    pygame.time.set_timer(lazer_event, random.randrange(1500, 30000))
                    pygame.time.set_timer(shield_event, random.randrange(1000, 20000))
                    recording_data = {'improvents': [],
                                      'mobs': []}
                    recording_events = []
                if recording_start:
                    if watch_repeat_button.pressed(event.pos):
                        recording_go = True
                        screen.fill(BLACK)

        game_over_surface.fill(GREY)
        draw_text(50, 0, 'ВАШ РЕЗУЛЬТАТ', game_over_surface, 40, BLACK)
        draw_text(180 - 30 - len(str(score)) + 1, 40, score, game_over_surface, 60, BLACK)
        screen.blit(game_over_surface, (60, 180))
        game_over_sprites.draw(screen)
        pygame.display.flip()
        if recording_start:
            if events == []:
                recording_events.append('')
            else:
                recording_events.append(events)
        player.update(left, right, shoot)
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        improvement_hits = pygame.sprite.groupcollide(improvements, bullets, True, True)
        if shield_is_active:
            player_hit = pygame.sprite.groupcollide(player_sprite, mobs, False, True)
        else:
            player_hit = pygame.sprite.groupcollide(player_sprite, mobs, True, True)
            if player_hit:
                game_running = False
                game_over = True

        for i in hits:
            make_new_mob()
            score += 1

        for i in player_hit:
            make_new_mob()
            score += 1

        for i in improvement_hits:
            if i.type == 'lazer':
                i.baf(player)
            if i.type == 'shield':
                shield_is_active = True

        screen.fill(BLACK)
        mobs.update()
        improvements.update()
        bullets.update()
        all_sprites.draw(screen)
        if shield_is_active:
            screen.blit(shield_on_player_image, (player.rect.x, player.rect.y))
        draw_text(220, 0, score, screen, 100, GREEN)
        pygame.display.flip()
