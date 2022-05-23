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