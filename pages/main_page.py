import pygame
from gui_elements import buttons, player_details

pygame.init()

FPS = 60
background = pygame.image.load('assets/main_menu.png')
monster = pygame.image.load('assets/icons/monster.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 20)
player_font = pygame.font.SysFont('Arial', 26)
game_name = FONT.render('ULTIMATE REFLEX FIGHTER', True, '#B2B600')

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def main_page():
    clock = pygame.time.Clock()

    play_button = buttons.Button('PLAY', 200, 45, (110, 360), button_font)
    store_button = buttons.Button('STORE', 200, 45, (110, 420), button_font)
    inventory_button = buttons.Button('INVENTORY', 200, 45, (110, 480), button_font)
    leaderboard_button = buttons.Button('LEADERBOARD', 200, 45, (110, 540), button_font)
    profile_button = buttons.Button('PROFILE', 200, 45, (110, 600), button_font)
    settings_button = buttons.Button('SETTINGS', 200, 45, (110, 660), button_font)

    player = player_details.Player_Details(360, 140, (900, 60), player_font, 'Dutz', 10, 100, monster)

    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        screen.blit(game_name, (280, 260))

        play_button.draw(screen)
        store_button.draw(screen)
        inventory_button.draw(screen)
        leaderboard_button.draw(screen)
        profile_button.draw(screen)
        settings_button.draw(screen)
        player.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
