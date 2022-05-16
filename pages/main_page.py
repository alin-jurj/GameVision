import pygame
from gui_elements import buttons, player_details, character_buying_box
from pages import leaderboard, play

pygame.init()

FPS = 60
background = pygame.image.load('../assets/main_menu.png')
monster = pygame.image.load('../assets/icons/monster.png')
character = pygame.image.load('../assets/characters/Artemis1_resized.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 20)
player_font = pygame.font.SysFont('Arial', 25)
game_name = FONT.render('ULTIMATE REFLEX FIGHTER', True, '#B2B600')

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def main_page(screen):
    clock = pygame.time.Clock()

    play_button = buttons.Button('PLAY', 200, 45, (110, 360), button_font)
    store_button = buttons.Button('STORE', 200, 45, (110, 420), button_font)
    inventory_button = buttons.Button('INVENTORY', 200, 45, (110, 480), button_font)
    leaderboard_button = buttons.Button('LEADERBOARD', 200, 45, (110, 540), button_font)
    profile_button = buttons.Button('PROFILE', 200, 45, (110, 600), button_font)
    settings_button = buttons.Button('SETTINGS', 200, 45, (110, 660), button_font)

    player = player_details.Player_Details(360, 140, (900, 60), player_font, 'Dutz', 10, 100, 960, monster)

    character_box = character_buying_box.Character_Buying_Box(240, 310, (900, 400), 'Artemis', character, 100, 20, 10,
                                                              100, 310)

    run = True
    leaderboard_page = 0
    play_page = 0
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        screen.blit(game_name, (280, 260))

        if play_button.draw(screen):
            play_page = 1
            run = False

        store_button.draw(screen)
        inventory_button.draw(screen)

        if leaderboard_button.draw(screen):
            leaderboard_page = 1
            run = False

        profile_button.draw(screen)
        settings_button.draw(screen)
        player.draw(screen)
        character_box.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if play_page == 1:
        play.play(screen)

    if leaderboard_page == 1:
        leaderboard.draw(screen)
