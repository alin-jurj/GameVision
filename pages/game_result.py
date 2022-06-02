import pygame
from pages import main_page
from database import queries
from gui_elements import image_buttons

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


def end_game_result(screen, logged_in_user, map_choice, text):
    clock = pygame.time.Clock()

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))

    run = True
    main = False

    xp = 0
    money = 0
    win_loss = 0

    while run:
        screen.fill((0, 0, 0))
        screen.blit(map_choice, (0, 0))
        screen.blit(text, (500, 500))
        clock.tick(FPS)

        if text == 'YOU WON!':
            xp = 100
            money = 50
            win_loss = 1
        else:
            xp = 40
            money = 15
            win_loss = 0

        if back_button.draw(screen):
            run = False
            main = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    logged_in_user.set_xp(xp)
    logged_in_user.add_money(money)

    if win_loss == 1:
        logged_in_user.add_wins()
        wins = logged_in_user.get_wins()
        queries.update_wins(logged_in_user.get_userId(), wins)
    else:
        logged_in_user.add_losses()
        losses = logged_in_user.get_losses()
        queries.update_losses(logged_in_user.get_userId(), losses)

    queries.update_user_money(logged_in_user.get_userId(), logged_in_user.get_money())
    queries.update_user_lvl_xp(logged_in_user.get_userId(), logged_in_user.get_lvl(), logged_in_user.get_xp())

    if main:
        main_page.main_page(screen, logged_in_user)
