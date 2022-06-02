import pygame
from pages import main_page
from database import queries
from gui_elements import image_buttons, buttons, character_buying_box, icon_box

pygame.init()

FPS = 60
background = pygame.image.load('../assets/main_menu.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 28)
text_font = pygame.font.SysFont('Arial', 32)
back = pygame.image.load('../assets/misc/back.png')
path_to_char = '../assets/characters/body/'
path_to_icons = '../assets/icons/'


def game_result(screen, logged_in_user, map_choice, text):
    clock = pygame.time.Clock()

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))

    run = True
    main = False

    while run:
        screen.fill((0, 0, 0))
        screen.blit(map_choice, (0, 0))
        screen.blit(text, (500,500))
        clock.tick(FPS)

        if back_button.draw(screen):
            run = False
            main = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if main:
        main_page.main_page(screen, logged_in_user)